"""q2's three navigation steps; account creation reuses b4–b11."""
from __future__ import annotations

import threading

from .cloud import CloudPhone
from .core import ToolError
from .post_menu import AttemptDeadline, PostMenuStep
from .account_flow import (
    _at_or_after, _ensure_menu, _find_scrolling, _read_nodes, _tap,
    _unique, _wait_screen, build_common_steps, home_visible, screen,
    visit_home,
)
from .runner import RunJob


def build_q2_steps(phone: CloudPhone, on_otp, on_status=lambda _status: None
                   ) -> tuple[PostMenuStep, ...]:
    """Start at the Browse menu, visit Home, then return and tap Pets."""
    def home(job: RunJob, deadline: AttemptDeadline,
             stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "IDENTIFIER"):
            return
        visit_home(phone, deadline, stop)

    def browse_menu(job: RunJob, deadline: AttemptDeadline,
                    stop: threading.Event) -> None:
        nodes = _read_nodes(phone, deadline, stop)
        if _at_or_after(nodes, "IDENTIFIER") or screen(nodes) == "MENU":
            return
        if not home_visible(nodes):
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
