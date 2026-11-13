import threading
import unittest
from unittest.mock import patch

from amazon_android.cloud import CloudPhone
from amazon_android.core import ToolError
from amazon_android.post_menu import AttemptDeadline
from amazon_android.account_flow import (
    _button, _find_scrolling, _national_phone, _unique,
    build_common_steps, resume_common_index, screen,
)
from amazon_android.q1_flow import build_q1_steps
from amazon_android.q2_flow import build_q2_steps
from amazon_android.runner import AccountData, RunJob


def node(text, *, bounds="[10,10][200,50]", kind="android.widget.TextView"):
    return {"text": text, "bounds": bounds, "class": kind}


class Q1FlowTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone("127.0.0.1:5001")
        self.job = RunJob(0, "batch", None, account=AccountData(
            "12025550123", "Example User", "Example456!",
            "https://apifc.net/smsrecord?token=q1"))
        self.deadline = AttemptDeadline(180)
        self.stop = threading.Event()

    def test_classifies_supported_screens_and_stops_on_unknown(self):
        cases = [
            (["Shop by category."], "MENU"),
            (["Sign In", "Customer Service"], "MENU"),
            (["Sign in or create account", "Enter mobile number or email"],
             "IDENTIFIER"),
            (["Country/region code", "United States +1"], "COUNTRY"),
            (["Looks like you are new to Amazon", "Proceed to create an account"],
             "NEW_ACCOUNT"),
            (["Create account", "First and last name"], "CREATE_FORM"),
            (["Verify with WhatsApp", "Send code by SMS"], "WHATSAPP"),
            (["Verify mobile number", "Enter security code"], "SMS"),
            (["Something unexpected"], "UNKNOWN"),
        ]
        for labels, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(screen([node(label) for label in labels]), expected)

    def test_ambiguous_button_stops_instead_of_guessing(self):
        with self.assertRaises(ToolError):
            _unique([node("Continue", bounds="[0,0][100,40]"),
                     node("Continue", bounds="[0,50][100,90]")], "Continue")

    def test_accessibility_description_can_identify_a_button(self):
        button = {"text": "", "content-desc": "Send code by SMS",
                  "bounds": "[0,0][100,40]"}
        self.assertIs(_unique([button], "Send code by SMS"), button)

    def test_visible_continue_is_chosen_over_hidden_duplicate(self):
        hidden = node("Continue", bounds="[0,0][0,0]")
        button = node("Continue", bounds="[20,470][350,520]",
                      kind="android.widget.Button")
        button["clickable"] = "true"
        field = node("", bounds="[30,210][350,250]",
                     kind="android.widget.EditText")
        self.assertIs(_button([hidden, button], "Continue", below=field), button)

    def test_country_scrolls_past_hidden_us_entry(self):
        hidden = node("United States +1", bounds="[0,0][0,0]")
        visible = node("United States +1", bounds="[50,320][320,360]")
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[[hidden, node("Ukraine +380")], [visible]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll:
            result = _find_scrolling(self.phone, "United States +1",
                                     self.deadline, self.stop)
        self.assertIs(result, visible)
        scroll.assert_called_once()

    def test_phone_uses_input_digits_then_checks_us_national_number(self):
        self.assertEqual(_national_phone(self.job), "2025550123")

    def test_only_first_three_steps_are_q1_specific(self):
        q1 = build_q1_steps(self.phone, lambda code: None)
        common = build_common_steps(self.phone, lambda code: None)
        self.assertEqual([step.name for step in q1[:3]],
                         ["b1 Gifting", "b2 Pets", "b3 Fashion and Beauty"])
        self.assertEqual([step.name for step in q1[3:]],
                         [step.name for step in common])
        self.assertEqual(common[0].name, "b4 Sign In")

    def test_b4_focuses_phone_field_on_existing_identifier_screen(self):
        field = node("", kind="android.widget.EditText")
        identifier = [node("Sign in or create account"),
                      node("Enter mobile number or email"), field]
        sign_in = build_common_steps(self.phone, lambda code: None)[0].action
        with patch("amazon_android.account_flow._read_nodes",
                   return_value=identifier), \
             patch("amazon_android.account_flow._tap") as tap:
            sign_in(self.job, self.deadline, self.stop)
        self.assertIs(tap.call_args.args[1], field)

    def test_paused_q1_and_q2_rewind_from_b10_to_shared_b4(self):
        identifier = [node("Sign in or create account"),
                      node("Enter mobile number or email")]
        with patch("amazon_android.account_flow._read_nodes",
                   return_value=identifier):
            for factory in (build_q1_steps, build_q2_steps):
                steps = factory(self.phone, lambda code: None)
                current = next(i for i, step in enumerate(steps)
                               if step.name.startswith("b10"))
                target = resume_common_index(self.phone, steps, current,
                                             self.deadline, self.stop)
                self.assertEqual(steps[target].name, "b4 Sign In")

    def test_common_sms_steps_keep_each_machine_url_and_state(self):
        second = RunJob(1, "batch", None, account=AccountData(
            "12025550124", "Second User", "Example456!",
            "https://apifc.net/smsrecord?token=q2"))
        first_send = next(step.action for step in build_common_steps(
            self.phone, lambda code: None) if step.name.startswith("b10"))
        second_send = next(step.action for step in build_common_steps(
            CloudPhone("127.0.0.1:5002"), lambda code: None)
            if step.name.startswith("b10"))
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS")]
        sms = [node("Verify mobile number"), node("Enter security code")]
        with patch("amazon_android.account_flow._read_nodes", return_value=whatsapp), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._wait_screen", return_value=sms):
            first_send(self.job, self.deadline, self.stop)
            second_send(second, self.deadline, self.stop)
        self.assertEqual(tap.call_count, 2)

    def test_sms_is_not_sent_twice_after_uncertain_transition(self):
        steps = build_q1_steps(self.phone, lambda code: None)
        send_sms = next(step.action for step in steps if step.name.startswith("b10"))
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS")]
        with patch("amazon_android.account_flow._read_nodes", return_value=whatsapp), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._wait_screen",
                   side_effect=ToolError("slow screen")):
            with self.assertRaises(ToolError):
                send_sms(self.job, self.deadline, self.stop)
            with self.assertRaisesRegex(ToolError, "Đã bấm gửi SMS"):
                send_sms(self.job, self.deadline, self.stop)
        tap.assert_called_once()

    def test_sms_screen_after_manual_send_continues_without_second_tap(self):
        statuses = []
        send_sms = next(step.action for step in build_common_steps(
            self.phone, lambda code: None, statuses.append)
            if step.name.startswith("b10"))
        sms = [node("Verify mobile number"), node("Enter security code")]
        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow._tap") as tap:
            send_sms(self.job, self.deadline, self.stop)
        tap.assert_not_called()
        self.assertEqual(statuses, ["Đang chờ mã"])

    def test_create_button_is_after_otp_deadline(self):
        steps = build_q1_steps(self.phone, lambda code: None)
        self.assertTrue(all(step.within_attempt for step in steps[:-1]))
        self.assertFalse(steps[-1].within_attempt)

    def test_sms_code_comes_from_q1_url_and_not_whatsapp(self):
        received = []
        statuses = []
        steps = build_q1_steps(self.phone, received.append, statuses.append)
        send_sms = next(step.action for step in steps if step.name.startswith("b10"))
        enter_otp = next(step.action for step in steps if step.name == "b11 nhập OTP")
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS")]
        sms = [node("Verify mobile number"), node("Enter security code"),
               node("Create your Amazon account")]
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[whatsapp, sms]), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._tap"), \
             patch("amazon_android.account_flow._wait_screen", return_value=sms):
            send_sms(self.job, self.deadline, self.stop)
        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow._field", return_value={"text": ""}), \
             patch("amazon_android.account_flow.wait_for_new_otp",
                   return_value="222222") as wait, \
             patch("amazon_android.account_flow._type_field") as typed:
            enter_otp(self.job, self.deadline, self.stop)
        self.assertEqual(received, ["222222"])
        self.assertEqual(statuses, ["Đang chờ mã", "Đã nhập mã"])
        self.assertEqual(wait.call_args.args[:2],
                         (self.job.account.otp_url, None))
        self.assertEqual(typed.call_args.args[2], "222222")

    def test_create_is_not_pressed_twice_after_screen_changes(self):
        create = build_q1_steps(self.phone, lambda code: None)[-1].action
        sms = [node("Verify mobile number"), node("Enter security code"),
               node("Create your Amazon account")]
        next_screen = [node("Next page")]
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[sms, next_screen, next_screen]), \
             patch("amazon_android.account_flow._field",
                   return_value={"text": "222222"}), \
             patch("amazon_android.account_flow._tap") as tap:
            create(self.job, AttemptDeadline(30), self.stop)
            create(self.job, AttemptDeadline(30), self.stop)
        tap.assert_called_once()


if __name__ == "__main__":
    unittest.main()
