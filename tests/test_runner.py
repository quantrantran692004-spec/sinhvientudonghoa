import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from amazon_android.core import ToolError
from amazon_android.profile_registry import ProfileRegistry
from amazon_android.runner import AccountData, RunJob, run_batch
from amazon_android.swarmote_desktop import (ProfileCreateNotSubmitted,
    ProfileManagerWindowError, ProfileNotFound, ProxyConfig)


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.registry = ProfileRegistry(Path(self.temp.name) / "profiles.json")
        proxy = ProxyConfig("socks5", "proxy.example", 1001, "user", "secret")
        self.jobs = [RunJob(i, "batch", proxy) for i in range(3)]
        self.existing = set()
        self.running = set()
        self.calls = []
        self.stop = threading.Event()

    def status(self, name):
        if name not in self.existing:
            raise ProfileNotFound(name)
        return {"profile_name": name,
                "state": "Running" if name in self.running else "Offline",
                "device_id": f"ACN{name}"}

    def create(self, name, _proxy):
        self.calls.append(f"create:{name}")
        self.existing.add(name)

    def start(self, name, *, wait=True):
        self.calls.append(f"start:{name}")
        self.running.add(name)
        return {"state": "Running" if wait else "Starting",
                "device_id": f"ACN{name}"}

    def install(self, name, device_id=None):
        self.calls.append(f"install:{name}")
        return {"amazon_package_installed": True}

    def group_start(self, names):
        self.calls.append("group:" + ",".join(names))
        return {name: {"state": "Running"} for name in names}

    def execute(self, jobs=None, start_group_size=1, auto_close=True,
                hide_profile_creation=False, menu_ready=None):
        events = []
        def shell(name, device_id):
            return {"serial": f"127.0.0.1:{5000 + int(name[1:])}",
                    "device_id": device_id}

        def menu(phone):
            if auto_close:
                self.running.discard(f"q{int(phone.serial.rsplit(':', 1)[1]) - 5000}")
            return {"stage": "HOME_MENU_OPEN"}

        def create(name, proxy, **kwargs):
            if hide_profile_creation:
                self.assertEqual(kwargs, {"hide_window": True})
            else:
                self.assertEqual(kwargs, {})
            self.create(name, proxy)

        with patch("amazon_android.runner.profile_status", self.status), \
             patch("amazon_android.runner.visible_profile_names",
                   side_effect=lambda: set(self.existing)), \
             patch("amazon_android.runner.create_profile", side_effect=create), \
             patch("amazon_android.runner.start_profile", self.start), \
             patch("amazon_android.runner.install_amazon", self.install), \
             patch("amazon_android.runner.open_adb_shell", side_effect=shell), \
             patch("amazon_android.runner.show_apps"), \
             patch("amazon_android.runner.open_amazon"), \
             patch("amazon_android.runner.open_home_menu", side_effect=menu):
            result = run_batch(jobs or self.jobs, self.registry,
                               lambda *event: events.append(event), self.stop,
                               start_group_size=start_group_size,
                               hide_profile_creation=hide_profile_creation,
                               menu_ready=menu_ready)
        return result, events

    def test_opens_first_phone_before_creating_second_profile(self):
        result, _ = self.execute()
        self.assertEqual(result["menu_open"], 3)
        self.assertLess(self.calls.index("start:q1"), self.calls.index("create:q2"))

    def test_menu_callback_carries_the_correct_phone_serial(self):
        ready = []
        result, _ = self.execute(self.jobs[:2],
                                 menu_ready=lambda *item: ready.append(item))
        self.assertEqual(result["menu_open"], 2)
        self.assertEqual(sorted(ready), [
            (0, "q1", "ACNq1", "127.0.0.1:5001"),
            (1, "q2", "ACNq2", "127.0.0.1:5002"),
        ])

    def test_existing_q2_menu_reconnects_its_serial_before_done(self):
        item = self.registry.reserve("batch", 1, self.status)
        self.existing.add("q2")
        self.running.add("q2")
        self.registry.mark("batch", 1, "DONE", device_id="ACNq2",
                           stage="MENU_OPEN")
        account_job = RunJob(1, "batch", self.jobs[1].proxy,
                             account=AccountData(
                                 "12025550124", "Second User", "Example456!",
                                 "https://apifc.net/smsrecord?token=q2"))
        ready = []
        result, events = self.execute([account_job], auto_close=False,
                                      menu_ready=lambda *args: ready.append(args))
        self.assertEqual(result["menu_open"], 1)
        self.assertEqual(ready, [(1, "q2", "ACNq2", "127.0.0.1:5002")])
        self.assertEqual(events[-1][2], "done")
        self.assertNotIn("install:q2", self.calls)

    def test_existing_q2_menu_offline_does_not_claim_automation_started(self):
        self.registry.reserve("batch", 1, self.status)
        self.existing.add("q2")
        self.registry.mark("batch", 1, "DONE", device_id="ACNq2",
                           stage="MENU_OPEN")
        ready = []
        result, events = self.execute([self.jobs[1]],
                                      menu_ready=lambda *args: ready.append(args))
        self.assertEqual(result["stopped"], 1)
        self.assertEqual(ready, [])
        self.assertEqual(events[-1][2], "stopped")

    def test_hidden_creation_setting_only_changes_create_call(self):
        result, _ = self.execute(self.jobs[:1], hide_profile_creation=True)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["menu_open"], 1)
        self.assertIn("start:q1", self.calls)

    def test_fresh_fixed_name_is_checked_before_create(self):
        original_status = self.status
        checked = []

        def status(name):
            if name not in self.existing:
                checked.append(name)
            return original_status(name)

        with patch.object(self, "status", side_effect=status):
            result, _ = self.execute(self.jobs[:1])
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["menu_open"], 1)
        self.assertEqual(checked, ["q1"])

    def test_manager_window_error_stops_batch_before_reserving_more_names(self):
        def unavailable(_name, _proxy):
            try:
                raise ProfileManagerWindowError("two manager windows")
            except ProfileManagerWindowError as exc:
                raise ProfileCreateNotSubmitted(str(exc)) from exc

        with patch.object(self, "create", side_effect=unavailable):
            result, _ = self.execute()
        self.assertEqual(result["error"], 1)
        self.assertEqual(result["stopped"], 2)
        self.assertIsNone(self.registry.get("batch", 1))
        self.assertIsNone(self.registry.get("batch", 2))

    def test_creates_second_profile_while_first_phone_is_installing(self):
        second_created = threading.Event()
        first_install_started = threading.Event()
        original_create = self.create
        original_install = self.install

        def create(name, proxy):
            if name == "q2":
                self.assertTrue(first_install_started.wait(3),
                                "q2 creation did not overlap q1 installation")
            original_create(name, proxy)
            if name == "q2":
                second_created.set()

        def install(name, device_id=None):
            if name == "q1":
                first_install_started.set()
                self.assertTrue(second_created.wait(3), "q2 creation waited for q1 install")
            return original_install(name, device_id=device_id)

        with patch.object(self, "create", side_effect=create), \
             patch.object(self, "install", side_effect=install):
            result, _ = self.execute(self.jobs[:2], start_group_size=2)
        self.assertTrue(first_install_started.is_set())
        self.assertEqual(result["menu_open"], 2)

    def test_next_phone_waits_until_user_closes_a_running_phone(self):
        third_created = threading.Event()
        original_create = self.create
        result = {}

        def create(name, proxy):
            original_create(name, proxy)
            if name == "q3":
                third_created.set()

        def run():
            with patch.object(self, "create", side_effect=create):
                result["summary"], result["events"] = self.execute(
                    start_group_size=2, auto_close=False)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        self.assertTrue(third_created.wait(3))
        self.assertNotIn("start:q3", self.calls)
        self.running.discard("q1")  # User closes a phone in Swarmote.
        thread.join(6)
        self.assertFalse(thread.is_alive())
        self.assertIn("start:q3", self.calls)
        self.assertEqual(result["summary"]["menu_open"], 3)

    def test_stop_releases_waiting_batch_without_starting_next_phone(self):
        third_created = threading.Event()
        original_create = self.create
        result = {}

        def create(name, proxy):
            original_create(name, proxy)
            if name == "q3":
                third_created.set()

        def run():
            with patch.object(self, "create", side_effect=create):
                result["summary"], _ = self.execute(start_group_size=2, auto_close=False)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        self.assertTrue(third_created.wait(3))
        self.stop.set()
        thread.join(6)
        self.assertFalse(thread.is_alive())
        self.assertNotIn("start:q3", self.calls)
        self.assertEqual(self.registry.get("batch", 2)["state"], "STOPPED")

    def test_continue_respects_running_phones_from_same_batch(self):
        first, _ = self.execute(self.jobs[:2], start_group_size=2, auto_close=False)
        self.assertEqual(first["menu_open"], 2)
        item = self.registry.reserve("batch", 2, self.status)
        self.create(item["name"], self.jobs[2].proxy)
        self.registry.mark("batch", 2, "READY", device_id="ACNq3",
                           stage="PROFILE_CONFIRMED")
        result = {}

        def resume():
            result["summary"], _ = self.execute(self.jobs[2:], start_group_size=2,
                                                auto_close=False)

        thread = threading.Thread(target=resume, daemon=True)
        thread.start()
        time.sleep(0.3)
        self.assertNotIn("start:q3", self.calls)
        self.running.discard("q1")
        thread.join(6)
        self.assertFalse(thread.is_alive())
        self.assertIn("start:q3", self.calls)
        self.assertEqual(result["summary"]["menu_open"], 1)

    def test_full_resume_counts_running_profiles_before_starting_waiter(self):
        for index in range(3):
            item = self.registry.reserve("batch", index, self.status)
            self.existing.add(item["name"])
            self.registry.mark("batch", index,
                               "DONE" if index < 2 else "READY",
                               device_id=f"ACN{item['name']}",
                               stage="MENU_OPEN" if index < 2 else "PROFILE_CONFIRMED")
        self.running.update({"q1", "q2"})
        result = {}

        def resume():
            result["summary"], _ = self.execute(start_group_size=2, auto_close=False)

        thread = threading.Thread(target=resume, daemon=True)
        thread.start()
        time.sleep(0.3)
        self.assertNotIn("start:q3", self.calls)
        self.running.discard("q1")
        thread.join(6)
        self.assertFalse(thread.is_alive())
        self.assertIn("start:q3", self.calls)

    def test_settings_limit_starts_only_confirmed_profiles(self):
        result, _ = self.execute(start_group_size=12)
        self.assertEqual(result["menu_open"], 3)
        self.assertEqual({call for call in self.calls if call.startswith("start:")},
                         {"start:q1", "start:q2", "start:q3"})

    def test_limit_two_eventually_starts_all_when_closed(self):
        result, _ = self.execute(start_group_size=2)
        self.assertEqual(result["menu_open"], 3)
        self.assertIn("start:q1", self.calls)
        self.assertIn("start:q2", self.calls)
        self.assertIn("start:q3", self.calls)

    def test_failed_start_still_creates_remaining_profiles(self):
        def failed_start(name, *, wait=True):
            self.calls.append("start:" + name)
            raise ToolError("selection failed")

        with patch.object(self, "start", side_effect=failed_start):
            result, events = self.execute(start_group_size=2)
        self.assertEqual(result["error"], 1)
        self.assertEqual(result["stopped"], 2)
        self.assertIn("create:q3", self.calls)
        self.assertNotIn("start:q2", self.calls)
        self.assertTrue(any(e[0] == 2 and e[2] == "stopped" for e in events))

    def test_failed_create_does_not_retry_and_other_rows_continue(self):
        normal_create = self.create
        def create(name, proxy):
            if name == "q2":
                self.calls.append("create:q2")
                raise ToolError("uncertain")
            normal_create(name, proxy)
        with patch.object(self, "create", side_effect=create):
            result, events = self.execute()
        self.assertEqual(result["menu_open"], 2)
        self.assertEqual(result["error"], 1)
        self.assertEqual(self.registry.get("batch", 1)["state"], "UNCERTAIN")
        self.assertNotIn("start:q2", self.calls)
        self.assertTrue(any(e[0] == 1 and e[2] == "uncertain" for e in events))

    def test_continue_after_install_skips_second_install(self):
        normal_install = self.install
        def install_then_stop(name, device_id=None):
            normal_install(name, device_id=device_id)
            self.stop.set()
        with patch.object(self, "install", side_effect=install_then_stop):
            result, _ = self.execute(self.jobs[:1])
        self.assertEqual(result["stopped"], 1)
        self.assertEqual(self.registry.get("batch", 0)["stage"], "APP_INSTALLED")
        self.stop.clear()
        result, _ = self.execute(self.jobs[:1])
        self.assertEqual(result["menu_open"], 1)
        self.assertEqual(self.calls.count("create:q1"), 1)
        self.assertEqual(self.calls.count("install:q1"), 1)

    def test_proxy_test_failure_is_known_not_submitted(self):
        def failed(_name, _proxy):
            raise ProfileCreateNotSubmitted("Test Failed")
        with patch.object(self, "create", side_effect=failed):
            result, events = self.execute(self.jobs[:1])
        item = self.registry.get("batch", 0)
        self.assertEqual((item["state"], item["stage"]), ("ERROR", "RESERVED"))
        self.assertEqual(item["last_error"], "Test Failed")
        self.assertEqual(result["error"], 1)
        self.assertTrue(any(e[2] == "error" for e in events))


if __name__ == "__main__":
    unittest.main()
