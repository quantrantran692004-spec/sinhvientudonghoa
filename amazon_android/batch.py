"""One-run provisioning of five independent Swarmote phones.

The batch currently stops at Amazon's registration identifier screen.
Credentials are supplied in memory and are never persisted here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .core import ToolError
from .swarmote_desktop import ProxyConfig, create_profile, ready_for_registration


@dataclass(frozen=True)
class BatchItem:
    profile_name: str
    proxy: ProxyConfig


def parse_proxy_line(line: str) -> ProxyConfig:
    parts = line.strip().split(":", 3)
    if len(parts) != 4:
        raise ToolError("Proxy cần dạng host:port:username:password")
    host, port, username, password = parts
    if not username or not password:
        raise ToolError("Proxy trong mẻ cần username và password")
    try:
        number = int(port)
    except ValueError as exc:
        raise ToolError("Port proxy phải là số") from exc
    return ProxyConfig("socks5", host, number, username, password)


def prepare_five(items: list[BatchItem], progress: Callable[[int, str, str], None]) -> list[dict]:
    """Create all five Profiles first, then prepare Amazon on each phone.

    A failed item is reported and never retried automatically. This is important
    because Swarmote may complete a cloud create after a local timeout.
    """
    if len(items) != 5:
        raise ToolError("Mỗi mẻ cần đúng 5 cấu hình")
    names = [x.profile_name.strip() for x in items]
    if any(not x for x in names) or len(set(names)) != 5:
        raise ToolError("5 tên Profile phải khác nhau và không để trống")
    results = [{"profile_name": name, "stage": "PENDING"} for name in names]
    created: list[int] = []
    for i, item in enumerate(items):
        progress(i, "CREATING_PROFILE", "Đang tạo Profile và gán proxy")
        try:
            create_profile(item.profile_name, item.proxy)
        except ToolError as exc:
            results[i] = {"profile_name": names[i], "stage": "ERROR", "error": str(exc)}
            progress(i, "ERROR", str(exc))
        else:
            created.append(i)
            results[i] = {"profile_name": names[i], "stage": "PROFILE_CREATED"}
            progress(i, "PROFILE_CREATED", "Đã tạo Profile")
    for i in created:
        progress(i, "PREPARING_AMAZON", "Đang mở máy, cài Amazon và tới màn đăng ký")
        try:
            detail = ready_for_registration(names[i])
        except ToolError as exc:
            results[i] = {"profile_name": names[i], "stage": "ERROR", "error": str(exc)}
            progress(i, "ERROR", str(exc))
        else:
            results[i] = {"profile_name": names[i], "stage": "REGISTRATION_ENTRY",
                          "device_id": detail["profile"]["device_id"]}
            progress(i, "REGISTRATION_ENTRY", "Đã tới ô email/số điện thoại")
    return results
