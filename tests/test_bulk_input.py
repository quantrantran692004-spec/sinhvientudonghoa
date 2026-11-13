import unittest

from amazon_android.bulk_input import parse_column, parse_records
from amazon_android.core import ToolError


class BulkInputTests(unittest.TestCase):
    def test_proxy_rows_map_in_order(self):
        found = parse_column("proxy", "one.example:1001:u:p\ntwo.example:1002:u:q\n")
        self.assertEqual([(x.host, x.port) for x in found],
                         [("one.example", 1001), ("two.example", 1002)])

    def test_internal_blank_line_rejected_to_preserve_alignment(self):
        with self.assertRaises(ToolError):
            parse_column("name", "First\n\nThird")

    def test_password_whitespace_is_not_silently_changed(self):
        self.assertEqual(parse_column("password", "  value  \n"), ["  value  "])

    def test_markdown_table_imports_multiple_records_and_optional_proxy(self):
        rows = parse_records(
            "| Job 1 | +84901234567 | Pass1234 | Name One | one.example:1001:u:p |\n"
            "| --- | ---: | --- | --- | --- |\n"
            "| Job 2 | +84901234568 | Pass5678 | Name Two | two.example:1002:u:q |"
        )
        self.assertEqual([item.profile_name for item in rows], ["Job 1", "Job 2"])
        self.assertEqual(rows[1].full_name, "Name Two")
        self.assertEqual(rows[1].proxy.host, "two.example")

    def test_table_with_four_columns_keeps_proxy_optional(self):
        rows = parse_records("Job 1\t+84901234567\tPass1234\tName One")
        self.assertIsNone(rows[0].proxy)

    def test_three_column_markdown_table_assigns_q_profiles(self):
        rows = parse_records(
            "| 17624680931 | Example456! | Wilhelmina |\n"
            "| ----------: | --------- | ---------- |\n"
            "| 17624680932 | Example789! | Cordelia |"
        )
        self.assertEqual([item.profile_name for item in rows], ["q1", "q2"])
        self.assertEqual([item.phone for item in rows], ["17624680931", "17624680932"])
        self.assertEqual(rows[1].full_name, "Cordelia")

    def test_table_rejects_ambiguous_column_count(self):
        with self.assertRaises(ToolError):
            parse_records("17624680931,Example456!")

    def test_desktop_table_requires_exactly_three_columns(self):
        with self.assertRaises(ToolError):
            parse_records("Job 1,17624680931,Example456!,Name One",
                          three_columns_only=True)

    def test_desktop_otp_table_keeps_each_url_with_its_phone(self):
        rows = parse_records(
            "| SĐT | Mật khẩu | Tên | URL OTP |\n"
            "| --- | --- | --- | --- |\n"
            "| 17624680931 | Example456! | First | https://apifc.net/smsrecord?token=one |\n"
            "| 17624680932 | Example789! | Second | https://apifc.net/smsrecord?token=two |",
            account_table=True,
        )
        self.assertEqual([(row.profile_name, row.phone, row.otp_url) for row in rows], [
            ("q1", "17624680931", "https://apifc.net/smsrecord?token=one"),
            ("q2", "17624680932", "https://apifc.net/smsrecord?token=two"),
        ])
        self.assertNotIn("token=one", repr(rows[0]))

    def test_desktop_otp_table_requires_url_and_rejects_shared_token(self):
        with self.assertRaisesRegex(ToolError, "4 cột"):
            parse_records("17624680931,Example456!,First", account_table=True)
        with self.assertRaisesRegex(ToolError, "URL OTP"):
            parse_records("17624680931,Example456!,First,", account_table=True)
        with self.assertRaisesRegex(ToolError, "trùng"):
            parse_records(
                "17624680931,Example456!,First,https://apifc.net/smsrecord?token=same\n"
                "17624680932,Example789!,Second,https://apifc.net/smsrecord?token=same",
                account_table=True,
            )

    def test_expanded_markdown_table_maps_twelve_cards_and_otp_links_by_row(self):
        rows = []
        for index in range(12):
            url = f"https://apifc.net/smsrecord?token=synthetic{index:02d}"
            card = f"400000000000{index:04d}\\|12\\|2030"
            cells = [f"1202555{index:04d}", "Example456!", f"Name {index + 1}",
                     "", "", "", "", "", "", card, f"[{url}]({url})"]
            rows.append("| " + " | ".join(cells) + " |")
        separator = "| " + " | ".join(["---:"] + ["-"] * 10) + " |"
        rows.insert(1, separator)
        found = parse_records("\n".join(rows), account_table=True)
        self.assertEqual(len(found), 12)
        self.assertEqual([item.profile_name for item in found],
                         [f"q{index}" for index in range(1, 13)])
        for index, item in enumerate(found):
            self.assertEqual(item.phone, f"1202555{index:04d}")
            self.assertEqual(item.card, f"400000000000{index:04d}|12|2030")
            self.assertEqual(item.otp_url,
                             f"https://apifc.net/smsrecord?token=synthetic{index:02d}")
            self.assertNotIn(item.card, repr(item))

    def test_card_column_can_use_raw_pipes_and_rejects_extra_url(self):
        url = "https://apifc.net/smsrecord?token=synthetic"
        five_columns = parse_records(
            f"| 12025550123 | Example456! | Name | 4000000000000001\\|12\\|2030 | {url} |",
            account_table=True,
        )
        self.assertEqual(five_columns[0].card, "4000000000000001|12|2030")
        found = parse_records(
            f"| 12025550123 | Example456! | Name | 4000000000000001|12|2030 | {url} |",
            account_table=True,
        )
        self.assertEqual(found[0].card, "4000000000000001|12|2030")
        with self.assertRaisesRegex(ToolError, "đúng 1 URL OTP"):
            parse_records(
                f"| 12025550123 | Example456! | Name | {url} | {url} |",
                account_table=True,
            )


if __name__ == "__main__":
    unittest.main()
