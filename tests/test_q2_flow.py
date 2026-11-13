import unittest
from unittest.mock import Mock, patch

from amazon_android.cloud import CloudPhone
from amazon_android.post_menu import AttemptDeadline
from amazon_android.account_flow import build_common_steps
from amazon_android.q2_flow import build_q2_steps
from amazon_android.runner import AccountData, RunJob


class Q2FlowTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone("127.0.0.1:5002")
        self.job = RunJob(1, "batch", None, account=AccountData(
            "12025550124", "Second User", "Example456!",
            "https://apifc.net/smsrecord?token=q2"))
        self.deadline = AttemptDeadline(180)
        self.stop = Mock()
        self.stop.is_set.return_value = False

    def test_q2_has_its_own_first_three_steps_then_common_registration(self):
        steps = build_q2_steps(self.phone, lambda _code: None)
        common = build_common_steps(self.phone, lambda _code: None)
        self.assertEqual([step.name for step in steps[:3]],
                         ["b1 Trang chủ 2–5 giây", "b2 Menu ba gạch", "b3 Pets"])
        self.assertEqual([step.name for step in steps[3:]],
                         [step.name for step in common])

    def test_home_tap_is_verified_then_viewed_for_selected_seconds(self):
        menu = [{"text": "Shop by category", "content-desc": ""},
                {"text": "", "content-desc": "Home Tab, 1 of 4",
                 "bounds": "[0,700][100,800]"}]
        home = [{"text": "Sign in for the best experience",
                 "content-desc": ""}]
        action = build_q2_steps(self.phone, lambda _code: None)[0].action
        with patch("amazon_android.q2_flow._read_nodes", side_effect=[menu, home]), \
             patch("amazon_android.q2_flow._tap") as tap, \
             patch("amazon_android.q2_flow.random.choice", return_value=3):
            action(self.job, self.deadline, self.stop)
        tap.assert_called_once()
        self.stop.wait.assert_called_with(3)

    def test_menu_and_pets_use_current_ui(self):
        home = [{"text": "Sign in for the best experience",
                 "content-desc": ""},
                {"text": "", "content-desc": "Browse menu Tab, 4 of 4",
                 "bounds": "[300,700][400,800]"}]
        menu = [{"text": "Shop by category", "content-desc": ""}]
        steps = build_q2_steps(self.phone, lambda _code: None)
        with patch("amazon_android.q2_flow._read_nodes", return_value=home), \
             patch("amazon_android.q2_flow._tap") as tap, \
             patch("amazon_android.q2_flow._wait_screen", return_value=menu):
            steps[1].action(self.job, self.deadline, self.stop)
        tap.assert_called_once()
        with patch("amazon_android.q2_flow._read_nodes", return_value=menu), \
             patch("amazon_android.q2_flow._ensure_menu"), \
             patch("amazon_android.q2_flow._find_scrolling",
                   return_value={"text": "Pets", "bounds": "[0,0][10,10]"}), \
             patch("amazon_android.q2_flow._tap") as tap:
            steps[2].action(self.job, self.deadline, self.stop)
        tap.assert_called_once()


if __name__ == "__main__":
    unittest.main()
