#coding:utf-8

import unittest

from redis import Redis
from unique_counter import UniqueCounter

class TestUniqueCounter(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.counter = UniqueCounter(self.client, "unique-counter")

    def test_count_in(self):
        self.assertTrue(
            self.counter.count_in("a")
        )
        self.assertFalse(
            self.counter.count_in("a")
        )

    def test_get_result(self):
        self.assertEqual(
            self.counter.get_result(),
            0
        )
        self.counter.count_in("a")
        self.assertEqual(
            self.counter.get_result(),
            1
        )

if __name__ == "__main__":
    unittest.main()
