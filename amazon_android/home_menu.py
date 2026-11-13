"""Deterministic Amazon navigation through the home browse menu."""
from __future__ import annotations

import re
import time
import xml.etree.ElementTree as ET

from .cloud import CloudPhone, cloud_adb, open_amazon
from .core import AMAZON_PACKAGE, ToolError
from .swarmote_desktop import install_amazon, open_adb_shell, show_apps, start_profile


BOUNDS = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")


def _nodes(phone: CloudPhone) -> list[dict[str, str]]:
    path = "/sdcard/amazon_tool_menu.xml"
    last_error = "Android chưa trả cây giao diện hợp lệ"
    for attempt in range(3):
        try:
            dumped = cloud_adb(phone, "shell", "uiautomator", "dump", path,
                               timeout=15, check=False)
            # Some Windows ADB invocations report an interrupted exit code after
            # Android has already written the dump. Accept only an explicit
            # success message for that case, then validate the XML itself.
            if dumped.returncode and f"dumped to: {path}" not in dumped.stdout:
                last_error = f"ADB dump trả mã {dumped.returncode}"
                if attempt < 2:
                    time.sleep(0.3)
                continue
            result = cloud_adb(phone, "shell", "cat", path, timeout=15, check=False)
            nodes = [node.attrib for node in ET.fromstring(result.stdout).iter("node")]
            if not any(node.get("package") == AMAZON_PACKAGE for node in nodes):
                last_error = "Màn hình trước chưa phải Amazon Shopping"
                if attempt < 2:
                    time.sleep(0.3)
                continue
            return nodes
        except (ToolError, ET.ParseError) as exc:
            last_error = str(exc) if isinstance(exc, ToolError) else "XML chưa hợp lệ"
        if attempt < 2:
            time.sleep(0.3)
    raise ToolError(f"Không đọc được giao diện Amazon sau 3 lần: {last_error}")


def _tap(phone: CloudPhone, node: dict[str, str]) -> None:
    match = BOUNDS.fullmatch(node.get("bounds", ""))
    if not match:
        raise ToolError("Không xác định được vị trí nút Amazon")
    x1, y1, x2, y2 = map(int, match.groups())
    cloud_adb(phone, "shell", "input", "tap",
              str((x1 + x2) // 2), str((y1 + y2) // 2))


def open_home_menu(phone: CloudPhone, timeout: int = 45) -> dict:
    """Reach Amazon's Browse menu, with no account data entered."""
    deadline = time.monotonic() + timeout
    backed_out = False
    skipped = False
    tapped_menu = False
    while time.monotonic() < deadline:
        nodes = _nodes(phone)
        labels = {node.get("text", "") for node in nodes}
        if ("Authentication required" in labels or
                "Verify mobile number" in labels or
                "Enter security code" in labels):
            raise ToolError("Amazon đang ở bước xác minh tài khoản; giữ nguyên màn hình để bạn tiếp tục")
        if any(label.strip().rstrip(".") == "Shop by category" for label in labels):
            return {"stage": "HOME_MENU_OPEN", "account_input_sent": False}
        menu = [node for node in nodes
                if node.get("content-desc", "").startswith("Browse menu Tab")]
        if len(menu) == 1 and not tapped_menu:
            _tap(phone, menu[0])
            tapped_menu = True
        elif "Skip sign in" in labels and not skipped:
            buttons = [node for node in nodes
                       if node.get("text") == "Skip sign in"
                       and node.get("class") == "android.widget.Button"]
            if len(buttons) != 1:
                raise ToolError("Không xác định được nút Skip sign in duy nhất")
            _tap(phone, buttons[0])
            skipped = True
        elif "Sign in or create account" in labels and not backed_out:
            cloud_adb(phone, "shell", "input", "keyevent", "4")
            backed_out = True
        time.sleep(1)
    raise ToolError("Amazon chưa hiện menu ba gạch; đã dừng tại màn hiện tại")


def ready_for_home_menu(name: str) -> dict:
    """Start, install and open Amazon, then stop at the home Browse menu."""
    profile = start_profile(name)
    installed = install_amazon(name)
    shell = open_adb_shell(name)
    show_apps(name, shell["device_id"])
    phone = CloudPhone(shell["serial"])
    open_amazon(phone)
    menu = open_home_menu(phone)
    return {"profile": profile, "amazon_package_installed":
            installed["amazon_package_installed"], **menu}
