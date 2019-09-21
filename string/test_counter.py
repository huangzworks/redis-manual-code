#coding:utf-8

import unittest

from redis import Redis
from counter import Counter

class TestCounter(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.counter = Counter(self.client, 'test-counter')

    def test_increase_works(self):
        self.assertEqual(
            self.counter.increase(),
            1
        )

        self.assertEqual(
            self.counter.increase(5),
            6
        )

    def test_decrease_works(self):
        self.assertEqual(
            self.counter.decrease(),
            -1
        )

        self.assertEqual(
            self.counter.decrease(5),
            -6
        )

    def test_get_return_0_when_key_not_exists(self):
        self.assertEqual(
            self.counter.get(),
            0
        )

    def test_get_works(self):
        self.counter.increase(10)

        self.assertEqual(
            self.counter.get(),
            10
        )

    def test_reset_works(self):
        self.counter.increase(10)

        self.assertEqual(
            self.counter.reset(),
            10
        )

        self.assertEqual(
            self.counter.get(),
            0
        )

if __name__ == "__main__":
    unittest.main()
