import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android.cloud import CloudPhone
from amazon_android.core import ToolError
from amazon_android.post_menu import (
    AttemptDeadline, PostMenuSession, PostMenuStep, attempt_seconds,
    type_characters,
)
from amazon_android.runner import RunJob


class PostMenuTests(unittest.TestCase):
    def test_each_phone_has_its_own_cyclic_attempt_budget(self):
        self.assertEqual([attempt_seconds(i) // 60 for i in range(1, 10)],
                         [3, 4, 5, 4, 3, 4, 5, 4, 3])
        q1 = PostMenuSession("batch", 0, "q1")
        q2 = PostMenuSession("batch", 1, "q2")
        self.assertEqual((q1.attempts, q2.attempts), (0, 0))

    def test_error_pauses_only_its_phone_and_continue_rechecks_same_step(self):
        q1 = PostMenuSession("batch", 0, "q1")
        q2 = PostMenuSession("batch", 1, "q2")
        repaired = threading.Event()
        calls = []
        events = []

        def first_step(job, deadline, stop):
            calls.append((job.index, "first", deadline.seconds))
            if job.index == 0 and not repaired.is_set():
                raise ToolError("Màn hình chưa đúng")

        def second_step(job, deadline, stop):
            calls.append((job.index, "second", deadline.seconds))

        steps = (PostMenuStep("Bước đầu", first_step),
                 PostMenuStep("Bước sau", second_step))
        emit = lambda *event: events.append(event)
        threads = [
            threading.Thread(target=q1.run,
                             args=(RunJob(0, "batch", None), steps, emit, threading.Event())),
            threading.Thread(target=q2.run,
                             args=(RunJob(1, "batch", None), steps, emit, threading.Event())),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual((q1.state, q1.next_step, q1.attempts), ("PAUSED", 0, 1))
        self.assertEqual((q2.state, q2.next_step, q2.attempts), ("DONE", 2, 1))
        self.assertTrue(any(event[0] == 0 and event[2] == "post_paused" for event in events))
        repaired.set()
        q1.run(RunJob(0, "batch", None), steps, emit, threading.Event())
        self.assertEqual((q1.state, q1.next_step, q1.attempts), ("DONE", 2, 2))
        self.assertEqual([call for call in calls if call[0] == 0],
                         [(0, "first", 180), (0, "first", 240), (0, "second", 240)])

    def test_deadline_limits_wait_and_expiry_is_error(self):
        deadline = AttemptDeadline(1, started=time.monotonic() - 0.5)
        self.assertLessEqual(deadline.allowance(10), 0.5)
        expired = AttemptDeadline(1, started=time.monotonic() - 2)
        with self.assertRaises(ToolError):
            expired.remaining()

    def test_resume_can_rewind_only_this_phone_to_its_current_screen(self):
        session = PostMenuSession("batch", 0, "q1")
        calls = []
        job = RunJob(0, "batch", None)
        first = (PostMenuStep("b4", lambda *_: calls.append("b4")),
                 PostMenuStep("b5", lambda *_: calls.append("b5")))
        session.state = "PAUSED"
        session.next_step = 1
        session.attempts = 1
        observed = []

        def reconcile(current, active_job, deadline, stop):
            observed.append((current, active_job.index, deadline.seconds))
            return 0, first

        session.run(job, first, lambda *_: None, threading.Event(),
                    reconcile=reconcile)
        self.assertEqual(observed, [(1, 0, 240)])
        self.assertEqual(calls, ["b4", "b5"])
        self.assertEqual((session.state, session.next_step), ("DONE", 2))

    def test_first_attempt_clock_starts_when_menu_was_confirmed(self):
        session = PostMenuSession("batch", 0, "q1",
                                  menu_opened_at=time.monotonic() - 181)
        called = []
        session.run(RunJob(0, "batch", None),
                    (PostMenuStep("first", lambda *_: called.append(True)),),
                    lambda *_: None, threading.Event())
        self.assertEqual((session.state, session.next_step, session.attempts),
                         ("PAUSED", 0, 1))
        self.assertEqual(called, [])

    def test_types_one_character_at_a_time_without_clipboard(self):
        phone = CloudPhone("127.0.0.1:5001")
        with patch("amazon_android.post_menu.cloud_adb",
                   return_value=SimpleNamespace(returncode=0)) as adb:
            type_characters(phone, "A 1!", AttemptDeadline(180), threading.Event())
        self.assertEqual(adb.call_count, 4)
        commands = [call.kwargs["input_text"] for call in adb.call_args_list]
        self.assertEqual(commands, ["input text A\n", "input text %s\n",
                                    "input text 1\n", "input text '!'\n"])
        self.assertTrue(all(call.args[:2] == (phone, "shell")
                            for call in adb.call_args_list))

    def test_unsupported_character_stops_before_typing(self):
        with patch("amazon_android.post_menu.cloud_adb") as adb:
            with self.assertRaises(ToolError):
                type_characters(CloudPhone("127.0.0.1:5001"), "Tên",
                                AttemptDeadline(180), threading.Event())
        adb.assert_not_called()


if __name__ == "__main__":
    unittest.main()
