import unittest
from types import SimpleNamespace
from unittest.mock import patch

import win32con

from amazon_android.core import ToolError
from amazon_android.swarmote_desktop import ProxyConfig, create_profile


class CreationWindowVisibilityTests(unittest.TestCase):
    def setUp(self):
        self.window = SimpleNamespace(handle=123)
        self.proxy = ProxyConfig("socks5", "proxy.example", 3010, "user", "pass")
        self.visible = True
        self.transitions = []

    def show_window(self, _handle, command):
        self.transitions.append(command)
        self.visible = command != win32con.SW_HIDE

    def test_hidden_creation_restores_main_window(self):
        with patch("amazon_android.swarmote_desktop._main_window", return_value=self.window), \
             patch("amazon_android.swarmote_desktop._create_profile_form",
                   return_value={"created": True}) as create, \
             patch("win32gui.ShowWindow", side_effect=self.show_window), \
             patch("win32gui.IsWindowVisible", side_effect=lambda _handle: self.visible), \
             patch("win32gui.IsWindow", return_value=True):
            result = create_profile("q1", self.proxy, hide_window=True)
        self.assertTrue(result["created"])
        create.assert_called_once_with("q1", self.proxy, self.window)
        self.assertEqual(self.transitions, [win32con.SW_HIDE, win32con.SW_SHOWNA])
        self.assertTrue(self.visible)

    def test_hidden_creation_restores_main_window_after_error(self):
        with patch("amazon_android.swarmote_desktop._main_window", return_value=self.window), \
             patch("amazon_android.swarmote_desktop._create_profile_form",
                   side_effect=ToolError("proxy failed")), \
             patch("win32gui.ShowWindow", side_effect=self.show_window), \
             patch("win32gui.IsWindowVisible", side_effect=lambda _handle: self.visible), \
             patch("win32gui.IsWindow", return_value=True):
            with self.assertRaises(ToolError):
                create_profile("q1", self.proxy, hide_window=True)
        self.assertEqual(self.transitions, [win32con.SW_HIDE, win32con.SW_SHOWNA])
        self.assertTrue(self.visible)


if __name__ == "__main__":
    unittest.main()
