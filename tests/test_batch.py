import unittest
from unittest.mock import patch

from amazon_android.batch import BatchItem, parse_proxy_line, prepare_five
from amazon_android.core import ToolError


class BatchSafetyTests(unittest.TestCase):
    def test_proxy_line_rejects_missing_secret(self):
        with self.assertRaises(ToolError):
            parse_proxy_line("proxy.example:1080:user:")

    def test_failed_create_is_not_started_or_retried(self):
        proxy = parse_proxy_line("proxy.example:1080:user:secret")
        items = [BatchItem(f"Amazon-{i}", proxy) for i in range(5)]
        with patch("amazon_android.batch.create_profile", side_effect=ToolError("uncertain")) as create:
            with patch("amazon_android.batch.ready_for_registration") as ready:
                result = prepare_five(items, lambda *_: None)
        self.assertEqual(create.call_count, 5)
        ready.assert_not_called()
        self.assertTrue(all(item["stage"] == "ERROR" for item in result))

    def test_duplicate_names_stop_before_cloud_calls(self):
        proxy = parse_proxy_line("proxy.example:1080:user:secret")
        items = [BatchItem("same", proxy) for _ in range(5)]
        with patch("amazon_android.batch.create_profile") as create:
            with self.assertRaises(ToolError):
                prepare_five(items, lambda *_: None)
        create.assert_not_called()


if __name__ == "__main__":
    unittest.main()
