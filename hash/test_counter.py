#coding:utf-8

import unittest

from redis import Redis
from counter import Counter

class TestCounter(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()
        self.hash_key = "Counter::page_view"
        self.counter_name = "/user/peter"
        self.counter = Counter(self.client, self.hash_key, self.counter_name)

    def test_get_return_zero_when_counter_not_exists(self):
        self.assertEqual(
            self.counter.get(),
            0
        )
 
    def test_increase(self):
        self.counter.increase()
        self.assertEqual(
            self.counter.get(), 
            1
        )
        self.counter.increase(10)
        self.assertEqual(
            self.counter.get(),
            11
        )

    def test_decrease(self):
        self.counter.decrease()
        self.assertEqual(
            self.counter.get(),
            -1
        )
        self.counter.decrease(10)
        self.assertEqual(
            self.counter.get(),
            -11
        )

    def test_reset(self):
        self.counter.increase(10086)
        self.counter.reset()
        self.assertEqual(
            self.counter.get(),
            0
        )

if __name__ == "__main__":
    unittest.main()
