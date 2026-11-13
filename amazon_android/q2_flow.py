"""q2's three navigation steps; account creation reuses b4–b11."""
from __future__ import annotations

import random
import threading
import time

from .cloud import CloudPhone
from .core import ToolError
from .post_menu import AttemptDeadline, PostMenuStep
from .account_flow import (
    _at_or_after, _ensure_menu, _find_scrolling, _read_nodes, _tap,
    _unique, _wait_screen, build_common_steps, screen,
)
from .runner import RunJob


def _home_visible(nodes: list[dict[str, str]]) -> bool:
    if screen(nodes) == "MENU":
        return False
    return (any(node.get("text", "").strip().casefold() ==
                "sign in for the best experience" for node in nodes)
            or any(node.get("content-desc", "").startswith("Home Tab")
                   and node.get("selected") == "true" for node in nodes))


def build_q2_steps(phone: CloudPhone, on_otp, on_status=lambda _status: None
                   ) -> tuple[PostMenuStep, ...]:
    """Start at the Browse menu, visit Home, then return and tap Pets."""
    def home(job: RunJob, deadline: AttemptDeadline,
             stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "IDENTIFIER"):
            return
        if not _home_visible(nodes):
            if screen(nodes) != "MENU":
                raise ToolError("q2 chưa ở menu ba gạch để bấm biểu tượng nhà")
            _tap(phone, _unique(nodes, "Home Tab", starts=True), deadline)
            until = time.monotonic() + deadline.allowance(6)
            while time.monotonic() < until:
                if _home_visible(_read_nodes(phone, deadline, stop)):
                    break
                stop.wait(0.3)
            else:
                raise ToolError("q2 chưa xác nhận trang chủ sau khi bấm biểu tượng nhà")
        stop.wait(deadline.allowance(random.choice((2, 3, 4, 5))))
        deadline.remaining()

    def browse_menu(job: RunJob, deadline: AttemptDeadline,
                    stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "IDENTIFIER") or screen(nodes) == "MENU":
            return
        if not _home_visible(nodes):
            raise ToolError("q2 chưa ở trang chủ để mở menu ba gạch")
        _tap(phone, _unique(nodes, "Browse menu Tab", starts=True), deadline)
        _wait_screen(phone, {"MENU"}, deadline, stop, seconds=6)

    def pets(job: RunJob, deadline: AttemptDeadline,
             stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "IDENTIFIER"):
            return
        _ensure_menu(phone, deadline, stop)
        _tap(phone, _find_scrolling(phone, "Pets", deadline, stop), deadline)
        stop.wait(0.4)

    return (
        PostMenuStep("b1 Trang chủ 2–5 giây", home),
        PostMenuStep("b2 Menu ba gạch", browse_menu),
        PostMenuStep("b3 Pets", pets),
    ) + build_common_steps(phone, on_otp, on_status)
