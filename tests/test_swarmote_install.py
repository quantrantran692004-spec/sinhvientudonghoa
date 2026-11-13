import unittest
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android.swarmote_desktop import install_amazon, show_apps


class FakeControl:
    def __init__(self, name, kind, rectangle=(0, 0, 0, 0), invoke=None):
        self.element_info = SimpleNamespace(name=name, control_type=kind)
        self.coords = SimpleNamespace(left=rectangle[0], top=rectangle[1],
                                      right=rectangle[2], bottom=rectangle[3])
        self.on_invoke = invoke

    def rectangle(self):
        return self.coords

    def invoke(self):
        if self.on_invoke:
            self.on_invoke()

    def is_visible(self):
        return True


class InstallTests(unittest.TestCase):
    def test_apps_waits_for_phone_ui_without_using_screen_coordinates(self):
        events = []
        window = object()
        apps = FakeControl("Apps", "Text")
        apps.parent = lambda: FakeControl("", "Group", invoke=lambda: events.append("apps"))
        scans = []

        def descendants(_w):
            scans.append(1)
            return [] if len(scans) < 4 else [apps]

        with patch("amazon_android.swarmote_desktop._phone_window", return_value=window), \
             patch("amazon_android.swarmote_desktop._descendants", side_effect=descendants), \
             patch("amazon_android.swarmote_desktop._wait_for"), \
             patch("amazon_android.swarmote_desktop.time.sleep"):
            show_apps("q5", "ACN5")
        self.assertEqual(events, ["apps"])
        self.assertEqual(len(scans), 4)

    def test_returns_from_terminal_to_apps(self):
        events = []
        window = object()
        apps = FakeControl("Apps", "Text")
        apps.parent = lambda: FakeControl("", "Group", invoke=lambda: events.append("apps"))
        with patch("amazon_android.swarmote_desktop._phone_window", return_value=window), \
             patch("amazon_android.swarmote_desktop._descendants", return_value=[apps]), \
             patch("amazon_android.swarmote_desktop._wait_for") as wait:
            self.assertIs(show_apps("q2", "ACN1"), window)
        self.assertEqual(events, ["apps"])
        wait.assert_called_once_with(window, "App Store", "TabItem", seconds=10)

    def test_search_and_install_precede_terminal(self):
        events = []
        window = object()
        controls = [FakeControl("Apps", "Text"), FakeControl("App Store", "TabItem"),
                    FakeControl("Amazon Shopping", "Text", (100, 100, 200, 120)),
                    FakeControl("Install", "Button", (220, 105, 270, 140),
                                lambda: events.append("install"))]
        with patch("amazon_android.swarmote_desktop.profile_status",
                   return_value={"state": "Running", "device_id": "ACN1"}), \
             patch("amazon_android.swarmote_desktop.show_apps",
                   side_effect=lambda *_args: events.append("apps") or window), \
             patch("amazon_android.swarmote_desktop._descendants", return_value=controls), \
             patch("amazon_android.swarmote_desktop._wait_for"), \
             patch("amazon_android.swarmote_desktop._set_value",
                   side_effect=lambda _w, _n, _k, value: events.append("search:" + value)), \
             patch("amazon_android.swarmote_desktop.open_adb_shell",
                   side_effect=lambda _n, _id: events.append("terminal") or
                   {"serial": "127.0.0.1:5555", "device_id": "ACN1"}), \
             patch("amazon_android.cloud.require_online"), \
             patch("amazon_android.cloud.package_path", return_value="/data/app/amazon.apk"):
            result = install_amazon("q2")
        self.assertEqual(events, ["apps", "search:z", "install", "terminal", "apps"])
        self.assertTrue(result["amazon_package_installed"])


if __name__ == "__main__":
    unittest.main()
