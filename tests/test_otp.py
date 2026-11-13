import unittest
from io import BytesIO
from unittest.mock import MagicMock, patch

from amazon_android.core import ToolError
from amazon_android.otp import extract_otp, read_otp, validate_otp_url, wait_for_new_otp


class OtpTests(unittest.TestCase):
    def test_extracts_only_amazon_sign_in_code(self):
        self.assertEqual(extract_otp(
            "yes|Amazon: 354670 is your sign-in code. For your security, don't share it."
        ), "354670")
        self.assertIsNone(extract_otp("no|Waiting for SMS 123456"))
        with self.assertRaises(ToolError):
            extract_otp("yes|Another service: 123456 is your code")

    def test_url_validation_rejects_wrong_endpoint_and_duplicate_token_parameter(self):
        self.assertEqual(validate_otp_url("https://apifc.net/smsrecord?token=test"),
                         "https://apifc.net/smsrecord?token=test")
        for url in (
            "http://apifc.net/smsrecord?token=test",
            "https://other.example/smsrecord?token=test",
            "https://apifc.net/smsrecord?token=",
            "https://apifc.net/smsrecord?token=one&token=two",
        ):
            with self.subTest(url=url), self.assertRaises(ToolError):
                validate_otp_url(url)

    def test_read_otp_fetches_plain_text_response(self):
        url = "https://apifc.net/smsrecord?token=secret"
        with patch("amazon_android.otp._OPENER.open", return_value=BytesIO(
            b"yes|Amazon: 123456 is your sign-in code."
        )):
            self.assertEqual(read_otp(url), "123456")

    def test_read_otp_error_does_not_include_token(self):
        url = "https://apifc.net/smsrecord?token=secret"
        with patch("amazon_android.otp._OPENER.open", side_effect=TimeoutError):
            with self.assertRaises(ToolError) as caught:
                read_otp(url)
        self.assertNotIn("secret", str(caught.exception))

    def test_uses_browser_without_direct_http_request(self):
        url = "https://apifc.net/smsrecord?token=test"
        with patch("amazon_android.otp.read_otp") as direct, \
             patch("amazon_android.otp._read_otp_in_browser", return_value="123456") as browser:
            self.assertEqual(wait_for_new_otp(url, None), "123456")
        direct.assert_not_called()
        self.assertEqual(browser.call_args.args, (url, None))

    def test_tries_edge_after_chrome_receives_a_blocked_page(self):
        url = "https://apifc.net/smsrecord?token=test"
        chrome, edge = MagicMock(), MagicMock()
        chrome.new_page.return_value.url = url
        chrome.new_page.return_value.goto.return_value.ok = False
        page = edge.new_page.return_value
        page.url = url
        page.goto.return_value.ok = True
        page.goto.return_value.headers = {}
        page.locator.return_value.inner_text.side_effect = [
            "no|Waiting", "yes|Amazon: 123456 is your sign-in code."]
        with patch("playwright.sync_api.sync_playwright") as start:
            launch = start.return_value.__enter__.return_value.chromium.launch
            launch.side_effect = [chrome, edge]
            self.assertEqual(wait_for_new_otp(url, None, interval=0.001), "123456")
        self.assertEqual([call.kwargs["channel"] for call in launch.call_args_list],
                         ["chrome", "msedge"])
        self.assertEqual(page.goto.call_count, 2)
        chrome.close.assert_called_once()
        edge.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
