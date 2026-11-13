import unittest
import subprocess
from unittest.mock import patch

from amazon_android import cloud
from amazon_android.core import ToolError


class CloudBridgeTests(unittest.TestCase):
    @patch.object(cloud, "probe", return_value={"boot_completed": True,
                                                  "amazon_package_installed": True})
    def test_open_amazon_does_not_relaunch_foreground_app(self, _):
        calls = []
        def adb(_phone, *args, **_kwargs):
            calls.append(args)
            if "pidof" in args:
                return subprocess.CompletedProcess([], 0, "1234\n", "")
            if "dumpsys" in args:
                return subprocess.CompletedProcess([], 0,
                    "mCurrentFocus=Window{com.amazon.mShop.android.shopping/MainActivity}", "")
            self.fail(f"unexpected command: {args}")
        with patch.object(cloud, "cloud_adb", side_effect=adb):
            result = cloud.open_amazon(cloud.CloudPhone("127.0.0.1:12345"))
        self.assertTrue(result["amazon_foreground"])
        self.assertFalse(any("monkey" in args for args in calls))

    @patch.object(cloud, "probe", return_value={"boot_completed": True,
                                                  "amazon_package_installed": True})
    def test_open_amazon_retries_once_after_first_launch_exits(self, _):
        launches = 0
        checks = 0
        def adb(_phone, *args, **_kwargs):
            nonlocal launches, checks
            if "monkey" in args:
                launches += 1
                return subprocess.CompletedProcess([], 0, "Events injected: 1", "")
            if "pidof" in args:
                checks += 1
                return subprocess.CompletedProcess([], 0,
                    "1234\n" if launches == 2 else "", "")
            if "dumpsys" in args:
                return subprocess.CompletedProcess([], 0,
                    "mCurrentFocus=Window{com.amazon.mShop.android.shopping/MainActivity}", "")
            self.fail(f"unexpected command: {args}")
        with patch.object(cloud, "cloud_adb", side_effect=adb), \
             patch.object(cloud.time, "sleep"):
            result = cloud.open_amazon(cloud.CloudPhone("127.0.0.1:12345"))
        self.assertTrue(result["amazon_foreground"])
        self.assertEqual(launches, 2)
        self.assertGreaterEqual(checks, 10)

    def test_remote_host_is_not_accepted_as_swarmote_tunnel(self):
        with self.assertRaises(ToolError):
            cloud.CloudPhone("example.com:5555")

    @patch.object(cloud, "cloud_serials", return_value={})
    def test_no_tunnel_is_not_a_device(self, _):
        self.assertEqual(cloud.scan()["phones"], [])

    @patch.object(cloud, "swarmote_tunnel_owner", side_effect=lambda port: port == 12345)
    @patch.object(cloud, "cloud_adb", return_value=subprocess.CompletedProcess([], 0,
        "List of devices attached\n127.0.0.1:12345 device\n127.0.0.1:5555 device\n", ""))
    def test_discovery_excludes_other_local_adb_devices(self, *_):
        self.assertEqual(cloud.cloud_serials(), {"127.0.0.1:12345": "device"})

    @patch.object(cloud, "require_online")
    @patch.object(cloud, "prop", return_value="value")
    @patch.object(cloud, "package_path", return_value="/data/app/base.apk")
    @patch.object(cloud, "reported_installer", return_value="com.android.vending")
    def test_installer_metadata_does_not_prove_source(self, *_):
        result = cloud.probe(cloud.CloudPhone("127.0.0.1:12345"))
        self.assertTrue(result["amazon_package_installed"])
        self.assertEqual(result["reported_installer"], "com.android.vending")
        self.assertFalse(result["source_verified"])

    @patch.object(cloud, "probe", return_value={"boot_completed": True, "amazon_package_installed": False})
    @patch.object(cloud, "cloud_adb")
    def test_open_rejects_missing_package(self, adb, _):
        with self.assertRaisesRegex(ToolError, "chưa thấy Amazon"):
            cloud.open_amazon(cloud.CloudPhone("127.0.0.1:12345"))
        adb.assert_not_called()


if __name__ == "__main__":
    unittest.main()
