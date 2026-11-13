import unittest
import queue
from unittest.mock import patch

from amazon_android.desktop import Window, _automatic_resume_slots
from amazon_android.runner import AccountData


class DesktopResumeTests(unittest.TestCase):
    def test_restarts_only_ready_work_not_old_errors_or_completed_machines(self):
        items = [
            {"slot": 0, "state": "ERROR", "stage": "APP_INSTALLED"},
            {"slot": 1, "state": "DONE", "stage": "MENU_OPEN"},
            {"slot": 2, "state": "READY", "stage": "PROFILE_CONFIRMED"},
            {"slot": 3, "state": "STOPPED", "stage": "APP_INSTALLED"},
        ]
        self.assertEqual(_automatic_resume_slots(items), [2])

    def test_attach_existing_q1_only_after_running_menu_check(self):
        window = Window.__new__(Window)
        window.attach_events = queue.Queue()
        account = AccountData("12025550123", "Example User", "Example456!",
                              "https://apifc.net/smsrecord?token=q1")
        with patch("amazon_android.desktop.profile_status", return_value={
                "state": "Running", "device_id": "device-q1"}) as status, \
             patch("amazon_android.desktop.open_adb_shell", return_value={
                 "serial": "127.0.0.1:5001"}) as shell, \
             patch("amazon_android.desktop.verify_menu_open") as menu:
            window._probe_existing_profile(0, account)
        self.assertEqual(window.attach_events.get_nowait(),
                         ("ready", account, "127.0.0.1:5001"))
        status.assert_called_once_with("q1")
        shell.assert_called_once_with("q1", "device-q1")
        self.assertEqual(menu.call_args.args[0].serial, "127.0.0.1:5001")

    def test_attach_existing_q1_stops_if_offline(self):
        window = Window.__new__(Window)
        window.attach_events = queue.Queue()
        account = AccountData("12025550123", "Example User", "Example456!",
                              "https://apifc.net/smsrecord?token=q1")
        with patch("amazon_android.desktop.profile_status", return_value={
                "state": "Offline", "device_id": "device-q1"}), \
             patch("amazon_android.desktop.open_adb_shell") as shell, \
             patch("amazon_android.desktop.verify_menu_open") as menu:
            window._probe_existing_profile(0, account)
        state, _, reason = window.attach_events.get_nowait()
        self.assertEqual(state, "error")
        self.assertIn("Offline", reason)
        shell.assert_not_called()
        menu.assert_not_called()

    def test_attach_q2_uses_q2_profile_and_its_own_serial(self):
        window = Window.__new__(Window)
        window.attach_events = queue.Queue()
        account = AccountData("12025550124", "Second User", "Example456!",
                              "https://apifc.net/smsrecord?token=q2")
        with patch("amazon_android.desktop.profile_status", return_value={
                "state": "Running", "device_id": "device-q2"}) as status, \
             patch("amazon_android.desktop.open_adb_shell", return_value={
                 "serial": "127.0.0.1:5002"}) as shell, \
             patch("amazon_android.desktop.verify_menu_open") as menu:
            window._probe_existing_profile(1, account)
        self.assertEqual(window.attach_events.get_nowait(),
                         ("ready", account, "127.0.0.1:5002"))
        status.assert_called_once_with("q2")
        shell.assert_called_once_with("q2", "device-q2")
        self.assertEqual(menu.call_args.args[1], "q2")


if __name__ == "__main__":
    unittest.main()
