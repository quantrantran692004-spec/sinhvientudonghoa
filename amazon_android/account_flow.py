"""Shared Android UI recognition and Amazon registration steps b4–b11.

Every action reads the live Android hierarchy. Unknown or ambiguous screens
raise ToolError so the phone stays where it is for a manual fix.
"""
from __future__ import annotations

import math
import random
import re
import threading
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Callable

from .cloud import CloudPhone, cloud_adb
from .core import AMAZON_PACKAGE, ToolError
from .otp import wait_for_new_otp
from .post_menu import AttemptDeadline, PostMenuSession, PostMenuStep, type_characters
from .registration import BOUNDS, _field_for_label
from .runner import RunJob


UI_PATH = "/sdcard/amazon_tool_post_menu.xml"
SIZE = re.compile(r"(?:Physical|Override) size:\s*(\d+)x(\d+)")


def _text(node: dict[str, str]) -> str:
    value = node.get("text", "").strip() or node.get("content-desc", "")
    return " ".join(value.split()).casefold().rstrip(".")


def _has(nodes: list[dict[str, str]], label: str) -> bool:
    return any(_text(node) == label.casefold().rstrip(".") for node in nodes)


def screen(nodes: list[dict[str, str]]) -> str:
    """Classify only screenshot-supported screens; unknown means stop."""
    if _has(nodes, "Country/region code"):
        return "COUNTRY"
    if _has(nodes, "Verify mobile number") and _has(nodes, "Enter security code"):
        return "SMS"
    if _has(nodes, "Verify with WhatsApp") and _has(nodes, "Send code by SMS"):
        return "WHATSAPP"
    if _has(nodes, "Create account") and _has(nodes, "First and last name"):
        return "CREATE_FORM"
    if _has(nodes, "Looks like you are new to Amazon") and _has(
            nodes, "Proceed to create an account"):
        return "NEW_ACCOUNT"
    if _has(nodes, "Sign in or create account") and _has(
            nodes, "Enter mobile number or email"):
        return "IDENTIFIER"
    if (_has(nodes, "Shop by category") or
            (_has(nodes, "Sign In") and _has(nodes, "Customer Service"))):
        return "MENU"
    return "UNKNOWN"


def menu_layout(nodes: list[dict[str, str]]) -> str:
    """Classify a live Browse menu by its accessible content, not an image."""
    if screen(nodes) != "MENU":
        return "OTHER"
    labels = {_text(node) for node in nodes}
    cards = {"gifting", "pets", "fashion and beauty", "your stuff",
             "sports & outdoors", "books and reading", "office & professional"}
    list_items = {"books", "electronics", "home services", "see all",
                  "today's deals", "try prime"}
    if cards & labels:
        return "CARDS"
    if ({"sign in", "customer service"} <= labels and
            len(list_items & labels) >= 2):
        return "LIST"
    return "UNKNOWN"


def home_visible(nodes: list[dict[str, str]]) -> bool:
    if screen(nodes) == "MENU":
        return False
    return (_has(nodes, "Sign in for the best experience") or
            any(node.get("content-desc", "").startswith("Home Tab")
                and node.get("selected") == "true" for node in nodes))


def _read_nodes(phone: CloudPhone, deadline: AttemptDeadline,
                stop: threading.Event) -> list[dict[str, str]]:
    if stop.is_set():
        raise ToolError("Đã dừng máy này")
    timeout = max(1, math.ceil(min(6, deadline.remaining())))
    dumped = cloud_adb(phone, "shell", "uiautomator", "dump", UI_PATH,
                       timeout=timeout, check=False)
    if dumped.returncode and f"dumped to: {UI_PATH}" not in dumped.stdout:
        raise ToolError("Không đọc được cây giao diện Amazon")
    xml = cloud_adb(phone, "shell", "cat", UI_PATH, timeout=timeout,
                    check=False).stdout
    try:
        nodes = [node.attrib for node in ET.fromstring(xml).iter("node")
                 if node.attrib.get("package") == AMAZON_PACKAGE]
    except ET.ParseError as exc:
        raise ToolError("Cây giao diện Amazon chưa hợp lệ") from exc
    if not nodes:
        raise ToolError("Amazon không ở màn hình trước; giữ nguyên máy này")
    return nodes


def verify_menu_open(phone: CloudPhone, profile_name: str = "q1") -> None:
    """Read-only guard for attaching an already-running phone."""
    nodes = _read_nodes(phone, AttemptDeadline(10), threading.Event())
    if screen(nodes) != "MENU":
        raise ToolError(f"{profile_name} chưa ở menu ba gạch; mở đúng menu rồi thử lại")


def _bounds(node: dict[str, str]) -> tuple[int, int, int, int]:
    found = BOUNDS.fullmatch(node.get("bounds", ""))
    if not found:
        raise ToolError("Phần tử Amazon chưa có vùng bấm hợp lệ")
    x1, y1, x2, y2 = map(int, found.groups())
    if x2 <= x1 or y2 <= y1:
        raise ToolError("Vùng bấm Amazon không hợp lệ")
    return x1, y1, x2, y2


def _tap(phone: CloudPhone, node: dict[str, str], deadline: AttemptDeadline) -> None:
    x1, y1, x2, y2 = _bounds(node)
    cloud_adb(phone, "shell", "input", "tap", str((x1 + x2) // 2),
              str((y1 + y2) // 2),
              timeout=max(1, math.ceil(min(6, deadline.remaining()))))


def _unique(nodes: list[dict[str, str]], label: str,
            *, starts: bool = False) -> dict[str, str]:
    target = label.casefold()
    matches = [node for node in nodes if
               (_text(node).startswith(target) if starts else _text(node) == target)]
    # UI hierarchies sometimes repeat one visible label at identical bounds.
    distinct = {node.get("bounds", ""): node for node in matches}
    if len(distinct) != 1 or "" in distinct:
        raise ToolError(f"Không xác định được duy nhất '{label}' trên máy này")
    return next(iter(distinct.values()))


def _visible(node: dict[str, str]) -> bool:
    if node.get("visible-to-user") == "false" or node.get("enabled") == "false":
        return False
    try:
        _bounds(node)
    except ToolError:
        return False
    return True


def _button(nodes: list[dict[str, str]], label: str,
            *, below: dict[str, str] | None = None) -> dict[str, str]:
    """Select the visible action control, not a hidden duplicate label."""
    matches = [node for node in nodes if _text(node) == label.casefold()
               and _visible(node)]
    if below is not None:
        bottom = _bounds(below)[3]
        matches = [node for node in matches if _bounds(node)[1] >= bottom]
    for preferred in (
            [node for node in matches if node.get("clickable") == "true"
             and node.get("class") == "android.widget.Button"],
            [node for node in matches if node.get("clickable") == "true"],
            matches):
        distinct = {node["bounds"]: node for node in preferred}
        if len(distinct) == 1:
            return next(iter(distinct.values()))
        if len(distinct) > 1:
            break
    raise ToolError(f"Không xác định được duy nhất nút '{label}' trên máy này")


def _wait_screen(phone: CloudPhone, expected: set[str],
                 deadline: AttemptDeadline, stop: threading.Event,
                 *, seconds: float = 10) -> list[dict[str, str]]:
    until = time.monotonic() + deadline.allowance(seconds)
    while time.monotonic() < until:
        nodes = _read_nodes(phone, deadline, stop)
        if screen(nodes) in expected:
            return nodes
        stop.wait(min(0.4, max(0, until - time.monotonic())))
    raise ToolError("Amazon chưa hiện màn hình kế tiếp như ảnh hướng dẫn")


def visit_home(phone: CloudPhone, deadline: AttemptDeadline,
               stop: threading.Event) -> None:
    """Open Home by its accessible tab and view it for 2–5 seconds."""
    nodes = _read_nodes(phone, deadline, stop)
    if not home_visible(nodes):
        if screen(nodes) != "MENU":
            raise ToolError("Amazon chưa ở menu để mở Trang chủ")
        home = _unique([node for node in nodes if _visible(node)],
                       "Home Tab", starts=True)
        _tap(phone, home, deadline)
        until = time.monotonic() + deadline.allowance(6)
        while time.monotonic() < until:
            if home_visible(_read_nodes(phone, deadline, stop)):
                break
            stop.wait(min(0.3, max(0, until - time.monotonic())))
        else:
            raise ToolError("Amazon chưa xác nhận Trang chủ sau khi bấm biểu tượng nhà")
    stop.wait(deadline.allowance(random.choice((2, 3, 4, 5))))
    deadline.remaining()


def route_list_menu(phone: CloudPhone, steps: tuple[PostMenuStep, ...],
                    current: int, session: PostMenuSession,
                    deadline: AttemptDeadline,
                    stop: threading.Event) -> int | None:
    """On a list menu, visit Home once and continue at shared b4."""
    matches = [index for index, step in enumerate(steps)
               if step.name == "b4 Sign In"]
    if len(matches) != 1 or current >= matches[0]:
        return None
    nodes = _read_nodes(phone, deadline, stop)
    layout = menu_layout(nodes)
    if layout == "LIST":
        session.menu_route = "LIST"
    elif layout == "CARDS":
        session.menu_route = ""
    if session.menu_route != "LIST" or screen(nodes) in {
            "IDENTIFIER", "NEW_ACCOUNT", "CREATE_FORM", "WHATSAPP", "SMS"}:
        return None
    visit_home(phone, deadline, stop)
    return matches[0]


def _scroll_up(phone: CloudPhone, nodes: list[dict[str, str]],
               deadline: AttemptDeadline) -> None:
    dimensions = []
    for node in nodes:
        try:
            _, _, x2, y2 = _bounds(node)
            dimensions.append((x2, y2))
        except ToolError:
            pass
    if dimensions:
        width = max(item[0] for item in dimensions)
        height = max(item[1] for item in dimensions)
    else:
        output = cloud_adb(phone, "shell", "wm", "size", timeout=3).stdout
        found = SIZE.search(output)
        if not found:
            raise ToolError("Không xác định được kích thước màn hình máy này")
        width, height = map(int, found.groups())
    cloud_adb(phone, "shell", "input", "swipe", str(width // 2),
              str(int(height * 0.72)), str(width // 2),
              str(int(height * 0.32)), "360",
              timeout=max(1, math.ceil(min(6, deadline.remaining()))))


def _find_scrolling(phone: CloudPhone, label: str,
                    deadline: AttemptDeadline, stop: threading.Event,
                    *, starts: bool = False,
                    menu_action: bool = False) -> dict[str, str]:
    previous = None
    for _ in range(30):
        nodes = _read_nodes(phone, deadline, stop)
        target = label.casefold()
        matches = [node for node in nodes if _visible(node) and
                   (_text(node).startswith(target) if starts else _text(node) == target)]
        if matches:
            if menu_action:
                try:
                    return _button(matches, label)
                except ToolError:
                    # The menu can expose both its row and a duplicate label.
                    # Customer Service sits immediately before Sign In in both
                    # observed layouts; use that live landmark if it is unique.
                    anchors = [node for node in nodes if _visible(node)
                               and _text(node) == "customer service"]
                    if len({node["bounds"] for node in anchors}) == 1:
                        return _button(matches, label, below=anchors[0])
                    raise
            return _unique(matches, label, starts=starts)
        visible = tuple(_text(node) for node in nodes if _visible(node) and _text(node))
        if visible == previous:
            break
        previous = visible
        _scroll_up(phone, nodes, deadline)
        stop.wait(0.35)
    raise ToolError(f"Không tìm thấy '{label}' sau khi cuộn máy này")


def _ensure_menu(phone: CloudPhone, deadline: AttemptDeadline,
                 stop: threading.Event) -> list[dict[str, str]]:
    nodes = _read_nodes(phone, deadline, stop)
    if screen(nodes) == "MENU":
        return nodes
    browse = [node for node in nodes if node.get("content-desc", "").startswith(
        "Browse menu Tab")]
    if len(browse) == 1:
        _tap(phone, browse[0], deadline)
    elif not browse:
        # A category card may have opened a page. Return once, then recheck.
        cloud_adb(phone, "shell", "input", "keyevent", "4",
                  timeout=max(1, math.ceil(min(6, deadline.remaining()))))
    else:
        raise ToolError("Có nhiều nút Browse menu; dừng máy này để kiểm tra")
    return _wait_screen(phone, {"MENU"}, deadline, stop, seconds=6)


def _field(nodes: list[dict[str, str]], label: str) -> dict[str, str]:
    try:
        return _field_for_label(nodes, (label,))
    except ToolError:
        fields = [node for node in nodes
                  if node.get("class") == "android.widget.EditText"]
        if len(fields) == 1:
            return fields[0]
    raise ToolError(f"Không xác định được ô '{label}' của máy này")


def _type_field(phone: CloudPhone, label: str, value: str,
                deadline: AttemptDeadline, stop: threading.Event) -> None:
    nodes = _read_nodes(phone, deadline, stop)
    field = _field(nodes, label)
    current = field.get("text", "")
    if current == value:
        return
    if current and not value.startswith(current):
        raise ToolError(f"Ô '{label}' khác dữ liệu của máy này; sửa trực tiếp rồi Tiếp tục")
    _tap(phone, field, deadline)
    type_characters(phone, value[len(current):], deadline, stop)
    updated = _field(_read_nodes(phone, deadline, stop), label)
    if updated.get("text", "") != value:
        raise ToolError(f"Chưa xác nhận được nội dung ô '{label}'")


def _at_or_after(nodes: list[dict[str, str]], kind: str) -> bool:
    order = {"MENU": 0, "IDENTIFIER": 1, "NEW_ACCOUNT": 2,
             "CREATE_FORM": 3, "WHATSAPP": 4, "SMS": 5}
    return screen(nodes) in order and order[screen(nodes)] >= order[kind]


def _national_phone(job: RunJob) -> str:
    if job.account is None:
        raise ToolError("Máy này chưa có thông tin Amazon")
    digits = re.sub(r"\D", "", job.account.phone)
    if len(digits) == 11 and digits.startswith("1"):
        return digits[1:]
    if len(digits) == 10:
        return digits
    raise ToolError("SĐT máy này cần 10 số US hoặc 1 + 10 số")


def _check_summary(nodes: list[dict[str, str]], job: RunJob) -> None:
    digits_on_screen = "".join(re.findall(r"\d", " ".join(
        node.get("text", "") for node in nodes)))
    if _national_phone(job) not in digits_on_screen:
        raise ToolError("SĐT trên Amazon không khớp hàng của máy này")


def resume_common_index(phone: CloudPhone, steps: tuple[PostMenuStep, ...],
                        current: int, deadline: AttemptDeadline,
                        stop: threading.Event) -> int:
    """Rewind a paused phone to its observed shared screen, never skip ahead."""
    if current >= len(steps) - 1:  # A prior Create tap must never be repeated.
        return current
    target_name = {
        "MENU": "b4 Sign In",
        "IDENTIFIER": "b4 Sign In",
        "COUNTRY": "b6 chọn US +1",
        "NEW_ACCOUNT": "b8 Proceed to create an account",
        "CREATE_FORM": "b9 nhập tên",
        "WHATSAPP": "b10 Send code by SMS",
        "SMS": "b10 Send code by SMS",
    }.get(screen(_read_nodes(phone, deadline, stop)))
    if target_name is None:
        return current
    matches = [index for index, step in enumerate(steps)
               if step.name == target_name]
    return min(current, matches[0]) if len(matches) == 1 else current


@dataclass
class _RegistrationState:
    sms_requested: bool = False
    code: str = ""
    create_pressed: bool = False


def build_common_steps(phone: CloudPhone,
                       on_otp: Callable[[str], None],
                       on_status: Callable[[str], None] = lambda _status: None,
                       ) -> tuple[PostMenuStep, ...]:
    """Build b4–b11 once for any machine, with OTP state local to this phone."""
    state = _RegistrationState()

    def sign_in(job: RunJob, deadline: AttemptDeadline,
                stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if screen(nodes) == "IDENTIFIER":
            _tap(phone, _field(nodes, "Enter mobile number or email"), deadline)
            return
        if _at_or_after(nodes, "NEW_ACCOUNT"):
            return
        _ensure_menu(phone, deadline, stop)
        _tap(phone, _find_scrolling(phone, "Sign In", deadline, stop,
                                    menu_action=True), deadline)
        nodes = _wait_screen(phone, {"IDENTIFIER"}, deadline, stop)
        _tap(phone, _field(nodes, "Enter mobile number or email"), deadline)

    def phone_number(job: RunJob, deadline: AttemptDeadline,
                     stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "NEW_ACCOUNT"):
            return
        if screen(nodes) != "IDENTIFIER" or job.account is None:
            raise ToolError("Máy này chưa ở form nhập số điện thoại")
        _national_phone(job)
        _type_field(phone, "Enter mobile number or email", job.account.phone,
                    deadline, stop)

    def country(job: RunJob, deadline: AttemptDeadline,
                stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "NEW_ACCOUNT"):
            return
        if screen(nodes) == "IDENTIFIER":
            if _has(nodes, "US +1"):
                return
            candidates = [node for node in nodes if _visible(node) and re.fullmatch(
                r"[a-z]{2}\s*\+\d+", _text(node))]
            if len(candidates) != 1:
                raise ToolError("Không xác định được ô chọn mã quốc gia")
            _tap(phone, candidates[0], deadline)
            nodes = _wait_screen(phone, {"COUNTRY"}, deadline, stop)
        if screen(nodes) != "COUNTRY":
            raise ToolError("Máy này chưa ở danh sách mã quốc gia")
        _tap(phone, _find_scrolling(phone, "United States +1", deadline, stop,
                                    starts=True), deadline)
        nodes = _wait_screen(phone, {"IDENTIFIER"}, deadline, stop)
        if not _has(nodes, "US +1"):
            raise ToolError("Amazon chưa xác nhận mã US +1")

    def continue_number(job: RunJob, deadline: AttemptDeadline,
                        stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "NEW_ACCOUNT"):
            return
        if screen(nodes) != "IDENTIFIER" or not _has(nodes, "US +1"):
            raise ToolError("Máy này chưa xác nhận số điện thoại US +1")
        _check_summary(nodes, job)
        _tap(phone, _button(nodes, "Continue"), deadline)
        _wait_screen(phone, {"NEW_ACCOUNT", "CREATE_FORM"}, deadline, stop)

    def proceed(job: RunJob, deadline: AttemptDeadline,
                stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "CREATE_FORM"):
            return
        if screen(nodes) != "NEW_ACCOUNT":
            raise ToolError("Máy này chưa ở màn tạo tài khoản mới")
        _check_summary(nodes, job)
        _tap(phone, _unique(nodes, "Proceed to create an account"), deadline)
        _wait_screen(phone, {"CREATE_FORM"}, deadline, stop)

    def name(job: RunJob, deadline: AttemptDeadline,
             stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "WHATSAPP"):
            return
        if screen(nodes) != "CREATE_FORM" or job.account is None:
            raise ToolError("Máy này chưa ở form nhập tên")
        _check_summary(nodes, job)
        _type_field(phone, "First and last name", job.account.full_name,
                    deadline, stop)
        nodes = _read_nodes(phone, deadline, stop)
        _tap(phone, _button(nodes, "Continue",
                            below=_field(nodes, "First and last name")), deadline)
        _wait_screen(phone, {"WHATSAPP", "SMS"}, deadline, stop)

    def send_sms(job: RunJob, deadline: AttemptDeadline,
                 stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if screen(nodes) == "SMS":
            state.sms_requested = True
            on_status("Đang chờ mã")
            return
        if state.sms_requested:
            raise ToolError("Đã bấm gửi SMS nhưng chưa xác nhận màn nhập mã; kiểm tra máy này")
        if screen(nodes) != "WHATSAPP" or job.account is None:
            raise ToolError("Máy này chưa ở màn chọn gửi mã bằng SMS")
        _check_summary(nodes, job)
        _tap(phone, _unique(nodes, "Send code by SMS"), deadline)
        state.sms_requested = True
        on_status("Đang chờ mã")
        _wait_screen(phone, {"SMS"}, deadline, stop)

    def enter_otp(job: RunJob, deadline: AttemptDeadline,
                  stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if screen(nodes) != "SMS" or job.account is None:
            raise ToolError("Máy này chưa ở màn nhập mã SMS")
        current = _field(nodes, "Enter security code").get("text", "")
        if re.fullmatch(r"[0-9]{6}", current):
            state.code = current
            on_otp(current)
            on_status("Đã nhập mã")
            return
        if not state.sms_requested:
            raise ToolError("Chưa xác nhận được lần gửi SMS; sửa mã trên máy rồi Tiếp tục")
        code = state.code or wait_for_new_otp(
            job.account.otp_url, None,
            timeout=deadline.allowance(30), stop=stop)
        _type_field(phone, "Enter security code", code, deadline, stop)
        state.code = code
        on_otp(code)
        on_status("Đã nhập mã")

    def create_account(job: RunJob, deadline: AttemptDeadline,
                       stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if screen(nodes) != "SMS" and state.create_pressed:
            return
        if screen(nodes) != "SMS":
            raise ToolError("Máy này không còn ở màn SMS; kiểm tra trước khi tạo tài khoản")
        value = _field(nodes, "Enter security code").get("text", "")
        if not re.fullmatch(r"[0-9]{6}", value):
            raise ToolError("Máy này chưa nhập đủ OTP để tạo tài khoản")
        if not state.create_pressed:
            _tap(phone, _unique(nodes, "Create your Amazon account"), deadline)
            state.create_pressed = True
        until = time.monotonic() + deadline.allowance(10)
        while time.monotonic() < until:
            if screen(_read_nodes(phone, deadline, stop)) != "SMS":
                return  # A later screenshot is needed to classify the result.
            stop.wait(0.5)
        raise ToolError("Đã bấm Create nhưng Amazon vẫn ở màn OTP; kiểm tra máy này")

    return (
        PostMenuStep("b4 Sign In", sign_in),
        PostMenuStep("b5 nhập SĐT", phone_number),
        PostMenuStep("b6 chọn US +1", country),
        PostMenuStep("b7 Continue", continue_number),
        PostMenuStep("b8 Proceed to create an account", proceed),
        PostMenuStep("b9 nhập tên", name),
        PostMenuStep("b10 Send code by SMS", send_sms),
        PostMenuStep("b11 nhập OTP", enter_otp),
        PostMenuStep("b11 bấm Create your Amazon account", create_account,
                     within_attempt=False),
    )
