"""Per-phone workflow control after Amazon's Browse menu is open.

The Amazon screen steps are intentionally supplied later. Every step must
inspect the current UI before acting so a manual fix can be resumed safely.
"""
from __future__ import annotations

import math
import shlex
import threading
import time
from dataclasses import dataclass, field
from typing import Callable

from .cloud import CloudPhone, cloud_adb
from .core import ToolError
from .runner import RunJob


_MINUTES = (3, 4, 5, 4)


def attempt_seconds(attempt: int) -> int:
    """Independent 3 → 4 → 5 → 4 → 3 minute cycle for each phone."""
    if attempt < 1:
        raise ValueError("Attempt number starts at one")
    return _MINUTES[(attempt - 1) % len(_MINUTES)] * 60


@dataclass(frozen=True)
class AttemptDeadline:
    seconds: int
    started: float = field(default_factory=time.monotonic)

    def remaining(self) -> float:
        left = self.started + self.seconds - time.monotonic()
        if left <= 0:
            raise ToolError("Hết thời gian của lượt tự động hóa")
        return left

    def allowance(self, requested: float) -> float:
        """Give a wait only the time still available in this attempt."""
        if requested <= 0:
            raise ValueError("Requested wait must be positive")
        return min(requested, self.remaining())


StepAction = Callable[[RunJob, AttemptDeadline, threading.Event], None]
Progress = Callable[[int, str, str, str], None]


@dataclass(frozen=True)
class PostMenuStep:
    name: str
    action: StepAction
    within_attempt: bool = True


@dataclass
class PostMenuSession:
    batch_id: str
    index: int
    profile_name: str
    menu_opened_at: float | None = None
    next_step: int = 0
    attempts: int = 0
    state: str = "READY"
    last_error: str = ""
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def run(self, job: RunJob, steps: tuple[PostMenuStep, ...],
            emit: Progress, stop: threading.Event) -> None:
        """Run this phone only; errors pause at the same step for manual repair."""
        if not steps:
            raise ValueError("Post-menu steps have not been supplied")
        if (job.batch_id, job.index) != (self.batch_id, self.index):
            raise ValueError("Job does not belong to this phone session")
        with self._lock:
            if self.state not in {"READY", "PAUSED"}:
                return
            self.attempts += 1
            started = (self.menu_opened_at if self.attempts == 1
                       and self.menu_opened_at is not None else time.monotonic())
            deadline = AttemptDeadline(attempt_seconds(self.attempts), started)
            self.state = "RUNNING"
            self.last_error = ""
        emit(self.index,
             f"{self.profile_name} · lượt {self.attempts}, {deadline.seconds // 60} phút",
             "post_running", self.profile_name)
        while self.next_step < len(steps):
            step = steps[self.next_step]
            try:
                if stop.is_set():
                    raise ToolError("Đã dừng tự động hóa")
                if step.within_attempt:
                    deadline.remaining()
                action_deadline = deadline if step.within_attempt else AttemptDeadline(30)
                step.action(job, action_deadline, stop)
                if step.within_attempt:
                    deadline.remaining()
            except Exception as exc:
                reason = str(exc) if isinstance(exc, ToolError) else type(exc).__name__
                with self._lock:
                    self.state = "PAUSED"
                    self.last_error = f"{step.name}: {reason}"
                emit(self.index,
                     f"Dừng tại {step.name}: {reason} · sửa trên máy rồi bấm Tiếp tục",
                     "post_paused", self.profile_name)
                return
            with self._lock:
                self.next_step += 1
            emit(self.index, f"Đã xong {step.name} · {self.profile_name}",
                 "post_running", self.profile_name)
        with self._lock:
            self.state = "DONE"
        emit(self.index, f"Đã xong các bước đã hướng dẫn · {self.profile_name}",
             "post_done", self.profile_name)


def type_characters(phone: CloudPhone, value: str, deadline: AttemptDeadline,
                    stop: threading.Event) -> None:
    """Send one Android text key event per character; never use clipboard/paste."""
    if any(ord(char) < 32 or ord(char) > 126 for char in value):
        raise ToolError("Trường có ký tự Android chưa gõ được; sửa trực tiếp trên máy")
    for position, char in enumerate(value, 1):
        if stop.is_set():
            raise ToolError("Đã dừng khi đang gõ")
        remaining = deadline.remaining()
        token = "%s" if char == " " else char
        command = f"input text {shlex.quote(token)}\n"
        result = cloud_adb(phone, "shell", input_text=command,
                           timeout=max(1, math.ceil(min(remaining, 10))),
                           check=False)
        if result.returncode:
            raise ToolError(f"Android không gõ được ký tự thứ {position}")
