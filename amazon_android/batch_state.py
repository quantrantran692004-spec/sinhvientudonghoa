"""In-memory boundaries for one editable Swarmote batch."""
from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from .bulk_input import MAX_PROFILES
from .core import ToolError


@dataclass
class BatchDraft:
    batch_id: str = field(default_factory=lambda: uuid4().hex)
    proxy_count: int = 0
    account_count: int = 0
    locked: bool = False

    @property
    def count(self) -> int:
        # Show every pasted Amazon row even before its matching proxy is pasted.
        return self.account_count or max(1, min(self.proxy_count, MAX_PROFILES))

    def replace(self, kind: str, count: int) -> None:
        if self.locked:
            raise ToolError("Mẻ đã chạy; bấm Mẻ mới để nhập dữ liệu khác")
        limit = 100 if kind == "proxy" else MAX_PROFILES
        if not 1 <= count <= limit:
            raise ToolError("Danh sách proxy tối đa 100 dòng" if kind == "proxy"
                            else "Thông tin tài khoản cần 1–12 hàng")
        if kind == "proxy":
            self.proxy_count = count
        elif kind == "account":
            self.account_count = count
        else:
            raise ValueError("Unknown batch column")

    def validate(self, count: int) -> None:
        if self.proxy_count < count:
            raise ToolError(f"Cần ít nhất {count} proxy; hiện có {self.proxy_count}")
        if self.account_count not in {0, count}:
            raise ToolError(f"Thông tin Amazon có {self.account_count} hàng, cần {count} hàng")

    def new(self) -> "BatchDraft":
        return BatchDraft()
