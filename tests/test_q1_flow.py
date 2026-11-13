import threading
import unittest
from unittest.mock import patch

from amazon_android.cloud import CloudPhone
from amazon_android.core import AMAZON_PACKAGE, ToolError
from amazon_android.post_menu import AttemptDeadline, PostMenuSession
from amazon_android.account_flow import (
    _button, _find_scrolling, _national_phone, _parse_ui_nodes, _scroll_up, _unique,
    build_common_steps, menu_layout, resume_common_index,
    route_list_menu, screen,
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

    def test_list_menu_uses_live_text_structure_for_all_connected_machines(self):
        listed = [node(label) for label in (
            "Shop by Category", "Books", "Electronics", "Home services",
            "See all", "Customer Service", "Sign In")]
        cards = [node(label) for label in (
            "Shop by category", "Gifting", "Pets", "Fashion and Beauty")]
        self.assertEqual(menu_layout(listed), "LIST")
        self.assertEqual(menu_layout(cards), "CARDS")
        for factory in (build_q1_steps, build_q2_steps):
            steps = factory(self.phone, lambda _code: None)
            session = PostMenuSession("batch", 0, "q1")
            with patch("amazon_android.account_flow._read_nodes",
                       return_value=listed), \
                 patch("amazon_android.account_flow.visit_home") as home:
                target = route_list_menu(self.phone, steps, 0, session,
                                         self.deadline, self.stop)
            self.assertEqual(steps[target].name, "b4 Sign In")
            self.assertEqual(session.menu_route, "LIST")
            home.assert_called_once()
            with patch("amazon_android.account_flow._read_nodes",
                       return_value=cards), \
                 patch("amazon_android.account_flow.visit_home") as home:
                self.assertIsNone(route_list_menu(
                    self.phone, steps, 0, session, self.deadline, self.stop))
            self.assertEqual(session.menu_route, "")
            home.assert_not_called()

    def test_list_route_recovers_if_home_was_already_opened(self):
        steps = build_q2_steps(self.phone, lambda _code: None)
        session = PostMenuSession("batch", 1, "q2")
        session.menu_route = "LIST"
        home_nodes = [node("Sign in for the best experience")]
        with patch("amazon_android.account_flow._read_nodes",
                   return_value=home_nodes), \
             patch("amazon_android.account_flow.visit_home") as home:
            target = route_list_menu(self.phone, steps, 0, session,
                                     self.deadline, self.stop)
        self.assertEqual(steps[target].name, "b4 Sign In")
        home.assert_called_once()

    def test_shared_b4_returns_from_home_to_list_menu_sign_in(self):
        field = node("", kind="android.widget.EditText")
        home = [node("Sign in for the best experience")]
        listed = [node(label) for label in (
            "Shop by Category", "Books", "Electronics", "Customer Service",
            "Sign In")]
        identifier = [node("Sign in or create account"),
                      node("Enter mobile number or email"), field]
        sign_in, focus = build_common_steps(self.phone, lambda _code: None)[:2]
        with patch("amazon_android.account_flow._read_nodes", return_value=home), \
             patch("amazon_android.account_flow._ensure_menu",
                   return_value=listed) as ensure, \
             patch("amazon_android.account_flow._find_scrolling",
                   return_value=listed[-1]), \
             patch("amazon_android.account_flow._wait_screen",
                   return_value=identifier), \
             patch("amazon_android.account_flow._tap") as tap:
            sign_in.action(self.job, self.deadline, self.stop)
            tap.assert_called_once()
            focus.action(self.job, self.deadline, self.stop)
        ensure.assert_called_once()
        self.assertEqual(tap.call_count, 2)
        self.assertIs(tap.call_args_list[0].args[1], listed[-1])
        self.assertIs(tap.call_args_list[1].args[1], field)

    def test_b4_prefers_clickable_sign_in_when_tree_repeats_label(self):
        label = node("Sign In", bounds="[20,220][130,250]")
        row = node("Sign In", bounds="[20,530][340,580]",
                   kind="android.widget.Button")
        row["clickable"] = "true"
        menu = [node("Shop by Category"), node("Customer Service",
                                               bounds="[20,470][340,510]"),
                label, row]
        with patch("amazon_android.account_flow._read_nodes", return_value=menu):
            selected = _find_scrolling(self.phone, "Sign In", self.deadline,
                                       self.stop, menu_action=True)
        self.assertIs(selected, row)

    def test_b4_uses_customer_service_landmark_for_two_text_labels(self):
        other = node("Sign In", bounds="[20,220][130,250]")
        menu_row = node("Sign In", bounds="[20,530][340,580]")
        menu = [node("Shop by Category"), node("Customer Service",
                                               bounds="[20,470][340,510]"),
                other, menu_row]
        with patch("amazon_android.account_flow._read_nodes", return_value=menu):
            selected = _find_scrolling(self.phone, "Sign In", self.deadline,
                                       self.stop, menu_action=True)
        self.assertIs(selected, menu_row)

    def test_b4_stops_if_two_sign_in_rows_remain_below_landmark(self):
        menu = [node("Shop by Category"),
                node("Customer Service", bounds="[20,470][340,510]"),
                node("Sign In", bounds="[20,530][340,580]"),
                node("Sign In", bounds="[20,590][340,640]")]
        with patch("amazon_android.account_flow._read_nodes", return_value=menu):
            with self.assertRaises(ToolError):
                _find_scrolling(self.phone, "Sign In", self.deadline,
                                self.stop, menu_action=True)

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

    def test_name_continue_combines_nested_webview_controls(self):
        row = node("Continue", bounds="[20,470][350,520]")
        label = node("Continue", bounds="[140,480][230,510]")
        row["clickable"] = label["clickable"] = "true"
        field = node("Name", bounds="[30,210][350,250]")
        self.assertIs(_button([label, row], "Continue", below=field), row)

    def test_b9_selects_full_width_continue_among_separate_matches(self):
        field = node("Name", bounds="[30,210][350,250]")
        action = dict(node("Continue", bounds="[35,470][345,520]"), clickable="true")
        duplicate = dict(node("Continue", bounds="[120,525][240,555]"), clickable="true")
        self.assertIs(_button([duplicate, action], "Continue", below=field), action)
        another_action = dict(action, bounds="[35,530][345,580]")
        with self.assertRaises(ToolError):
            _button([action, another_action], "Continue", below=field)

    def test_b9_resolves_two_xml_labels_to_one_clickable_parent(self):
        xml = f'''<hierarchy>
          <node package="{AMAZON_PACKAGE}" clickable="true" bounds="[35,470][345,520]">
            <node package="{AMAZON_PACKAGE}" text="Continue" bounds="[120,478][240,500]" />
            <node package="{AMAZON_PACKAGE}" content-desc="Continue" bounds="[116,483][244,510]" />
          </node>
        </hierarchy>'''
        nodes = _parse_ui_nodes(xml)
        field = node("Name", bounds="[30,210][350,250]")
        self.assertIs(_button(nodes, "Continue", below=field), nodes[0])

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

    def test_b6_open_country_list_scrolls_before_tapping_us(self):
        country = [node("Country/region code")]
        hidden = node("United States +1", bounds="[0,0][0,0]")
        visible = node("United States +1", bounds="[50,320][320,360]")
        confirmed = [node("Sign in or create account"),
                     node("Enter mobile number or email"), node("US +1")]
        action = next(step.action for step in build_common_steps(
            self.phone, lambda _code: None) if step.name.startswith("b6"))
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[country, [hidden], [visible]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._wait_screen",
                   return_value=confirmed):
            action(self.job, self.deadline, self.stop)
        scroll.assert_called_once()
        self.assertIs(tap.call_args.args[1], visible)

    def test_b6_long_swipe_stays_inside_country_list(self):
        region = node("", bounds="[40,120][340,720]")
        region["scrollable"] = "true"
        with patch("amazon_android.account_flow.cloud_adb") as adb:
            _scroll_up(self.phone, [region], self.deadline, country_list=True, fling=True)
        _, _, _, _, x1, y1, x2, y2, duration = adb.call_args.args
        self.assertEqual(x1, x2)
        self.assertTrue(40 < int(x1) < 340)
        self.assertTrue(120 < int(y2) < int(y1) < 720)
        self.assertGreater(int(y1) - int(y2), 400)
        self.assertLessEqual(int(duration), 120)

    def test_b6_scrolls_back_if_fling_passes_us(self):
        target = node("United States +1")
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[[node("Afghanistan +93")],
                                [node("Zimbabwe +263")], [target]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch.object(self.stop, "wait", return_value=False):
            self.assertIs(_find_scrolling(self.phone, "United States +1",
                                          self.deadline, self.stop,
                                          country_list=True), target)
        self.assertTrue(scroll.call_args_list[0].kwargs["fling"])
        self.assertTrue(scroll.call_args_list[1].kwargs["reverse"])

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

    def test_b4a_focuses_phone_field_on_existing_identifier_screen(self):
        field = node("", kind="android.widget.EditText")
        identifier = [node("Sign in or create account"),
                      node("Continue"), field,
                      node("", kind="android.widget.EditText", bounds="[0,0][0,0]")]
        focus = build_common_steps(self.phone, lambda code: None)[1].action
        with patch("amazon_android.account_flow._read_nodes",
                   return_value=identifier), \
             patch("amazon_android.account_flow._tap") as tap:
            focus(self.job, self.deadline, self.stop)
        self.assertIs(tap.call_args.args[1], field)

    def test_b5_retries_focus_before_typing_phone_number(self):
        field = dict(node("", kind="android.widget.EditText"), focused="false")
        focused = dict(field, focused="true")
        filled = dict(focused, text=self.job.account.phone)
        heading = [node("Sign in or create account"), node("Continue")]
        steps = build_common_steps(self.phone, lambda _code: None)
        actions = []
        with patch("amazon_android.account_flow._read_nodes", side_effect=[
                heading + [field], heading + [field], heading + [focused],
                heading + [filled]]), \
             patch("amazon_android.account_flow._tap",
                   side_effect=lambda *_: actions.append("tap")), \
             patch("amazon_android.account_flow.type_characters",
                   side_effect=lambda *_: actions.append("type")):
            steps[2].action(self.job, self.deadline, self.stop)
        self.assertEqual(actions, ["tap", "tap", "type"])

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

    def test_b10_taps_sms_and_confirms_sms_screen_before_any_url_read(self):
        statuses = []
        action = next(step.action for step in build_common_steps(
            self.phone, lambda _code: None, statuses.append)
            if step.name.startswith("b10"))
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS")]
        sms = [node("Verify mobile number"), node("Enter security code")]
        order = []
        with patch("amazon_android.account_flow._read_nodes",
                   return_value=whatsapp), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._tap",
                   side_effect=lambda *_: order.append("tap SMS")), \
             patch("amazon_android.account_flow._wait_screen",
                   side_effect=lambda *_args, **_kwargs:
                       (order.append("SMS screen") or sms)), \
             patch("amazon_android.account_flow.wait_for_new_otp") as read:
            action(self.job, self.deadline, self.stop)
        self.assertEqual(order, ["tap SMS", "SMS screen"])
        self.assertEqual(statuses, ["Đang chờ mã"])
        read.assert_not_called()

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
             patch("amazon_android.account_flow.time.monotonic",
                   return_value=self.deadline.started + 1), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._tap"), \
             patch("amazon_android.account_flow._wait_screen", return_value=sms):
            send_sms(self.job, self.deadline, self.stop)
        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow.time.monotonic",
                   return_value=self.deadline.started + 2), \
             patch.object(self.stop, "wait", return_value=False) as delay, \
             patch("amazon_android.account_flow._field", return_value={"text": ""}), \
             patch("amazon_android.account_flow.wait_for_new_otp",
                   return_value="222222") as wait, \
             patch("amazon_android.account_flow._type_field") as typed:
            enter_otp(self.job, self.deadline, self.stop)
        delay.assert_called_once_with(3)
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
