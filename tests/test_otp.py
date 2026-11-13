import threading
import unittest
from io import BytesIO
from unittest.mock import patch

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

    def test_waits_for_new_code_and_keeps_profiles_separate(self):
        url_a = "https://apifc.net/smsrecord?token=one"
        url_b = "https://apifc.net/smsrecord?token=two"
        replies = {url_a: iter(["111111", "333333"]),
                   url_b: iter(["222222", "444444"])}
        lock = threading.Lock()

        def next_code(url):
            with lock:
                return next(replies[url])

        result = {}
        with patch("amazon_android.otp.read_otp", side_effect=next_code):
            threads = [
                threading.Thread(target=lambda: result.update(a=wait_for_new_otp(
                    url_a, "111111", timeout=2, interval=0.001))),
                threading.Thread(target=lambda: result.update(b=wait_for_new_otp(
                    url_b, "222222", timeout=2, interval=0.001))),
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        self.assertEqual(result, {"a": "333333", "b": "444444"})

    def test_retries_temporary_http_403_after_sms_send(self):
        url = "https://apifc.net/smsrecord?token=test"
        with patch("amazon_android.otp.read_otp",
                   side_effect=[ToolError("URL OTP trả HTTP 403"), "123456"]):
            self.assertEqual(wait_for_new_otp(url, None, timeout=2,
                                              interval=0.001), "123456")


if __name__ == "__main__":
    unittest.main()
