"""Explicitly confirmed installer for Google's Android command-line SDK packages."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from .core import IMAGE_ID, ToolError, executable, installed_image, sdk_root


REPOSITORY_URL = "https://dl.google.com/android/repository/repository2-1.xml"
DOWNLOAD_BASE = "https://dl.google.com/android/repository/"
PACKAGES = ("platform-tools", "emulator", "platforms/android-35",
            "system-images/android-35/google_apis_playstore/x86_64")


def official_commandline_archive() -> tuple[str, str, int]:
    with urllib.request.urlopen(REPOSITORY_URL, timeout=30) as response:
        xml = response.read()
    root = ET.fromstring(xml)
    for package in root.iter():
        if package.tag.endswith("remotePackage") and package.get("path") == "cmdline-tools;latest":
            for archive in package.iter():
                if not archive.tag.endswith("archive"):
                    continue
                host = next((x.text for x in archive if x.tag.endswith("host-os")), None)
                if host != "windows":
                    continue
                data = {x.tag.rsplit("}", 1)[-1]: x.text for x in archive.iter()}
                url, checksum, size = data.get("url"), data.get("checksum"), data.get("size")
                if url and checksum and size:
                    return DOWNLOAD_BASE + url, checksum.lower(), int(size)
    raise ToolError("Google SDK repository chưa cung cấp Command-line Tools cho Windows")


def confirm(message: str) -> None:
    if not sys.stdin.isatty():
        raise ToolError("Trình cài đặt cần phiên terminal tương tác để xác nhận")
    print(message)
    if input("Nhập CAI DAT để tiếp tục: ").strip() != "CAI DAT":
        raise ToolError("Đã hủy theo yêu cầu người dùng")


def download_commandline_tools(root: Path) -> None:
    url, expected, size = official_commandline_archive()
    if size > 500 * 1024 * 1024:
        raise ToolError("Gói Command-line Tools lớn bất thường; dừng để kiểm tra")
    confirm(f"Tải Android Command-line Tools từ {url}\nDung lượng: {size // 1048576} MB\nCài vào: {root}")
    target = root / "cmdline-tools" / "latest"
    if target.exists():
        raise ToolError(f"Đích cài đã tồn tại: {target}; không ghi đè")
    root.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(root).free < size + 2 * 1024**3:
        raise ToolError("Ổ đĩa cần tối thiểu 2 GB trống ngoài dung lượng tải")
    with tempfile.TemporaryDirectory(dir=root) as temp_name:
        temp = Path(temp_name)
        archive_path = temp / "tools.zip"
        digest = hashlib.sha1() if len(expected) == 40 else hashlib.sha256()
        with urllib.request.urlopen(url, timeout=60) as response, archive_path.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
                digest.update(chunk)
        if digest.hexdigest().lower() != expected:
            raise ToolError("Checksum gói Google SDK không khớp; đã hủy cài đặt")
        with zipfile.ZipFile(archive_path) as zipped:
            for member in zipped.infolist():
                parts = Path(member.filename.replace("\\", "/")).parts
                if not parts or parts[0] != "cmdline-tools" or ".." in parts:
                    raise ToolError("Đường dẫn không hợp lệ trong gói Google SDK")
            zipped.extractall(temp / "unpacked")
        source = temp / "unpacked" / "cmdline-tools"
        if not (source / "bin" / "sdkmanager.bat").is_file():
            raise ToolError("Gói Google SDK thiếu sdkmanager.bat")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(target))


def setup_sdk() -> None:
    root = sdk_root()
    if not shutil.which("java"):
        raise ToolError("Cần Java trước khi chạy sdkmanager")
    manager = executable("sdkmanager")
    if not manager:
        download_commandline_tools(root)
        manager = executable("sdkmanager")
    if not manager:
        raise ToolError("Không tìm thấy sdkmanager sau khi cài Command-line Tools")
    confirm("Google SDK Manager sẽ hiển thị giấy phép và cài các gói:\n" +
            "\n".join(PACKAGES) + f"\nVị trí: {root}")
    android = root / "cmdline-tools" / "latest" / "bin" / "android.exe"
    if android.is_file():
        for package in PACKAGES:
            subprocess.run([str(android), f"--sdk={root}", "sdk", "install", package], check=True)
    else:
        # Older command-line tools still use semicolon package IDs.
        subprocess.run([str(manager), f"--sdk_root={root}", "--licenses"], check=True)
        legacy = ("platform-tools", "emulator", "platforms;android-35", IMAGE_ID)
        for package in legacy:
            subprocess.run([str(manager), f"--sdk_root={root}", package], check=True)
    if not all(executable(name) for name in ("adb", "emulator", "avdmanager")) or not installed_image():
        raise ToolError("SDK Manager đã thoát nhưng các gói bắt buộc chưa cài đủ")
