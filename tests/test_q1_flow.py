import threading
import unittest
from types import SimpleNamespace
from subprocess import TimeoutExpired
from unittest.mock import patch

from PIL import Image, ImageDraw

from amazon_android.cloud import CloudPhone
from amazon_android.core import AMAZON_PACKAGE, ToolError
from amazon_android.post_menu import AttemptDeadline, PostMenuSession
from amazon_android.account_flow import (
    _button, _find_scrolling, _national_phone, _parse_ui_nodes, _read_nodes, _scroll_up, _unique,
    build_common_steps, menu_layout, resume_common_index,
    route_list_menu, screen, _yellow_form_button,
)
from amazon_android.q1_flow import build_q1_steps
from amazon_android.q2_flow import build_q2_steps
from amazon_android.runner import AccountData, RunJob


def node(text, *, bounds="[10,10][200,50]", kind="android.widget.TextView"):
    return {"text": text, "bounds": bounds, "class": kind}


class Q1FlowTests(unittest.TestCase):
    def test_b9_retries_continue_after_dismissing_visible_keyboard(self):
        field = node(self.job.account.full_name, kind="android.widget.EditText",
                     bounds="[30,210][350,250]")
        form = [node("Create account"), node("First and last name"), field]
        action = node("Continue", bounds="[35,470][345,520]")
        duplicate = node("Continue", bounds="[35,530][345,580]")
        b9 = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                  if step.name.startswith("b9"))
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[form + [action, duplicate], form + [action]]), \
             patch("amazon_android.account_flow._check_summary") as check, \
             patch("amazon_android.account_flow._wait_screen"), \
             patch("amazon_android.account_flow.cloud_adb",
                   return_value=SimpleNamespace(stdout="mInputShown=true")) as adb, \
             patch("amazon_android.account_flow._tap") as tap:
            b9(self.job, self.deadline, self.stop)
        self.assertEqual(adb.call_args.args[1:], ("shell", "input", "keyevent", "KEYCODE_BACK"))
        self.assertEqual(check.call_count, 2)
        self.assertEqual(tap.call_count, 1)
        self.assertIs(tap.call_args.args[1], action)

    def test_b8_recognizes_create_form_with_incomplete_accessibility_labels(self):
        controls = [node("Mobile number"), node("Continue"),
                    node("", kind="android.widget.EditText")]
        for landmark in (node("First and last name:"),
                         dict(node("Amazon"), **{"content-desc": "Create an account"})):
            with self.subTest(landmark=landmark):
                self.assertEqual(screen(controls + [landmark]), "CREATE_FORM")
        self.assertNotEqual(screen(controls), "CREATE_FORM")
        self.assertNotEqual(screen(controls + [node("First and last name"),
                          node("", kind="android.widget.EditText")]), "CREATE_FORM")

    def test_b8_resumes_on_create_form_without_tapping_again(self):
        form = [node("First and last name:"), node("Mobile number"), node("Continue"),
                node("", kind="android.widget.EditText")]
        b8 = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                  if step.name.startswith("b8"))
        with patch("amazon_android.account_flow._read_nodes", return_value=form), \
             patch("amazon_android.account_flow._tap") as tap:
            b8(self.job, self.deadline, self.stop)
        tap.assert_not_called()

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

    def test_b9_waits_for_name_readback_before_tapping_continue(self):
        action = node("Continue", bounds="[35,470][345,520]")
        heading = [node("Create account"), node("First and last name"), action]
        field = node("", kind="android.widget.EditText", bounds="[30,210][350,250]")
        value = self.job.account.full_name
        snapshots = [heading + [field], heading + [dict(field, text=value[:-1])],
                     heading + [dict(field, text=value)]]
        b9 = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                  if step.name.startswith("b9"))
        with patch("amazon_android.account_flow._read_nodes", side_effect=snapshots), \
             patch("amazon_android.account_flow._check_summary"), \
             patch("amazon_android.account_flow._wait_screen"), \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow.type_characters") as typed:
            b9(self.job, self.deadline, self.stop)
        typed.assert_called_once()
        self.assertEqual([call.args[1] for call in tap.call_args_list], [field, action])

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
                   side_effect=[country + [hidden], country + [visible], country + [visible]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch("amazon_android.account_flow._tap") as tap, \
             patch("amazon_android.account_flow._wait_screen",
                   return_value=confirmed):
            action(self.job, self.deadline, self.stop)
        scroll.assert_called_once()
        self.assertIs(tap.call_args.args[1], visible)

    def test_b6_checks_stable_us_row_and_recovers_from_sg_selection(self):
        heading = [node("Country/region code")]
        form = [node("Sign in or create account"), node("Enter mobile number or email")]
        moving = node("United States +1", bounds="[50,300][320,340]")
        settled = node("United States +1", bounds="[50,320][320,360]")
        sg = node("SG +65")
        end = heading + [node("Zimbabwe +263")]
        action = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                      if step.name.startswith("b6"))
        with patch("amazon_android.account_flow._read_nodes", side_effect=[
                heading + [moving], heading + [settled], heading + [settled],
                heading + [settled], heading + [settled]]), \
             patch("amazon_android.account_flow._wait_screen", side_effect=[
                 form + [sg], end, form + [node("US +1")]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch("amazon_android.account_flow._tap") as tap, \
             patch.object(self.stop, "wait", return_value=False):
            action(self.job, self.deadline, self.stop)
        self.assertEqual([call.args[1] for call in tap.call_args_list], [settled, sg, settled])
        self.assertTrue(scroll.call_args.kwargs["reverse"])

    def test_reads_current_ui_again_after_adb_timeout(self):
        error = ToolError("ADB timeout")
        error.__cause__ = TimeoutExpired("adb", 6)
        current = [node("United States +1")]
        with patch("amazon_android.account_flow._read_nodes_once",
                   side_effect=[error, current]) as read:
            self.assertEqual(_read_nodes(self.phone, self.deadline, self.stop), current)
        self.assertEqual(read.call_count, 2)

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
        self.assertLessEqual(int(duration), 70)

    def test_b6_scrolls_back_if_fling_passes_us(self):
        target = node("United States +1")
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[[node("Afghanistan +93")], [node("Japan +81")],
                                [node("Zimbabwe +263")], [target]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch.object(self.stop, "wait", return_value=False):
            self.assertIs(_find_scrolling(self.phone, "United States +1",
                                          self.deadline, self.stop,
                                          country_list=True), target)
        self.assertTrue(scroll.call_args_list[0].kwargs["fling"])
        self.assertTrue(scroll.call_args_list[1].kwargs["fling"])
        self.assertTrue(scroll.call_args_list[2].kwargs["reverse"])

    def test_b6_reverses_when_forward_swipe_no_longer_moves_list(self):
        last = [node("Wallis and Futuna +681")]
        target = node("United States +1")
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[[node("United Kingdom +44")], last, last, last, [target]]), \
             patch("amazon_android.account_flow._scroll_up") as scroll, \
             patch.object(self.stop, "wait", return_value=False):
            self.assertIs(_find_scrolling(self.phone, "United States +1",
                                          self.deadline, self.stop,
                                          country_list=True), target)
        self.assertFalse(scroll.call_args_list[0].kwargs["reverse"])
        self.assertEqual([call.kwargs["reverse"] for call in scroll.call_args_list[1:]],
                         [True, True, True])

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

    def test_sms_tap_timeout_checks_next_screen_without_resending(self):
        error = ToolError("ADB timeout")
        error.__cause__ = TimeoutExpired("adb", 6)
        whatsapp = [node("Verify with WhatsApp"), node("Send code by SMS"),
                    node(self.job.account.phone)]
        sms = [node("Verify mobile number"), node("Enter security code")]
        send_sms = next(step.action for step in build_common_steps(self.phone, lambda _: None)
                        if step.name.startswith("b10"))
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[whatsapp, sms]), \
             patch("amazon_android.account_flow._tap", side_effect=error) as tap:
            send_sms(self.job, self.deadline, self.stop)
        tap.assert_called_once()

    def test_incomplete_ui_dump_is_read_again_before_using_controls(self):
        incomplete = SimpleNamespace(returncode=0, stdout="<hierarchy>")
        valid = SimpleNamespace(returncode=0, stdout=
            f'<hierarchy><node package="{AMAZON_PACKAGE}" text="Continue" /></hierarchy>')
        with patch("amazon_android.account_flow.cloud_adb", side_effect=[
                incomplete, incomplete, valid, valid]) as adb:
            result = _read_nodes(self.phone, self.deadline, self.stop)
        self.assertEqual(result[0]["text"], "Continue")
        self.assertEqual(adb.call_count, 4)

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
               node("Create your Amazon account"), node(self.job.account.phone)]
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
             patch("amazon_android.account_flow._field", return_value={"text": ""}), \
             patch("amazon_android.account_flow.wait_for_new_otp",
                   return_value="222222") as wait, \
             patch("amazon_android.account_flow._type_field") as typed:
            enter_otp(self.job, self.deadline, self.stop)
        self.assertEqual(wait.call_args.kwargs["not_before"], self.deadline.started + 5)
        self.assertEqual(received, ["222222"])
        self.assertEqual(statuses, ["Đang chờ mã", "Đã nhập mã"])
        self.assertEqual(wait.call_args.args[:2],
                         (self.job.account.otp_url, None))
        self.assertEqual(typed.call_args.args[2], "222222")

    def test_b11_taps_otp_field_even_when_provider_read_fails(self):
        field = node("", kind="android.widget.EditText", bounds="[30,210][350,250]")
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone), field]
        steps = {step.name: step.action for step in build_common_steps(self.phone, lambda _: None)}
        actions = []

        def provider_read(*_args, **_kwargs):
            actions.append("read")
            raise ToolError("Provider unavailable")

        with patch("amazon_android.account_flow._read_nodes", return_value=sms), \
             patch("amazon_android.account_flow._tap",
                   side_effect=lambda _phone, target, _deadline: actions.append(target)), \
             patch("amazon_android.account_flow.wait_for_new_otp", side_effect=provider_read), \
             patch("amazon_android.account_flow.type_characters") as typed:
            steps["b10 Send code by SMS"](self.job, self.deadline, self.stop)
            steps["b11a chạm ô OTP"](self.job, self.deadline, self.stop)
            with self.assertRaisesRegex(ToolError, "Provider unavailable"):
                steps["b11 nhập OTP"](self.job, self.deadline, self.stop)
        self.assertEqual(actions, [field, "read"])
        typed.assert_not_called()

    def test_b11_restores_otp_focus_after_browser_returns(self):
        field = dict(node("", kind="android.widget.EditText", bounds="[30,210][350,250]"),
                     focused="false")
        focused = dict(field, focused="true")
        filled = dict(focused, text="222222")
        heading = [node("Verify mobile number"), node("Enter security code"),
                   node(self.job.account.phone)]
        steps = {step.name: step.action for step in build_common_steps(self.phone, lambda _: None)}
        actions = []
        with patch("amazon_android.account_flow._read_nodes", side_effect=[
                heading + [field], heading + [focused], heading + [field],
                heading + [field], heading + [focused], heading + [filled]]), \
             patch("amazon_android.account_flow._tap", side_effect=lambda *_: actions.append("tap")), \
             patch("amazon_android.account_flow.wait_for_new_otp", return_value="222222"), \
             patch("amazon_android.account_flow.type_characters",
                   side_effect=lambda _phone, value, *_: actions.append(value)):
            steps["b10 Send code by SMS"](self.job, self.deadline, self.stop)
            steps["b11 nhập OTP"](self.job, self.deadline, self.stop)
        self.assertEqual(actions, ["tap", "tap", "222222"])

    def test_create_is_not_pressed_twice_after_screen_changes(self):
        create = build_q1_steps(self.phone, lambda code: None)[-1].action
        sms = [node("Verify mobile number"), node("Enter security code"),
               node("Create your Amazon account"), node(self.job.account.phone)]
        next_screen = [node("Next page")]
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[sms, next_screen, next_screen]), \
             patch("amazon_android.account_flow._field",
                   return_value=node("222222", bounds="[10,1][200,9]")), \
             patch("amazon_android.account_flow._tap") as tap:
            create(self.job, AttemptDeadline(30), self.stop)
            create(self.job, AttemptDeadline(30), self.stop)
        tap.assert_called_once()

    def test_visual_fallback_accepts_one_yellow_form_button_and_rejects_two(self):
        field = node("", bounds="[25,100][335,140]")
        with Image.new("RGB", (360, 640), "white") as image:
            draw = ImageDraw.Draw(image)
            draw.rounded_rectangle((25, 330, 334, 369), radius=18, fill="#ffd814")
            draw.text((150, 345), "Continue", fill="black")
            result = _yellow_form_button(image, field)
            self.assertEqual(result["bounds"], "[25,330][335,370]")
            draw.rounded_rectangle((25, 240, 334, 279), radius=18, fill="#ffd814")
            with self.assertRaisesRegex(ToolError, "nút vàng"):
                _yellow_form_button(image, field)
            self.assertEqual(_yellow_form_button(image, field, labels=((140, 342, 220, 358),)),
                             result)

    def test_create_uses_visual_fallback_only_for_matching_phone_and_taps_once(self):
        create = build_common_steps(self.phone, lambda _: None)[-1].action
        otp = node("222222", kind="android.widget.EditText", bounds="[25,100][335,140]")
        sms = [node("Verify mobile number"), node("Enter security code"),
               node(self.job.account.phone), otp]
        wrong_phone = sms[:2] + [otp]
        button = node("", bounds="[25,155][335,195]")
        next_screen = [node("Next page")]
        with patch("amazon_android.account_flow._read_nodes",
                   side_effect=[wrong_phone, sms, next_screen, next_screen]), \
             patch("amazon_android.account_flow._visual_form_button", return_value=button) as visual, \
             patch("amazon_android.account_flow._tap") as tap:
            with self.assertRaisesRegex(ToolError, "SĐT"):
                create(self.job, self.deadline, self.stop)
            visual.assert_not_called()
            create(self.job, self.deadline, self.stop)
            create(self.job, self.deadline, self.stop)
        visual.assert_called_once_with(self.phone, sms, "Create your Amazon account", otp,
                                      self.deadline)
        tap.assert_called_once_with(self.phone, button, self.deadline)


if __name__ == "__main__":
    unittest.main()
