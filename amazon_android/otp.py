"""Read one profile's Amazon SMS code from its assigned APIFC URL.

The account flow reads this URL only after it has sent SMS and confirmed the
SMS entry screen. URLs and SMS bodies are never included in errors.
"""
from __future__ import annotations

import re
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .core import ToolError


CODE = re.compile(r"^yes\|Amazon:\s*(\d{6})\s+is your sign-in code\.", re.IGNORECASE)


def validate_otp_url(raw: str) -> str:
    """Accept only a tokenized HTTPS SMS-record endpoint."""
    url = raw.strip()
    if not url or len(url) > 2048 or any(char.isspace() for char in url):
        raise ToolError("URL OTP không hợp lệ")
    try:
        parts = urlsplit(url)
        tokens = parse_qs(parts.query, keep_blank_values=True).get("token", [])
        valid = (parts.scheme == "https" and parts.hostname == "apifc.net"
                 and parts.path == "/smsrecord" and parts.port is None
                 and not parts.username and not parts.password and not parts.fragment
                 and len(tokens) == 1 and bool(tokens[0]))
    except ValueError:
        valid = False
    if not valid:
        raise ToolError("URL OTP cần dạng https://apifc.net/smsrecord?token=...")
    return url


def otp_token(raw: str) -> str:
    """Return the identity of a validated URL for duplicate-row checks."""
    return parse_qs(urlsplit(validate_otp_url(raw)).query)["token"][0]


def extract_otp(body: str) -> str | None:
    """Extract only Amazon's sign-in code, never an unrelated digit sequence."""
    response = body.strip()
    match = CODE.match(response)
    if match:
        return match.group(1)
    if response.lower().startswith("yes|"):
        raise ToolError("Phản hồi OTP không đúng mẫu Amazon đã xác nhận")
    return None


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


_OPENER = build_opener(_NoRedirect)


def read_otp(url: str, *, timeout: float = 5) -> str | None:
    """GET the profile URL once and return its current code, if any."""
    url = validate_otp_url(url)
    request = Request(url, headers={"Accept": "text/plain"})
    try:
        with _OPENER.open(request, timeout=timeout) as response:
            payload = response.read(8193)
    except HTTPError as exc:
        raise ToolError(f"URL OTP trả HTTP {exc.code}") from None
    except (URLError, TimeoutError, OSError):
        raise ToolError("Không kết nối được URL OTP") from None
    if len(payload) > 8192:
        raise ToolError("Phản hồi OTP quá dài")
    return extract_otp(payload.decode("utf-8", errors="replace"))


def wait_for_new_otp(url: str, previous_code: str | None, *,
                     timeout: float = 30, interval: float = 1,
                     stop: threading.Event | None = None) -> str:
    """Poll one profile URL for a code after SMS was requested."""
    validate_otp_url(url)
    if timeout <= 0 or interval <= 0:
        raise ValueError("OTP timeout and interval must be positive")
    deadline = time.monotonic() + timeout
    stop = stop or threading.Event()
    last_http_403 = False
    while not stop.is_set():
        try:
            code = read_otp(url)
            last_http_403 = False
        except ToolError as exc:
            if str(exc) != "URL OTP trả HTTP 403":
                raise
            # Some links reject reads until the SMS has reached the provider.
            last_http_403 = True
            code = None
        if code is not None and code != previous_code:
            return code
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        stop.wait(min(interval, remaining))
    if stop.is_set():
        raise ToolError("Đã dừng chờ OTP")
    if last_http_403:
        raise ToolError("URL OTP vẫn trả HTTP 403 sau khi gửi SMS")
    raise ToolError("Hết thời gian chờ OTP mới")
