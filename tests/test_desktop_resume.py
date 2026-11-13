import unittest
import queue
import threading
from unittest.mock import patch

from amazon_android.desktop import Window, _automatic_resume_slots
from amazon_android.runner import AccountData, RunJob


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

    def test_q2_menu_without_serial_reports_why_it_cannot_start(self):
        window = Window.__new__(Window)
        window.post_menu_step_factories = {1: lambda *_: ()}
        window.post_menu_sessions = {}
        window.cancel = threading.Event()
        window.events = queue.Queue()
        window.jobs = {1: RunJob(1, "batch", None, account=AccountData(
            "12025550124", "Second User", "Example456!",
            "https://apifc.net/smsrecord?token=q2"))}
        window.phone_serials = {}
        window._start_post_menu(1)
        index, message, state, name = window.events.get_nowait()
        self.assertEqual((index, state, name), (1, "post_paused", "q2"))
        self.assertIn("chưa nối ADB", message)

    def test_q2_menu_without_amazon_row_reports_missing_data(self):
        window = Window.__new__(Window)
        window.post_menu_step_factories = {1: lambda *_: ()}
        window.post_menu_sessions = {}
        window.cancel = threading.Event()
        window.events = queue.Queue()
        window.jobs = {1: RunJob(1, "batch", None)}
        window.phone_serials = {1: "127.0.0.1:5002"}
        window._start_post_menu(1)
        _, message, state, _ = window.events.get_nowait()
        self.assertEqual(state, "menu_only")
        self.assertIn("chưa có hàng Amazon", message)


if __name__ == "__main__":
    unittest.main()
