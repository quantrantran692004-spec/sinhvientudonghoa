from __future__ import annotations

import ctypes
import json
import os
import re
import shutil
import socket
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


AMAZON_PACKAGE = "com.amazon.mShop.android.shopping"
PLAY_PACKAGE = "com.android.vending"
PLAY_SERVICES_PACKAGE = "com.google.android.gms"
PLAY_URL = f"market://details?id={AMAZON_PACKAGE}"
IMAGE_ID = "system-images;android-35;google_apis_playstore;x86_64"
LOCAL_ADB_SERVER_PORT = "5038"  # Keep SDK ADB separate from Swarmote's bundled ADB 36 on 5037.
STATES = {
    "DEVICE_OFF", "DEVICE_STARTING", "DEVICE_READY", "APP_NOT_INSTALLED",
    "APP_INSTALLING", "APP_READY", "REGISTRATION_SCREEN",
    "USER_INPUT_REQUIRED", "WAITING_FOR_OTP", "ERROR", "STOPPED",
}


class ToolError(RuntimeError):
    pass


def app_data_dir() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / ".local" / "share")
    return base / "AmazonAndroidTool"


def sdk_root() -> Path:
    for value in (os.environ.get("ANDROID_HOME"), os.environ.get("ANDROID_SDK_ROOT")):
        if value:
            return Path(value).expanduser()
    return Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "Android" / "Sdk"


def executable(name: str, root: Path | None = None) -> Path | None:
    root = root or sdk_root()
    suffix = ".exe" if name in ("adb", "emulator") else ".bat"
    locations = {
        "adb": [root / "platform-tools" / "adb.exe"],
        "emulator": [root / "emulator" / "emulator.exe"],
        "sdkmanager": [root / "cmdline-tools" / "latest" / "bin" / "sdkmanager.bat"],
        "avdmanager": [root / "cmdline-tools" / "latest" / "bin" / "avdmanager.bat"],
    }
    for path in locations.get(name, []):
        if path.is_file():
            return path
    found = shutil.which(name + suffix) or shutil.which(name)
    return Path(found) if found else None


def run(args: list[str | Path], timeout: int = 30, check: bool = True,
        input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            [str(arg) for arg in args], capture_output=True, text=True,
            errors="replace", timeout=timeout,
            **({"creationflags": subprocess.CREATE_NO_WINDOW}
               if sys.platform == "win32" else {}),
            **({"stdin": subprocess.DEVNULL} if input_text is None else {"input": input_text}),
        )
    except subprocess.TimeoutExpired as exc:
        raise ToolError(f"Lệnh quá thời gian {timeout}s: {args[0]}") from exc
    except OSError as exc:
        raise ToolError(f"Không chạy được {args[0]}: {exc}") from exc
    if check and result.returncode:
        detail = (result.stderr or result.stdout).strip()[-600:]
        raise ToolError(f"{args[0]} trả mã {result.returncode}: {detail}")
    return result


def available_memory_mb() -> int:
    if sys.platform == "win32":
        class MemoryStatus(ctypes.Structure):
            _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong),
                       ("total_phys", ctypes.c_ulonglong), ("avail_phys", ctypes.c_ulonglong),
                       ("total_page", ctypes.c_ulonglong), ("avail_page", ctypes.c_ulonglong),
                       ("total_virtual", ctypes.c_ulonglong), ("avail_virtual", ctypes.c_ulonglong),
                       ("avail_extended", ctypes.c_ulonglong)]
        status = MemoryStatus()
        status.length = ctypes.sizeof(status)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            raise ToolError("Không đọc được RAM trống")
        return status.avail_phys // (1024 * 1024)
    try:
        import psutil
        return psutil.virtual_memory().available // (1024 * 1024)
    except ImportError as exc:
        raise ToolError("Cần psutil để đọc RAM trên hệ điều hành này") from exc


@dataclass(frozen=True)
class Device:
    number: int
    name: str
    avd: str
    port: int

    @property
    def serial(self) -> str:
        return f"emulator-{self.port}"


DEVICES = [Device(i, f"Android {i:02d}", f"Amazon_Android_{i:02d}", 5554 + (i - 1) * 2)
           for i in range(1, 6)]


def get_device(number: int) -> Device:
    if number not in range(1, 6):
        raise ToolError("Chọn thiết bị từ 1 đến 5")
    return DEVICES[number - 1]


class Store:
    def __init__(self, path: Path | None = None):
        self.path = path or app_data_dir() / "state.sqlite3"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("CREATE TABLE IF NOT EXISTS devices (number INTEGER PRIMARY KEY, state TEXT NOT NULL, detail TEXT NOT NULL, boot_seconds REAL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, at TEXT NOT NULL, number INTEGER, state TEXT NOT NULL, detail TEXT NOT NULL)")
        for device in DEVICES:
            self.db.execute("INSERT OR IGNORE INTO devices(number,state,detail) VALUES(?,?,?)", (device.number, "DEVICE_OFF", "Chưa kiểm tra"))
        self.db.commit()

    def close(self) -> None:
        self.db.close()

    def set(self, device: Device, state: str, detail: str, boot_seconds: float | None = None) -> None:
        if state not in STATES:
            raise ValueError(state)
        # Callers pass operational details only; never pass credentials or UI contents here.
        at = datetime.now(timezone.utc).isoformat()
        with self.db:
            self.db.execute("UPDATE devices SET state=?,detail=?,boot_seconds=COALESCE(?,boot_seconds) WHERE number=?",
                            (state, detail, boot_seconds, device.number))
            self.db.execute("INSERT INTO events(at,number,state,detail) VALUES(?,?,?,?)",
                            (at, device.number, state, detail))

    def devices(self) -> list[dict]:
        rows = self.db.execute("SELECT number,state,detail,boot_seconds FROM devices ORDER BY number").fetchall()
        return [dict(number=n, state=s, detail=d, boot_seconds=b) for n, s, d, b in rows]

    def events(self, number: int | None = None, limit: int = 30) -> list[dict]:
        if number is None:
            rows = self.db.execute("SELECT at,number,state,detail FROM events ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        else:
            rows = self.db.execute("SELECT at,number,state,detail FROM events WHERE number=? ORDER BY id DESC LIMIT ?", (number, limit)).fetchall()
        return [dict(at=a, number=n, state=s, detail=d) for a, n, s, d in rows]


def adb(device: Device | None, *args: str, timeout: int = 30, check: bool = True) -> subprocess.CompletedProcess[str]:
    tool = executable("adb")
    if not tool:
        raise ToolError("Thiếu ADB: cài Android SDK Platform Tools")
    cmd: list[str | Path] = [tool, "-P", LOCAL_ADB_SERVER_PORT]
    if device:
        cmd += ["-s", device.serial]
    return run(cmd + list(args), timeout=timeout, check=check)


def connected_devices() -> set[str]:
    result = adb(None, "devices")
    return set(re.findall(r"^(emulator-\d+)\s+device\s*$", result.stdout, re.M))


def emulator_serials() -> set[str]:
    result = adb(None, "devices")
    return set(re.findall(r"^(emulator-\d+)\s+\S+\s*$", result.stdout, re.M))


def port_occupied(port: int) -> bool:
    with socket.socket() as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def device_avd_name(device: Device) -> str:
    result = adb(device, "emu", "avd", "name", check=False)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip() and line.strip() != "OK"]
    return lines[0] if result.returncode == 0 and lines else ""


def require_own_device(device: Device) -> None:
    if device.serial not in connected_devices():
        raise ToolError(f"ADB chưa thấy {device.serial}")
    actual = device_avd_name(device)
    if actual != device.avd:
        raise ToolError(f"Cổng {device.port} đang thuộc AVD {actual or 'không xác định'}, không phải {device.avd}")


def avd_names() -> set[str]:
    tool = executable("emulator")
    if not tool:
        return set()
    result = run([tool, "-list-avds"])
    return set(result.stdout.splitlines())


def installed_image(image_id: str = IMAGE_ID) -> bool:
    parts = image_id.split(";")
    if len(parts) != 4 or parts[0] != "system-images" or ".." in parts:
        return False
    return (sdk_root().joinpath(*parts) / "system.img").is_file()


def configure_avd(device: Device) -> None:
    config = Path.home() / ".android" / "avd" / f"{device.avd}.avd" / "config.ini"
    if not config.exists():
        raise ToolError(f"Không tìm thấy cấu hình AVD: {config}")
    contents = config.read_text(encoding="utf-8")
    if "google_apis_playstore" not in contents:
        raise ToolError(f"{device.avd} không dùng Google Play system image")
    settings = {"hw.ramSize": "1536", "vm.heapSize": "192", "hw.lcd.width": "720",
                "hw.lcd.height": "1280", "hw.lcd.density": "320", "PlayStore.enabled": "yes"}
    for key, value in settings.items():
        contents = re.sub(rf"(?m)^{re.escape(key)}=.*$", "", contents)
        contents += f"\n{key}={value}"
    config.write_text(contents.strip() + "\n", encoding="utf-8")


def create_avd(device: Device, image_id: str = IMAGE_ID) -> str:
    manager = executable("avdmanager")
    if not manager:
        raise ToolError("Thiếu avdmanager: cài Android SDK Command-line Tools")
    if not installed_image(image_id):
        raise ToolError(f"Chưa cài Google Play system image: {image_id}")
    if device.avd in avd_names():
        configure_avd(device)
        return "AVD đã tồn tại; đã xác minh cấu hình Google Play"
    result = run([manager, "create", "avd", "-n", device.avd, "-k", image_id],
                 timeout=120, input_text="no\n")
    configure_avd(device)
    return result.stdout.strip() or "Đã tạo AVD"


def start_device(device: Device, store: Store, allow_second: bool = False,
                 timeout: int = 240, force_low_memory: bool = False) -> float:
    tool = executable("emulator")
    if not tool:
        raise ToolError("Thiếu Android Emulator")
    if device.avd not in avd_names():
        raise ToolError(f"Chưa có AVD {device.avd}; chạy create-avd {device.number}")
    active = emulator_serials()
    if device.serial in active:
        require_own_device(device)
        raise ToolError(f"{device.name} đã chạy")
    if len(active) >= 2:
        raise ToolError("Đã có 2 emulator hoạt động; giới hạn tối đa là 2")
    if active and not allow_second:
        raise ToolError("Thiết bị thứ hai cần --allow-second và đủ RAM")
    required_mb = 3072 if active else 2304
    free_mb = available_memory_mb()
    if free_mb < required_mb and not force_low_memory:
        detail = f"RAM trống {free_mb} MB, cần ít nhất {required_mb} MB để khởi động an toàn"
        store.set(device, "ERROR", detail)
        raise ToolError(detail)
    if port_occupied(device.port) or port_occupied(device.port + 1):
        raise ToolError(f"Cổng {device.port}/{device.port + 1} đã được sử dụng")
    detail = f"Đang khởi động {device.avd}"
    if force_low_memory and free_mb < required_mb:
        detail += f"; người dùng cho phép thử với {free_mb} MB RAM trống"
    store.set(device, "DEVICE_STARTING", detail)
    log = app_data_dir() / f"emulator-{device.number:02d}.log"
    began = time.monotonic()
    process = None
    try:
        with log.open("ab") as output:
            flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            process = subprocess.Popen([str(tool), "-avd", device.avd, "-port", str(device.port),
                                        "-no-audio"], stdout=output, stderr=output,
                                       creationflags=flags)
        while time.monotonic() - began < timeout:
            if process.poll() is not None:
                raise ToolError(f"Emulator thoát với mã {process.returncode}; xem {log}")
            try:
                if device.serial in connected_devices():
                    require_own_device(device)
                    boot = adb(device, "shell", "getprop", "sys.boot_completed", check=False)
                    if boot.stdout.strip() == "1":
                        seconds = round(time.monotonic() - began, 1)
                        store.set(device, "DEVICE_READY", f"Android đã khởi động sau {seconds}s; ADB sẵn sàng", seconds)
                        return seconds
            except ToolError:
                # ADB may transiently reset while Android boots.
                pass
            time.sleep(3)
        raise ToolError(f"Emulator chưa khởi động sau {timeout}s; xem {log}")
    except Exception as exc:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
        store.set(device, "ERROR", str(exc))
        raise


def stop_device(device: Device, store: Store) -> None:
    require_own_device(device)
    adb(device, "emu", "kill", timeout=15)
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if device.serial not in connected_devices():
            store.set(device, "STOPPED", "Emulator đã dừng")
            return
        time.sleep(1)
    store.set(device, "ERROR", "Đã gửi lệnh dừng nhưng emulator vẫn kết nối")
    raise ToolError("Emulator chưa dừng sau 30s")


def emulator_processes(device: Device):
    try:
        import psutil
    except ImportError as exc:
        raise ToolError("Cần cài psutil để theo dõi và dừng khẩn cấp emulator") from exc
    matches = []
    for process in psutil.process_iter(["name", "cmdline"]):
        try:
            args = process.info["cmdline"] or []
            name = (process.info["name"] or "").lower()
            if "emulator" not in name:
                continue
            avd_match = any(args[i] == "-avd" and args[i + 1] == device.avd
                            for i in range(len(args) - 1)) or f"@{device.avd}" in args
            port_match = any(args[i] == "-port" and args[i + 1] == str(device.port)
                             for i in range(len(args) - 1))
            if avd_match and port_match:
                matches.append(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return matches


def device_resources(device: Device) -> dict:
    try:
        import psutil
    except ImportError as exc:
        raise ToolError("Cần cài psutil để theo dõi tài nguyên") from exc
    processes = {}
    for parent in emulator_processes(device):
        try:
            for process in [parent, *parent.children(recursive=True)]:
                processes[process.pid] = process
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    total_rss = 0
    for process in processes.values():
        try:
            total_rss += process.memory_info().rss
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    try:
        online = device.serial in connected_devices() and device_avd_name(device) == device.avd
    except ToolError:
        online = False
    return {"name": device.name, "serial": device.serial, "adb_ready": online,
            "emulator_pids": sorted(processes), "emulator_ram_mb": round(total_rss / 1048576),
            "host_cpu_percent": psutil.cpu_percent(interval=0.2),
            "host_free_ram_mb": available_memory_mb()}


def emergency_stop(device: Device, store: Store) -> None:
    try:
        if device.serial in connected_devices():
            require_own_device(device)
            adb(device, "emu", "kill", timeout=10, check=False)
    except ToolError:
        pass
    parents = emulator_processes(device)
    processes = {}
    for parent in parents:
        try:
            for process in [*parent.children(recursive=True), parent]:
                processes[process.pid] = process
        except Exception:
            continue
    for process in processes.values():
        try:
            process.terminate()
        except Exception:
            pass
    if processes:
        import psutil
        _, alive = psutil.wait_procs(list(processes.values()), timeout=5)
        for process in alive:
            try:
                process.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    if port_occupied(device.port) or port_occupied(device.port + 1):
        store.set(device, "ERROR", "Dừng khẩn cấp chưa giải phóng cổng emulator")
        raise ToolError("Cổng emulator vẫn được sử dụng sau dừng khẩn cấp")
    store.set(device, "STOPPED", "Đã dừng khẩn cấp emulator")


def package_installed(device: Device, package: str) -> bool:
    result = adb(device, "shell", "pm", "path", package, check=False)
    return result.returncode == 0 and any(line.startswith("package:") for line in result.stdout.splitlines())


def play_install_verified(device: Device) -> bool:
    result = adb(device, "shell", "pm", "list", "packages", "-i", AMAZON_PACKAGE, check=False)
    return result.returncode == 0 and any(
        line.startswith(f"package:{AMAZON_PACKAGE} ") and "installer=com.android.vending" in line
        for line in result.stdout.splitlines()
    )


def check_play(device: Device) -> None:
    require_own_device(device)
    missing = [name for name in (PLAY_PACKAGE, PLAY_SERVICES_PACKAGE) if not package_installed(device, name)]
    if missing:
        raise ToolError(f"AVD không có Google Play: thiếu {', '.join(missing)}")


def install_amazon(device: Device, store: Store, timeout: int = 600) -> None:
    check_play(device)
    if package_installed(device, AMAZON_PACKAGE):
        if not play_install_verified(device):
            raise ToolError("Amazon đã cài nhưng không xác minh được nguồn cài Google Play")
        store.set(device, "DEVICE_READY", "Amazon Shopping đã cài từ Google Play; chưa kiểm tra mở")
        return
    store.set(device, "APP_INSTALLING", "Đang chờ người dùng cài Amazon Shopping từ Google Play")
    try:
        result = adb(device, "shell", "am", "start", "-a", "android.intent.action.VIEW",
                     "-d", PLAY_URL, "-p", PLAY_PACKAGE)
        if "Error" in result.stdout or "Exception" in result.stdout:
            raise ToolError(f"Không mở được Google Play: {result.stdout.strip()}")
        print("Google Play đã mở. Cài Amazon Shopping chính thức trên cửa sổ emulator.", flush=True)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if package_installed(device, AMAZON_PACKAGE):
                if not play_install_verified(device):
                    raise ToolError("Amazon xuất hiện nhưng không xác minh được nguồn cài Google Play")
                store.set(device, "DEVICE_READY", "Amazon Shopping đã cài từ Google Play; chưa kiểm tra mở")
                return
            time.sleep(4)
        raise ToolError("Hết thời gian chờ cài Amazon; có thể ứng dụng không khả dụng theo khu vực/tương thích")
    except Exception as exc:
        store.set(device, "ERROR", str(exc))
        raise


def open_amazon(device: Device, store: Store) -> None:
    require_own_device(device)
    if not package_installed(device, AMAZON_PACKAGE):
        store.set(device, "APP_NOT_INSTALLED", "Android Package Manager chưa thấy Amazon Shopping")
        raise ToolError("Amazon Shopping chưa được cài")
    if not play_install_verified(device):
        raise ToolError("Không xác minh được Amazon Shopping đã cài từ Google Play")
    try:
        result = adb(device, "shell", "monkey", "-p", AMAZON_PACKAGE, "-c",
                     "android.intent.category.LAUNCHER", "1")
        if "Events injected: 1" not in result.stdout:
            raise ToolError("Không gửi được sự kiện khởi chạy Amazon Shopping")
        time.sleep(8)
        pid = adb(device, "shell", "pidof", AMAZON_PACKAGE, check=False).stdout.strip()
        if not pid:
            raise ToolError("Amazon Shopping đã thoát hoặc crash sau khi mở")
        window = adb(device, "shell", "dumpsys", "window", check=False).stdout
        focus_lines = [line for line in window.splitlines()
                       if "mCurrentFocus=" in line or "mFocusedApp=" in line]
        if not any(AMAZON_PACKAGE in line for line in focus_lines):
            raise ToolError("Amazon Shopping còn tiến trình nhưng không ở màn hình trước")
        store.set(device, "APP_READY", "Amazon Shopping đang chạy và ở màn hình trước")
    except Exception as exc:
        store.set(device, "ERROR", str(exc))
        raise


def doctor() -> dict:
    root = sdk_root()
    avds: list[str] = []
    try:
        avds = sorted(avd_names())
    except ToolError:
        pass
    try:
        devices = sorted(connected_devices())
    except ToolError:
        devices = []
    accel = None
    emulator = executable("emulator")
    if emulator:
        result = run([emulator, "-accel-check"], timeout=20, check=False)
        accel = {"ok": result.returncode == 0, "detail": (result.stdout + result.stderr).strip()[-400:]}
    appium = shutil.which("appium") or shutil.which("appium.cmd")
    driver = None
    if appium:
        result = run([appium, "driver", "list", "--installed"], timeout=20, check=False)
        driver = "uiautomator2" in result.stdout.lower()
    free_ram = available_memory_mb()
    try:
        import psutil  # noqa: F401
        psutil_available = True
    except ImportError:
        psutil_available = False
    return {
        "python": sys.version.split()[0], "sdk_root": str(root),
        "local_adb_server_port": int(LOCAL_ADB_SERVER_PORT),
        "tools": {name: str(executable(name)) if executable(name) else None
                  for name in ("adb", "emulator", "sdkmanager", "avdmanager")},
        "java": shutil.which("java"), "node": shutil.which("node"),
        "psutil": psutil_available,
        "appium": appium, "uiautomator2": driver,
        "google_play_image": installed_image(), "avds": avds,
        "adb_devices": devices, "acceleration": accel,
        "free_ram_mb": free_ram,
        "can_start_first": free_ram >= 2304,
        "can_start_second": free_ram >= 3072,
    }


def print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))
