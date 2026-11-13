"""Non-secret desktop preferences."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from .core import ToolError
from .profile_registry import default_path


@dataclass(frozen=True)
class AppSettings:
    start_group_size: int = 1
    hide_profile_creation: bool = False

    def __post_init__(self) -> None:
        if not 1 <= self.start_group_size <= 12:
            raise ToolError("Giới hạn máy Running trong mẻ phải từ 1 đến 12")
        if not isinstance(self.hide_profile_creation, bool):
            raise ToolError("Tùy chọn ẩn cửa sổ tạo Profile không hợp lệ")


def settings_path() -> Path:
    return default_path().with_name("settings.json")


def load_settings(path: Path | None = None) -> AppSettings:
    source = path or settings_path()
    if not source.exists():
        return AppSettings()
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
        return AppSettings(int(data["start_group_size"]),
                           data.get("hide_profile_creation", False))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise ToolError("Không đọc được Settings; kiểm tra settings.json") from exc


def save_settings(settings: AppSettings, path: Path | None = None) -> None:
    target = path or settings_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
    try:
        temp.write_text(json.dumps({
            "start_group_size": settings.start_group_size,
            "hide_profile_creation": settings.hide_profile_creation,
        }),
                        encoding="utf-8")
        os.replace(temp, target)
    finally:
        temp.unlink(missing_ok=True)
