import tempfile
import unittest
from pathlib import Path

from amazon_android.core import ToolError
from amazon_android.settings import AppSettings, load_settings, save_settings


class SettingsTests(unittest.TestCase):
    def test_setting_persists_across_sessions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            self.assertEqual(load_settings(path).start_group_size, 1)
            self.assertFalse(load_settings(path).hide_profile_creation)
            save_settings(AppSettings(12, True), path)
            self.assertEqual(load_settings(path), AppSettings(12, True))

    def test_old_settings_file_keeps_creation_window_visible(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text('{"start_group_size": 2}', encoding="utf-8")
            self.assertEqual(load_settings(path), AppSettings(2, False))

    def test_setting_requires_one_to_twelve(self):
        for value in (0, 13):
            with self.assertRaises(ToolError):
                AppSettings(value)
        with self.assertRaises(ToolError):
            AppSettings(2, "yes")


if __name__ == "__main__":
    unittest.main()
