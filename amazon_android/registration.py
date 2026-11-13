"""Amazon Shopping registration entry through the live Android UI hierarchy."""
from __future__ import annotations

import re
import shlex
import time
import xml.etree.ElementTree as ET

from .cloud import CloudPhone, cloud_adb, require_online
from .core import AMAZON_PACKAGE, ToolError


BOUNDS = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")
EMAIL = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE = re.compile(r"^\+?[0-9]{7,16}$")


def _nodes(phone: CloudPhone) -> list[dict[str, str]]:
    require_online(phone)
    cloud_adb(phone, "shell", "uiautomator", "dump", "/sdcard/amazon_tool_ui.xml", timeout=15)
    xml = cloud_adb(phone, "shell", "cat", "/sdcard/amazon_tool_ui.xml", timeout=15).stdout
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as exc:
        raise ToolError("Android chưa trả cây giao diện hợp lệ") from exc
    nodes = [n.attrib for n in root.iter("node")]
    if not nodes or not any(n.get("package") == AMAZON_PACKAGE for n in nodes):
        raise ToolError("Màn hình trước không phải Amazon Shopping")
    return nodes


def _wait_nodes(phone: CloudPhone, predicate, timeout: int = 20) -> list[dict[str, str]]:
    until = time.monotonic() + timeout
    while time.monotonic() < until:
        nodes = _nodes(phone)
        if predicate(nodes):
            return nodes
        time.sleep(1)
    raise ToolError("Amazon không hiện màn hình mong đợi; đã dừng để tránh bấm sai")


def _tap(phone: CloudPhone, node: dict[str, str]) -> None:
    match = BOUNDS.fullmatch(node.get("bounds", ""))
    if not match or node.get("clickable") != "true":
        raise ToolError("Phần tử không có vùng bấm Android hợp lệ")
    x1, y1, x2, y2 = map(int, match.groups())
    if x2 <= x1 or y2 <= y1:
        raise ToolError("Vùng bấm Android không hợp lệ")
    cloud_adb(phone, "shell", "input", "tap", str((x1 + x2) // 2), str((y1 + y2) // 2))


def status(phone: CloudPhone) -> dict:
    nodes = _nodes(phone)
    texts = {n.get("text", "") for n in nodes}
    entry = "Sign in or create account" in texts
    fields = [n for n in nodes if n.get("class") == "android.widget.EditText"]
    return {"serial": phone.serial, "registration_entry": entry,
            "identifier_field_found": entry and len(fields) == 1,
            "continue_found": entry and any(n.get("text") == "Continue" and n.get("clickable") == "true"
                                            for n in nodes)}


def open_entry(phone: CloudPhone) -> dict:
    nodes = _wait_nodes(phone, lambda ns: any(n.get("text") == "Sign in or create account" for n in ns)
                        or any(n.get("text", "").endswith("Create an account") and n.get("clickable") == "true"
                               for n in ns))
    if not any(n.get("text") == "Sign in or create account" for n in nodes):
        targets = [n for n in nodes if n.get("text", "").endswith("Create an account")
                   and n.get("class") == "android.widget.Button" and n.get("clickable") == "true"]
        if len(targets) != 1:
            raise ToolError("Không xác định được nút tạo tài khoản duy nhất")
        _tap(phone, targets[0])
    _wait_nodes(phone, lambda ns: any(n.get("text") == "Sign in or create account" for n in ns)
                and len([n for n in ns if n.get("class") == "android.widget.EditText"]) == 1)
    return status(phone)


def fill_identifier(phone: CloudPhone, identifier: str) -> dict:
    """Fill only; do not press Continue or submit account data."""
    if not (EMAIL.fullmatch(identifier) or PHONE.fullmatch(identifier)):
        raise ToolError("Cần email hoặc số điện thoại hợp lệ")
    nodes = _wait_nodes(phone, lambda ns: any(n.get("text") == "Sign in or create account" for n in ns)
                        and len([n for n in ns if n.get("class") == "android.widget.EditText"]) == 1)
    field = next(n for n in nodes if n.get("class") == "android.widget.EditText")
    _type_into(phone, field, identifier)
    current = _nodes(phone)
    values = [n.get("text", "") for n in current if n.get("class") == "android.widget.EditText"]
    if len(values) != 1 or values[0] != identifier:
        raise ToolError("Không xác nhận được nội dung trường email/số điện thoại; chưa bấm Continue")
    return {"serial": phone.serial, "identifier_filled": True, "continue_pressed": False}


def _unique_button(nodes: list[dict[str, str]], label: str) -> dict[str, str]:
    found = [n for n in nodes if n.get("class") == "android.widget.Button"
             and n.get("text", "").casefold() == label.casefold()
             and n.get("clickable") == "true"]
    if len(found) != 1:
        raise ToolError(f"Không xác định được nút '{label}' duy nhất")
    return found[0]


def _field_for_label(nodes: list[dict[str, str]], names: tuple[str, ...]) -> dict[str, str]:
    """Match a WebView EditText with its immediately preceding visible label."""
    labels = [n for n in nodes if n.get("class") == "android.widget.TextView"
              and any(n.get("text", "").strip().casefold() == name.casefold() for name in names)]
    fields = [n for n in nodes if n.get("class") == "android.widget.EditText"]
    matches = []
    for label in labels:
        lb = BOUNDS.fullmatch(label.get("bounds", ""))
        if not lb:
            continue
        lx1, ly1, lx2, ly2 = map(int, lb.groups())
        for field in fields:
            fb = BOUNDS.fullmatch(field.get("bounds", ""))
            if not fb:
                continue
            fx1, fy1, fx2, fy2 = map(int, fb.groups())
            if 0 <= fy1 - ly2 <= 130 and min(lx2, fx2) > max(lx1, fx1):
                matches.append((fy1 - ly2, field))
    matches.sort(key=lambda pair: pair[0])
    if not matches or (len(matches) > 1 and matches[0][0] == matches[1][0]):
        raise ToolError(f"Không nhận diện được trường {names[0]} theo cây Android")
    return matches[0][1]


def _type_into(phone: CloudPhone, field: dict[str, str], value: str) -> None:
    _tap(phone, field)
    # Android input text uses %s for a space. Each argument stays in a subprocess
    # array; no host shell interpolation or local credential log is used.
    command = f"input text {shlex.quote(value.replace(' ', '%s'))}\n"
    result = cloud_adb(phone, "shell", input_text=command, check=False)
    if result.returncode:
        raise ToolError("Android không nhập được dữ liệu vào trường đã chọn")


def fill_signup_form(phone: CloudPhone, full_name: str, phone_number: str,
                     password: str) -> dict:
    """Fill Amazon's name/password form, then stop before final submission.

    The identifier Continue step is needed to reach this form. If Amazon asks
    for verification or changes the page, stop without guessing controls.
    """
    if not full_name.strip() or len(full_name.strip()) > 100:
        raise ToolError("Tên người dùng không hợp lệ")
    if not PHONE.fullmatch(phone_number):
        raise ToolError("Số điện thoại cần 7–16 chữ số, có thể bắt đầu bằng +")
    if len(password) < 8 or any(ord(c) < 33 or ord(c) > 126 for c in password):
        raise ToolError("Mật khẩu cần ít nhất 8 ký tự ASCII in được, không có khoảng trắng")
    open_entry(phone)
    fill_identifier(phone, phone_number)
    _tap(phone, _unique_button(_nodes(phone), "Continue"))
    nodes = _wait_nodes(phone, lambda ns: any(n.get("text", "").strip().casefold()
                              in {"your name", "name", "full name", "password", "create account", "verify mobile number"}
                              for n in ns), timeout=30)
    texts = {n.get("text", "").strip().casefold() for n in nodes}
    if any("verify" in t or "captcha" in t or "otp" in t for t in texts):
        return {"serial": phone.serial, "stage": "USER_VERIFICATION_REQUIRED",
                "final_submit_pressed": False}
    name_field = _field_for_label(nodes, ("Your name", "Name", "Full name"))
    password_field = _field_for_label(nodes, ("Password", "Create password"))
    _type_into(phone, name_field, full_name.strip())
    # Refresh after a field edit because WebView bounds may shift.
    password_field = _field_for_label(_nodes(phone), ("Password", "Create password"))
    _type_into(phone, password_field, password)
    nodes = _nodes(phone)
    # Some Amazon versions request confirmation; fill only when a distinct
    # labeled field exists. Never press a create/verify button here.
    if any(n.get("text", "").strip().casefold() in {"re-enter password", "confirm password"}
           for n in nodes):
        confirm = _field_for_label(nodes, ("Re-enter password", "Confirm password"))
        _type_into(phone, confirm, password)
    return {"serial": phone.serial, "stage": "FORM_INPUT_SENT_REVIEW_REQUIRED",
            "final_submit_pressed": False}
