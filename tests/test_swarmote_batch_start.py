import unittest
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android.swarmote_desktop import _select_profile_rows, start_profile, start_profiles_together


class FakeBox:
    def __init__(self, name, checked=False):
        self.name = name
        self.checked = checked
        self.element_info = SimpleNamespace(name=name, control_type="CheckBox")
        self.iface_toggle = SimpleNamespace(Toggle=self.toggle)

    def toggle(self):
        self.checked = not self.checked

    def get_toggle_state(self):
        return int(self.checked)


class FakeButton:
    def __init__(self, on_invoke):
        self.element_info = SimpleNamespace(name="Start(2)", control_type="Button")
        self.on_invoke = on_invoke

    def is_enabled(self):
        return True

    def invoke(self):
        self.on_invoke()


class BatchStartTests(unittest.TestCase):
    def test_single_start_can_return_while_phone_is_booting(self):
        invocations = []
        window = object()
        button = FakeButton(lambda: invocations.append("Start"))
        button.element_info.name = "Start(1)"
        row = SimpleNamespace(element_info=SimpleNamespace(name="q1", control_type="DataItem"))
        with patch("amazon_android.swarmote_desktop.profile_status",
                   return_value={"profile_name": "q1", "state": "Offline", "device_id": "ACN1"}) as status, \
             patch("amazon_android.swarmote_desktop._main_window", return_value=window), \
             patch("amazon_android.swarmote_desktop._one",
                   return_value=SimpleNamespace(iface_value=SimpleNamespace(CurrentValue=""))), \
             patch("amazon_android.swarmote_desktop._select_profile_rows"), \
             patch("amazon_android.swarmote_desktop._selected_profile_names", return_value={"q1"}), \
             patch("amazon_android.swarmote_desktop._descendants", return_value=[button, row]):
            result = start_profile("q1", wait=False)
        self.assertEqual(invocations, ["Start"])
        self.assertEqual(result["state"], "Starting")
        self.assertEqual(status.call_count, 1)

    def test_start_finds_profile_on_another_page_and_restores_filter(self):
        window = object()
        current = {"filter": ""}
        button = FakeButton(lambda: None)
        button.element_info.name = "Start(1)"
        row = SimpleNamespace(element_info=SimpleNamespace(name="q30", control_type="DataItem"))

        def descendants(_w):
            return [button, row] if current["filter"] == "q30" else [button]

        def set_value(_w, _name, _kind, value):
            current["filter"] = value

        with patch("amazon_android.swarmote_desktop.profile_status",
                   return_value={"profile_name": "q30", "state": "Offline", "device_id": "ACN30"}), \
             patch("amazon_android.swarmote_desktop._main_window", return_value=window), \
             patch("amazon_android.swarmote_desktop._one",
                   return_value=SimpleNamespace(iface_value=SimpleNamespace(CurrentValue=""))), \
             patch("amazon_android.swarmote_desktop._descendants", side_effect=descendants), \
             patch("amazon_android.swarmote_desktop._set_value", side_effect=set_value), \
             patch("amazon_android.swarmote_desktop._wait_for"), \
             patch("amazon_android.swarmote_desktop._select_profile_rows"), \
             patch("amazon_android.swarmote_desktop._selected_profile_names", return_value={"q30"}):
            result = start_profile("q30", wait=False)
        self.assertEqual(result["state"], "Starting")
        self.assertEqual(current["filter"], "")

    def test_only_confirmed_target_names_are_selected_for_one_start_command(self):
        boxes = {name: FakeBox(name, checked=(name == "q1"))
                 for name in ("q1", "q2", "q3")}
        running = set()
        invocations = []

        def invoke():
            invocations.append({name for name, box in boxes.items() if box.checked})
            running.update(invocations[-1])

        button = FakeButton(invoke)
        window = object()
        rows = {name: object() for name in boxes}

        def status(name):
            return {"profile_name": name,
                    "state": "Running" if name in running else "Offline",
                    "device_id": f"ACN{name}"}

        def one(_window, name, kind):
            self.assertEqual(kind, "DataItem")
            return SimpleNamespace(parent=lambda: rows[name])

        def descendants(control):
            if control is window:
                return [*boxes.values(), button]
            return [boxes[name] for name, row in rows.items() if row is control]

        with patch("amazon_android.swarmote_desktop.profile_status", side_effect=status), \
             patch("amazon_android.swarmote_desktop._main_window", return_value=window), \
             patch("amazon_android.swarmote_desktop._one", side_effect=one), \
             patch("amazon_android.swarmote_desktop._descendants", side_effect=descendants), \
             patch("amazon_android.swarmote_desktop._selected_profile_names",
                   side_effect=lambda _w: {name for name, box in boxes.items() if box.checked}), \
             patch("amazon_android.swarmote_desktop._profile_checkbox",
                   side_effect=lambda _w, name: boxes[name]):
            result = start_profiles_together(["q2", "q3"], timeout=2)

        self.assertEqual(invocations, [{"q2", "q3"}])
        self.assertEqual({name for name, item in result.items() if item["state"] == "Running"},
                         {"q2", "q3"})
        self.assertFalse(boxes["q1"].checked)

    def test_selection_waits_for_each_row_before_toggling_next(self):
        selected = set()
        pending = []
        calls = []
        window = object()

        def checkbox(_w, name):
            def toggle():
                self.assertFalse(pending, "next row toggled before previous selection settled")
                calls.append(name)
                pending.append(name)
            return SimpleNamespace(iface_toggle=SimpleNamespace(Toggle=toggle))

        def read(_w):
            if pending:
                selected.symmetric_difference_update(pending)
                pending.clear()
            return set(selected)

        with patch("amazon_android.swarmote_desktop._profile_checkbox", side_effect=checkbox), \
             patch("amazon_android.swarmote_desktop._selected_profile_names", side_effect=read):
            _select_profile_rows(window, ["q2", "q3"])
        self.assertEqual(calls, ["q2", "q3"])
        self.assertEqual(selected, {"q2", "q3"})


if __name__ == "__main__":
    unittest.main()
