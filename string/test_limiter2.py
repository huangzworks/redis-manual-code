#coding:utf-8

import unittest

from redis import Redis
from limiter2 import Limiter

class TestLimiter(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.max_execute_times = 3

        self.limiter = Limiter(self.client, "try_login")
        self.limiter.set_max_execute_times(self.max_execute_times)

    def test_set_max_execute_times_and_get_max_execute_times_works(self):
        self.assertEqual(
            self.limiter.get_max_execute_times(),
            self.max_execute_times
        )

    def test_get_current_execute_times_works(self):
        self.assertEqual(
            self.limiter.get_current_execute_times(),
            0
        )

    def test_still_valid_to_execute_works(self):
        for i in range(self.max_execute_times):
            self.assertTrue(
                self.limiter.still_valid_to_execute()
            )
        self.assertFalse(
            self.limiter.still_valid_to_execute()
        )

    def test_remaining_execute_times_works(self):
        self.assertEqual(
            self.limiter.remaining_execute_times(),
            self.max_execute_times
        )

    def test_reset_current_execute_times_works(self):
        self.limiter.still_valid_to_execute()
        self.limiter.reset_current_execute_times()
        self.assertEqual(
            self.limiter.remaining_execute_times(),
            self.max_execute_times
        )

if __name__ == "__main__":
    unittest.main()
