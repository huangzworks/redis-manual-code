#coding:utf-8

import unittest

from redis import Redis
from auto_complete import AutoComplete

class TestAutoComplete(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.ac = AutoComplete(self.client)

    def test_feed_and_hint(self):
        self.ac.feed("黄晓明", 100)
        self.ac.feed("黄健翔", 70)
        self.ac.feed("黄健宏", 50)

        self.assertEqual(
            self.ac.hint("黄", 5),
            ["黄晓明", "黄健翔", "黄健宏"]
        )

        self.assertEqual(
            self.ac.hint("黄健", 5),
            ["黄健翔", "黄健宏"]
        )

        self.assertEqual(
            self.ac.hint("黄健", 1),
            ["黄健翔"]
        )

if __name__ == "__main__":
    unittest.main()
