"""Pure parsing for indexed bulk paste; no secrets are written or logged."""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field

from .batch import parse_proxy_line
from .core import ToolError
from .otp import otp_token, validate_otp_url
from .registration import PHONE
from .swarmote_desktop import ProxyConfig

MAX_PROFILES = 12
MAX_PROXY_CANDIDATES = 100
MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CARD = re.compile(r"(\d{12,19})\|(\d{1,2})\|(\d{2,4})")


def _table_cells(line: str) -> list[str]:
    """Split Markdown columns without treating escaped pipes as separators."""
    if line.startswith("|") and line.endswith("|"):
        body = line[1:-1]
        return [cell.strip().replace(r"\|", "|")
                for cell in re.split(r"(?<!\\)\|", body)]
    if "\t" in line:
        return [cell.strip() for cell in line.split("\t")]
    return [cell.strip() for cell in next(csv.reader([line]))]


def _url_from_cell(cell: str) -> str:
    """Use the actual Markdown link target, if the cell contains a link."""
    match = MARKDOWN_LINK.fullmatch(cell)
    if match:
        label, url = match.groups()
        if label.startswith(("http://", "https://")) and label != url:
            raise ToolError("Chữ và đích của link URL OTP không khớp")
        return url
    return cell


def validate_card(raw: str) -> str:
    """Keep the user's card reference in memory without echoing its value."""
    card = raw.strip()
    match = CARD.fullmatch(card)
    if not match or not 1 <= int(match.group(2)) <= 12:
        raise ToolError("Thẻ cần dạng số thẻ|tháng|năm")
    return card

@dataclass(frozen=True)
class BulkRecord:
    profile_name: str
    phone: str
    full_name: str
    password: str = field(repr=False)
    proxy: ProxyConfig | None = field(default=None, repr=False)
    otp_url: str = field(default="", repr=False)
    card: str = field(default="", repr=False)


def parse_records(text: str, *, three_columns_only: bool = False,
                  account_table: bool = False) -> list[BulkRecord]:
    """Read 1–12 Markdown, tab or CSV rows, including the desktop OTP format."""
    if three_columns_only and account_table:
        raise ValueError("Choose one account table format")
    raw_rows = [line.strip() for line in text.splitlines() if line.strip()]
    rows = []
    for line in raw_rows:
        cells = _table_cells(line)
        if cells and all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        if cells and cells[0].casefold() in {"profile", "profile name", "tên profile", "sđt", "số điện thoại", "phone"}:
            continue
        rows.append(cells)
    if not 1 <= len(rows) <= MAX_PROFILES:
        raise ToolError("Bảng cần 1–12 dòng dữ liệu")
    result = []
    for index, cells in enumerate(rows, 1):
        if three_columns_only and len(cells) != 3:
            raise ToolError(f"Bảng dòng {index}: dán đúng 3 cột SĐT | Mật khẩu | Tên")
        if account_table and len(cells) < 4:
            raise ToolError(f"Bảng dòng {index}: cần ít nhất 4 cột SĐT | Mật khẩu | Tên | URL OTP")
        otp_url = ""
        card = ""
        if account_table:
            profile = f"q{index}"
            phone, password, name = cells[:3]
            try:
                url_cells = [_url_from_cell(cell) for cell in cells[3:] if cell]
            except ToolError as exc:
                raise ToolError(f"Bảng dòng {index}: {exc}") from exc
            urls = [cell for cell in url_cells
                    if cell.startswith(("http://", "https://"))]
            if len(urls) != 1:
                raise ToolError(f"Bảng dòng {index}: cần đúng 1 URL OTP trong hàng")
            otp_url = urls[0]
            other = [cell for cell in url_cells if cell not in urls]
            if other:
                # Markdown exports may escape the two pipes or leave them raw.
                raw_card = other[0] if len(other) == 1 else "|".join(other)
                try:
                    card = validate_card(raw_card)
                except ToolError as exc:
                    raise ToolError(f"Bảng dòng {index}: {exc}") from exc
        elif len(cells) == 3:
            profile = f"q{index}"
            phone, password, name = cells
        elif len(cells) in {4, 5}:
            profile, phone, password, name = cells[:4]
        else:
            raise ToolError(f"Bảng dòng {index}: cần SĐT | Mật khẩu | Tên")
        if not profile or len(profile) > 80:
            raise ToolError(f"Bảng dòng {index}: tên Profile không hợp lệ")
        if not PHONE.fullmatch(phone):
            raise ToolError(f"Bảng dòng {index}: số điện thoại không hợp lệ")
        if len(password) < 8 or any(ord(c) < 33 or ord(c) > 126 for c in password):
            raise ToolError(f"Bảng dòng {index}: mật khẩu cần ít nhất 8 ký tự ASCII, không có dấu cách")
        if not name or len(name) > 100:
            raise ToolError(f"Bảng dòng {index}: tên Amazon không hợp lệ")
        if account_table:
            try:
                otp_url = validate_otp_url(otp_url)
            except ToolError as exc:
                raise ToolError(f"Bảng dòng {index}: {exc}") from exc
        try:
            proxy = (parse_proxy_line(cells[4])
                     if not account_table and len(cells) == 5 and cells[4] else None)
        except ToolError as exc:
            raise ToolError(f"Bảng dòng {index}: {exc}") from exc
        result.append(BulkRecord(profile, phone, name, password, proxy, otp_url, card))
    if len({item.profile_name.casefold() for item in result}) != len(result):
        raise ToolError("Bảng có tên Profile trùng nhau")
    tokens = [otp_token(item.otp_url) for item in result if item.otp_url]
    if len(tokens) != len(set(tokens)):
        raise ToolError("Bảng có URL OTP trùng nhau giữa các máy")
    return result


def lines(text: str, label: str) -> list[str]:
    rows = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    while rows and rows[-1] == "":
        rows.pop()
    if not rows:
        raise ToolError(f"Danh sách {label} đang trống")
    limit = MAX_PROXY_CANDIDATES if label == "proxy" else MAX_PROFILES
    if len(rows) > limit:
        raise ToolError(f"Danh sách {label} có {len(rows)} dòng; giới hạn là {limit}")
    for index, row in enumerate(rows, 1):
        if not row.strip():
            raise ToolError(f"Danh sách {label}: dòng {index} đang trống")
    return rows


def parse_column(kind: str, text: str) -> list:
    label = {"proxy": "proxy", "name": "tên", "phone": "số điện thoại",
             "password": "mật khẩu"}.get(kind)
    if label is None:
        raise ValueError("Unknown column")
    rows = lines(text, label)
    if kind == "proxy":
        parsed = []
        for index, row in enumerate(rows, 1):
            try:
                parsed.append(parse_proxy_line(row.strip()))
            except ToolError as exc:
                raise ToolError(f"Proxy dòng {index}: {exc}") from exc
        return parsed
    if kind == "phone":
        for index, row in enumerate(rows, 1):
            if not PHONE.fullmatch(row.strip()):
                raise ToolError(f"Số điện thoại dòng {index} sai định dạng")
        return [row.strip() for row in rows]
    if kind == "name":
        return [row.strip() for row in rows]
    # Password whitespace is preserved intentionally; no echo of its value.
    return rows
