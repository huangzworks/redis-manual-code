import unittest
from base36 import base10_to_base36

class TestBase10ToBase36(unittest.TestCase):

    def test_(self):
        self.assertEqual(
            base10_to_base36(0),
            "0"
        )

        self.assertEqual(
            base10_to_base36(10086),
            "7S6"
        )

        self.assertEqual(
            base10_to_base36(572921),
            "CA2H"
        )

if __name__ == "__main__":
    unittest.main()
