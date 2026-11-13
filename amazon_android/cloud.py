"""ADB bridge for an already-running cloud phone exposed on local loopback.

Swarmote's desktop Terminal creates its own authenticated SSH tunnel. This
module never requests its credentials or calls undocumented service endpoints.
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from dataclasses import dataclass
from os import environ
from pathlib import Path

import psutil

from .core import AMAZON_PACKAGE, PLAY_PACKAGE, PLAY_SERVICES_PACKAGE, ToolError, executable, run


LOOPBACK_SERIAL = re.compile(r"^(?:127\.0\.0\.1|localhost):([1-9]\d{0,4})$")


@dataclass(frozen=True)
class CloudPhone:
    serial: str

    def __post_init__(self) -> None:
        match = LOOPBACK_SERIAL.fullmatch(self.serial)
        if not match or int(match.group(1)) > 65535:
            raise ToolError("Chỉ nhận cổng ADB cục bộ dạng 127.0.0.1:<port> từ Swarmote")


def swarmote_adb_path() -> Path:
    base = Path(environ.get("LOCALAPPDATA", str(Path.home())))
    bundled = base / "Programs" / "Swarmote" / "resources" / "adb" / "bin" / "win" / "adb.exe"
    if bundled.is_file():
        return bundled
    sdk = executable("adb")
    if sdk:
        return sdk
    raise ToolError("Không tìm thấy ADB của Swarmote hoặc Android SDK")


def swarmote_tunnel_owner(port: int) -> bool:
    expected = Path(environ.get("LOCALAPPDATA", str(Path.home()))) / "Programs" / "Swarmote" / "Swarmote.exe"
    for connection in psutil.net_connections(kind="tcp"):
        if connection.status != psutil.CONN_LISTEN or not connection.laddr or not connection.pid:
            continue
        if connection.laddr.port != port or connection.laddr.ip != "127.0.0.1":
            continue
        try:
            if psutil.Process(connection.pid).exe().casefold() == str(expected).casefold():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False


def cloud_adb(phone: CloudPhone | None, *args: str, timeout: int = 30,
              check: bool = True, input_text: str | None = None):
    command: list[str | Path] = [swarmote_adb_path()]
    if phone:
        command += ["-s", phone.serial]
    return run(command + list(args), timeout=timeout, check=check, input_text=input_text)


def cloud_serials() -> dict[str, str]:
    output = cloud_adb(None, "devices").stdout
    devices = {}
    for line in output.splitlines():
        fields = line.split()
        if len(fields) >= 2:
            match = LOOPBACK_SERIAL.fullmatch(fields[0])
            if match and swarmote_tunnel_owner(int(match.group(1))):
                devices[fields[0]] = fields[1]
    return devices


def cloud_screenshot(phone: CloudPhone, *, timeout: int) -> bytes:
    """Capture Android pixels directly, without writing a screenshot to disk."""
    try:
        result = subprocess.run(
            [str(swarmote_adb_path()), "-s", phone.serial, "exec-out", "screencap", "-p"],
            stdin=subprocess.DEVNULL, capture_output=True, timeout=timeout, check=True,
            **({"creationflags": subprocess.CREATE_NO_WINDOW} if sys.platform == "win32" else {}),
        )
    except (OSError, subprocess.SubprocessError):
        raise ToolError("Không chụp được màn hình Android để tìm nút") from None
    return result.stdout


def require_online(phone: CloudPhone) -> None:
    state = cloud_serials().get(phone.serial)
    if state != "device":
        raise ToolError(f"ADB chưa kết nối {phone.serial} (trạng thái: {state or 'không thấy'})")


def prop(phone: CloudPhone, key: str) -> str:
    return cloud_adb(phone, "shell", "getprop", key).stdout.strip()


def package_path(phone: CloudPhone, package: str) -> str | None:
    result = cloud_adb(phone, "shell", "pm", "path", package, check=False)
    if result.returncode:
        return None
    return next((line.removeprefix("package:") for line in result.stdout.splitlines()
                 if line.startswith("package:")), None)


def reported_installer(phone: CloudPhone) -> str | None:
    result = cloud_adb(phone, "shell", "pm", "list", "packages", "-i",
                       AMAZON_PACKAGE, check=False)
    for line in result.stdout.splitlines():
        if line.startswith(f"package:{AMAZON_PACKAGE} "):
            found = re.search(r"\binstaller=([^\s]+)", line)
            return found.group(1) if found else None
    return None


def probe(phone: CloudPhone) -> dict:
    require_online(phone)
    amazon = package_path(phone, AMAZON_PACKAGE)
    return {
        "serial": phone.serial,
        "android_serial": prop(phone, "ro.serialno"),
        "model": prop(phone, "ro.product.model"),
        "android_version": prop(phone, "ro.build.version.release"),
        "boot_completed": prop(phone, "sys.boot_completed") == "1",
        "play_store_installed": package_path(phone, PLAY_PACKAGE) is not None,
        "play_services_installed": package_path(phone, PLAY_SERVICES_PACKAGE) is not None,
        "amazon_package_installed": amazon is not None,
        "reported_installer": reported_installer(phone) if amazon else None,
        "source_verified": False,  # Installer metadata alone cannot prove APK provenance.
    }


def scan() -> dict:
    serials = cloud_serials()
    phones = []
    for serial, state in sorted(serials.items()):
        if state == "device":
            try:
                phones.append(probe(CloudPhone(serial)))
            except ToolError as exc:
                phones.append({"serial": serial, "adb_state": state, "error": str(exc)})
        else:
            phones.append({"serial": serial, "adb_state": state})
    return {"provider": "Swarmote local ADB tunnel", "phones": phones,
            "hint": "Mở Terminal > ADB Shell trong Profile Swarmote nếu danh sách trống"}


def open_amazon(phone: CloudPhone) -> dict:
    state = probe(phone)
    if not state["boot_completed"]:
        raise ToolError("Điện thoại đám mây chưa boot xong")
    if not state["amazon_package_installed"]:
        raise ToolError("Android Package Manager chưa thấy Amazon Shopping")

    def foreground() -> tuple[bool, bool]:
        pid = cloud_adb(phone, "shell", "pidof", AMAZON_PACKAGE,
                        check=False).stdout.strip()
        if not pid:
            return False, False
        window = cloud_adb(phone, "shell", "dumpsys", "window",
                           check=False).stdout
        focus = [line for line in window.splitlines()
                 if "mCurrentFocus=" in line or "mFocusedApp=" in line]
        return True, any(AMAZON_PACKAGE in line for line in focus)

    running, focused = foreground()
    if running and focused:
        return {**state, "amazon_running": True, "amazon_foreground": True}

    for attempt in range(2):
        launched = cloud_adb(phone, "shell", "monkey", "-p", AMAZON_PACKAGE,
                             "-c", "android.intent.category.LAUNCHER", "1")
        if "Events injected: 1" not in launched.stdout:
            raise ToolError("Không gửi được lệnh mở Amazon Shopping")
        for _ in range(8):
            time.sleep(1)
            running, focused = foreground()
            if running and focused:
                return {**state, "amazon_running": True, "amazon_foreground": True}
        if running:
            raise ToolError("Amazon Shopping đang chạy nhưng chưa lên màn hình trước; kiểm tra cửa sổ điện thoại")
        if attempt == 0:
            time.sleep(2)
    raise ToolError("Amazon Shopping không giữ được tiến trình sau 2 lần mở; kiểm tra app trên điện thoại")
