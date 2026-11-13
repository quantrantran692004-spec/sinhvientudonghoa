"""Persistent Profile identity metadata; never stores proxy or Amazon inputs."""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Callable

from .core import ToolError
from .swarmote_desktop import ProfileNotFound


def default_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home())))
    return base / "AmazonAndroidTool" / "profiles.json"


class ProfileRegistry:
    def __init__(self, path: Path | None = None, *, persistent: bool = True) -> None:
        self.path = path or default_path()
        self.persistent = persistent
        self._lock = threading.RLock()
        if not persistent:
            self.data = {"next_number": 1, "items": {}}
        elif self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
                if not isinstance(self.data.get("next_number"), int) or not isinstance(self.data.get("items"), dict):
                    raise ValueError("invalid registry")
            except (OSError, ValueError, TypeError) as exc:
                raise ToolError("Không đọc được danh sách Profile đã cấp; dừng để tránh trùng tên") from exc
        else:
            self.data = {"next_number": 1, "items": {}}

    def _save(self) -> None:
        if not self.persistent:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_name(f"{self.path.name}.{os.getpid()}.tmp")
        try:
            temp.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")
            os.replace(temp, self.path)
        finally:
            temp.unlink(missing_ok=True)

    def get(self, batch_id: str, slot: int) -> dict | None:
        with self._lock:
            item = self.data["items"].get(f"{batch_id}:{slot}")
            return dict(item) if item else None

    def items_for_batch(self, batch_id: str) -> list[dict]:
        with self._lock:
            return [dict(item) for item in self.data["items"].values()
                    if item.get("batch_id") == batch_id]

    def latest_resumable_batch(self) -> tuple[str, list[dict]] | None:
        """Resume only batches whose Profiles were already confirmed in Swarmote."""
        allowed = {"PROFILE_CONFIRMED", "STARTED", "APP_INSTALLED", "MENU_OPEN"}
        with self._lock:
            batch_ids = list(dict.fromkeys(
                item["batch_id"] for item in self.data["items"].values()))
            if not batch_ids:
                return None
            batch_id = batch_ids[-1]
            items = sorted((dict(item) for item in self.data["items"].values()
                            if item.get("batch_id") == batch_id),
                           key=lambda item: item["slot"])
            if not items or len(items) > 12:
                return None
            if [item["slot"] for item in items] != list(range(len(items))):
                return None
            if all(item.get("stage") == "MENU_OPEN" for item in items):
                return None
            if all(item.get("stage") in allowed and item.get("device_id")
                   for item in items):
                return batch_id, items
        return None

    def preview_names(self, count: int) -> list[str]:
        """The twelve positions always map to q1..q12 in a new batch."""
        return [f"q{slot}" for slot in range(1, count + 1)]

    def reserve(self, batch_id: str, slot: int, lookup: Callable[[str], dict]) -> dict:
        """Reserve an unused qN, skipping names already visible in Swarmote."""
        key = f"{batch_id}:{slot}"
        with self._lock:
            existing = self.data["items"].get(key)
            if existing:
                return dict(existing)
            name = f"q{slot + 1}"
            try:
                lookup(name)
            except ProfileNotFound:
                item = {"name": name, "batch_id": batch_id,
                        "slot": slot, "state": "READY", "stage": "RESERVED",
                        "device_id": None}
                self.data["items"][key] = item
                self._save()
                return dict(item)
            raise ToolError(f"{name} đã tồn tại trong Swarmote; không thể tạo trùng cho Máy {slot + 1}")

    def mark(self, batch_id: str, slot: int, state: str,
             device_id: str | None = None, stage: str | None = None,
             error: str | None = None) -> dict:
        key = f"{batch_id}:{slot}"
        with self._lock:
            if key not in self.data["items"]:
                raise ToolError("Profile chưa được cấp tên")
            item = self.data["items"][key]
            item["state"] = state
            if stage:
                item["stage"] = stage
            if device_id:
                item["device_id"] = device_id
            if error is not None:
                item["last_error"] = error[:240]
            elif state in {"READY", "DONE"}:
                item.pop("last_error", None)
            self._save()
            return dict(item)
