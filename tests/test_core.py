import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from amazon_android import core


class SafetyTests(unittest.TestCase):
    @patch.object(core.subprocess, "run",
                  return_value=subprocess.CompletedProcess(["adb.exe"], 0, "ok", ""))
    def test_windows_adb_commands_do_not_open_console_windows(self, run):
        with patch.object(core.sys, "platform", "win32"):
            result = core.run([Path("adb.exe"), "devices"])
        self.assertEqual(result.stdout, "ok")
        self.assertEqual(run.call_args.kwargs["creationflags"],
                         subprocess.CREATE_NO_WINDOW)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = core.Store(Path(self.temp.name) / "state.sqlite3")
        self.device = core.get_device(1)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_state_survives_reopen(self):
        self.store.set(self.device, "DEVICE_READY", "ADB sẵn sàng", 12.5)
        self.store.db.close()
        reopened = core.Store(Path(self.temp.name) / "state.sqlite3")
        self.assertEqual(reopened.devices()[0]["state"], "DEVICE_READY")
        self.assertEqual(reopened.devices()[0]["boot_seconds"], 12.5)
        self.assertEqual(len(reopened.events(1)), 1)
        reopened.close()

    @patch.object(core, "executable", return_value=Path("adb.exe"))
    @patch.object(core, "run")
    def test_local_adb_does_not_replace_swarmote_server(self, run, _):
        core.adb(None, "devices")
        self.assertEqual(run.call_args.args[0][:3], [Path("adb.exe"), "-P", "5038"])

    @patch.object(core, "available_memory_mb", return_value=400)
    @patch.object(core, "emulator_serials", return_value=set())
    @patch.object(core, "avd_names", return_value={"Amazon_Android_01"})
    @patch.object(core, "executable", return_value=Path("emulator.exe"))
    @patch.object(core.subprocess, "Popen")
    def test_low_ram_never_launches_emulator(self, popen, *_):
        with self.assertRaisesRegex(core.ToolError, "RAM trống"):
            core.start_device(self.device, self.store)
        popen.assert_not_called()

    @patch.object(core, "check_play")
    @patch.object(core, "package_installed", return_value=False)
    @patch.object(core, "adb", return_value=subprocess.CompletedProcess([], 0, "Starting: Intent", ""))
    @patch("builtins.print")
    def test_opening_play_page_is_not_install_success(self, *_):
        with self.assertRaisesRegex(core.ToolError, "Hết thời gian"):
            core.install_amazon(self.device, self.store, timeout=0)
        self.assertEqual(self.store.devices()[0]["state"], "ERROR")

    @patch.object(core, "check_play")
    @patch.object(core, "package_installed", return_value=True)
    @patch.object(core, "play_install_verified", return_value=False)
    def test_unverified_installer_is_rejected(self, *_):
        with self.assertRaisesRegex(core.ToolError, "nguồn cài"):
            core.install_amazon(self.device, self.store)

    @patch.object(core, "adb")
    def test_play_installer_must_match_package(self, adb):
        adb.return_value = subprocess.CompletedProcess([], 0,
            "package:com.other installer=com.android.vending\n"
            "package:com.amazon.mShop.android.shopping installer=com.android.vending\n", "")
        self.assertTrue(core.play_install_verified(self.device))
        adb.return_value = subprocess.CompletedProcess([], 0,
            "package:com.amazon.mShop.android.shopping installer=null\n", "")
        self.assertFalse(core.play_install_verified(self.device))


if __name__ == "__main__":
    unittest.main()
