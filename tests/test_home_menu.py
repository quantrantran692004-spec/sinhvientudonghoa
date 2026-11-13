import unittest
import subprocess
from unittest.mock import patch

from amazon_android.cloud import CloudPhone
from amazon_android.core import AMAZON_PACKAGE, ToolError
from amazon_android.home_menu import _nodes, open_home_menu


class HomeMenuTests(unittest.TestCase):
    def test_leaves_account_verification_screen_untouched(self):
        phone = CloudPhone("127.0.0.1:12345")
        with patch("amazon_android.home_menu._nodes", return_value=[
            {"text": "Authentication required", "package": AMAZON_PACKAGE},
            {"text": "Verify mobile number", "package": AMAZON_PACKAGE},
        ]), patch("amazon_android.home_menu._tap") as tap:
            with self.assertRaisesRegex(ToolError, "xác minh tài khoản"):
                open_home_menu(phone, timeout=1)
        tap.assert_not_called()

    def test_accepts_valid_android_dump_after_interrupted_adb_exit(self):
        phone = CloudPhone("127.0.0.1:12345")
        path = "/sdcard/amazon_tool_menu.xml"
        dumped = subprocess.CompletedProcess([], 3221225786,
                                             f"UI hierchary dumped to: {path}\n", "")
        xml = f'<hierarchy><node package="{AMAZON_PACKAGE}" text="Skip sign in" /></hierarchy>'
        read = subprocess.CompletedProcess([], 0, xml, "")
        with patch("amazon_android.home_menu.cloud_adb", side_effect=[dumped, read]) as adb:
            nodes = _nodes(phone)
        self.assertEqual(nodes[0]["text"], "Skip sign in")
        self.assertEqual(adb.call_count, 2)

    def test_retries_failed_dump_before_reading_xml(self):
        phone = CloudPhone("127.0.0.1:12345")
        path = "/sdcard/amazon_tool_menu.xml"
        failed = subprocess.CompletedProcess([], 3221225786, "", "")
        dumped = subprocess.CompletedProcess([], 0, f"dumped to: {path}", "")
        xml = f'<hierarchy><node package="{AMAZON_PACKAGE}" /></hierarchy>'
        read = subprocess.CompletedProcess([], 0, xml, "")
        with patch("amazon_android.home_menu.cloud_adb",
                   side_effect=[failed, dumped, read]) as adb, \
             patch("amazon_android.home_menu.time.sleep"):
            nodes = _nodes(phone)
        self.assertEqual(nodes[0]["package"], AMAZON_PACKAGE)
        self.assertEqual(adb.call_count, 3)

    def test_category_heading_with_or_without_period_confirms_menu(self):
        phone = CloudPhone("127.0.0.1:12345")
        for heading in ("Shop by category", "Shop by category."):
            with self.subTest(heading=heading), patch(
                "amazon_android.home_menu._nodes",
                return_value=[{"text": heading, "package": "com.amazon.mShop.android.shopping"}],
            ):
                self.assertEqual(open_home_menu(phone, timeout=1)["stage"], "HOME_MENU_OPEN")


if __name__ == "__main__":
    unittest.main()
