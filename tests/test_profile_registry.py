import tempfile
import unittest
from pathlib import Path

from amazon_android.profile_registry import ProfileRegistry
from amazon_android.swarmote_desktop import ProfileNotFound, ProfileLookupError


def absent(name):
    raise ProfileNotFound(name)


class ProfileRegistryTests(unittest.TestCase):
    def test_session_registry_does_not_write_or_advance_next_launch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profiles.json"
            first = ProfileRegistry(path, persistent=False)
            self.assertEqual(first.reserve("a", 0, absent)["name"], "q1")
            self.assertFalse(path.exists())
            second = ProfileRegistry(path, persistent=False)
            self.assertEqual(second.preview_names(12), [f"q{i}" for i in range(1, 13)])

    def test_reopens_only_confirmed_unfinished_batch_without_proxy_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profiles.json"
            registry = ProfileRegistry(path)
            for slot in range(3):
                registry.reserve("batch", slot, absent)
                registry.mark("batch", slot, "READY", device_id=f"ACN{slot}",
                              stage="PROFILE_CONFIRMED")
            for slot in (0, 1):
                registry.mark("batch", slot, "DONE", stage="MENU_OPEN")
            restored = ProfileRegistry(path).latest_resumable_batch()
            self.assertIsNotNone(restored)
            self.assertEqual(restored[0], "batch")
            self.assertEqual([item["name"] for item in restored[1]], ["q1", "q2", "q3"])
            registry.mark("batch", 2, "DONE", stage="MENU_OPEN")
            self.assertIsNone(ProfileRegistry(path).latest_resumable_batch())

    def test_completed_latest_batch_does_not_resume_older_batch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profiles.json"
            registry = ProfileRegistry(path)
            registry.reserve("old", 0, absent)
            registry.mark("old", 0, "READY", device_id="ACN1",
                          stage="PROFILE_CONFIRMED")
            registry.reserve("new", 0, absent)
            registry.mark("new", 0, "DONE", device_id="ACN2", stage="MENU_OPEN")
            self.assertIsNone(ProfileRegistry(path).latest_resumable_batch())

    def test_each_new_batch_reuses_twelve_fixed_slot_names(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profiles.json"
            names = []
            for batch, size in (("a", 3), ("b", 5), ("c", 4)):
                registry = ProfileRegistry(path)
                names.extend(registry.reserve(batch, i, absent)["name"] for i in range(size))
            self.assertEqual(names, [f"q{i}" for i in range(1, 4)] +
                             [f"q{i}" for i in range(1, 6)] +
                             [f"q{i}" for i in range(1, 5)])
            content = path.read_text(encoding="utf-8")
            self.assertNotIn("password", content.casefold())
            self.assertNotIn("proxy", content.casefold())

    def test_existing_external_name_blocks_fixed_slot(self):
        with tempfile.TemporaryDirectory() as directory:
            registry = ProfileRegistry(Path(directory) / "profiles.json")
            def lookup(name):
                if name == "q1":
                    return {"profile_name": name}
                raise ProfileNotFound(name)
            with self.assertRaisesRegex(Exception, "q1"):
                registry.reserve("a", 0, lookup)
            self.assertIsNone(registry.get("a", 0))

    def test_lookup_error_does_not_reserve_a_name(self):
        with tempfile.TemporaryDirectory() as directory:
            registry = ProfileRegistry(Path(directory) / "profiles.json")
            def broken(_name):
                raise ProfileLookupError("UI changed")
            with self.assertRaises(ProfileLookupError):
                registry.reserve("a", 0, broken)
            self.assertIsNone(registry.get("a", 0))

    def test_failed_before_create_reuses_name_in_next_batch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profiles.json"
            registry = ProfileRegistry(path)
            first = registry.reserve("old", 0, absent)
            self.assertEqual(first["name"], "q1")
            registry.mark("old", 0, "ERROR", stage="RESERVED")
            reopened = ProfileRegistry(path)
            self.assertEqual(reopened.preview_names(2), ["q1", "q2"])
            reused = reopened.reserve("new", 0, absent)
            self.assertEqual(reused["name"], "q1")
            self.assertEqual(reopened.get("old", 0)["name"], "q1")
            self.assertEqual(reopened.reserve("new", 1, absent)["name"], "q2")

    def test_uncertain_old_batch_does_not_advance_new_batch_slot(self):
        with tempfile.TemporaryDirectory() as directory:
            registry = ProfileRegistry(Path(directory) / "profiles.json")
            registry.reserve("old", 0, absent)
            registry.mark("old", 0, "UNCERTAIN", stage="CREATING")
            self.assertEqual(registry.reserve("new", 0, absent)["name"], "q1")


if __name__ == "__main__":
    unittest.main()
