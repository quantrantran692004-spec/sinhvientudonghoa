"""q1-only navigation b1–b3 before the shared account flow."""
from __future__ import annotations

import threading
from typing import Callable

from .account_flow import (
    _at_or_after, _ensure_menu, _find_scrolling, _read_nodes, _tap,
    build_common_steps,
)
from .cloud import CloudPhone
from .post_menu import AttemptDeadline, PostMenuStep
from .runner import RunJob


def build_q1_steps(phone: CloudPhone,
                   on_otp: Callable[[str], None],
                   on_status: Callable[[str], None] = lambda _status: None,
                   ) -> tuple[PostMenuStep, ...]:
    """Supply q1's three category taps, then reuse the common registration."""
    def category(label: str):
        def action(job: RunJob, deadline: AttemptDeadline,
                   stop: threading.Event) -> None:
            nodes = _read_nodes(phone, deadline, stop)
            if _at_or_after(nodes, "IDENTIFIER"):
                return
            _ensure_menu(phone, deadline, stop)
            _tap(phone, _find_scrolling(phone, label, deadline, stop), deadline)
            stop.wait(0.4)
        return action

    return (
        PostMenuStep("b1 Gifting", category("Gifting")),
        PostMenuStep("b2 Pets", category("Pets")),
        PostMenuStep("b3 Fashion and Beauty", category("Fashion and Beauty")),
    ) + build_common_steps(phone, on_otp, on_status)
