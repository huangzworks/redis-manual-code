#coding:utf-8

import unittest

from redis import Redis
from limiter import Limiter

class TestLimiter(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.limiter = Limiter(self.client, "limiter::ip")

    def test_set_max_execute_times_works(self):
        self.limiter.set_max_execute_times(3)

        self.assertIsNotNone(
            self.limiter.remaining_execute_times()
        )

    def test_remaining_execute_times_works(self):
        self.limiter.set_max_execute_times(3)

        self.assertEqual(
            self.limiter.remaining_execute_times(),
            3
        )

        self.limiter.still_valid_to_execute()

        self.assertEqual(
            self.limiter.remaining_execute_times(),
            2
        )

    def test_still_valid_to_execute_works(self):
        self.limiter.set_max_execute_times(3)

        for i in range(3):
            self.assertTrue(
                self.limiter.still_valid_to_execute()
            )

        self.assertFalse(
            self.limiter.still_valid_to_execute()
        )

if __name__ == "__main__":
    unittest.main()
