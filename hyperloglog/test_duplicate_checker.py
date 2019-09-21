#coding:utf-8

import unittest

from redis import Redis
from duplicate_checker import DuplicateChecker

class TestDuplicateChecker(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.checker = DuplicateChecker(self.client, "test-duplicate-checker")

    def test_is_duplicated(self):
        self.assertFalse(
            self.checker.is_duplicated("hello")
        )

        self.assertTrue(
            self.checker.is_duplicated("hello")
        )

    def test_unique_count(self):
        self.assertEqual(
            self.checker.unique_count(),
            0
        )

        self.checker.is_duplicated("hello")

        self.assertEqual(
            self.checker.unique_count(),
            1
        )

if __name__ == "__main__":
    unittest.main()
