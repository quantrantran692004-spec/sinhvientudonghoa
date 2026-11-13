import unittest

from amazon_android.core import ToolError
from amazon_android.registration import _field_for_label


class RegistrationLocatorTests(unittest.TestCase):
    def test_name_and_password_bind_to_their_own_fields(self):
        nodes = [
            {"class": "android.widget.TextView", "text": "Your name", "bounds": "[20,10][300,40]"},
            {"class": "android.widget.EditText", "bounds": "[20,55][500,105]"},
            {"class": "android.widget.TextView", "text": "Password", "bounds": "[20,145][300,175]"},
            {"class": "android.widget.EditText", "bounds": "[20,190][500,240]"},
        ]
        self.assertEqual(_field_for_label(nodes, ("Your name",))["bounds"], "[20,55][500,105]")
        self.assertEqual(_field_for_label(nodes, ("Password",))["bounds"], "[20,190][500,240]")

    def test_unknown_field_stops_before_typing(self):
        with self.assertRaises(ToolError):
            _field_for_label([{"class": "android.widget.EditText", "bounds": "[0,0][100,50]"}],
                             ("Password",))


if __name__ == "__main__":
    unittest.main()
