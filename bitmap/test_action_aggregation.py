#coding:utf-8

import unittest

from redis import Redis
from action_recorder import ActionRecorder
from action_aggregation import ActionAggregation

class TestActionAggregation(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        # recorders

        self.day_1_online = ActionRecorder(self.client, "day_1_online")
        self.day_2_online = ActionRecorder(self.client, "day_2_online")

        # data

        self.day_1_online.perform_by(10086)
        self.day_1_online.perform_by(12345)

        self.day_2_online.perform_by(10086)

        # aggregation object

        self.agg = ActionAggregation(self.client)

    def test_calc_and(self):
        self.agg.calc_and("two_days_online", "day_1_online", "day_2_online")

        self.result = ActionRecorder(self.client, "two_days_online")

        self.assertTrue(
            self.result.is_performed(10086)
        )

        self.assertEqual(
            self.result.count_performed(),
            1
        )

    def test_calc_or(self):
        self.agg.calc_or("atleast_one_day_online", "day_1_online", "day_2_online")

        self.result = ActionRecorder(self.client, "atleast_one_day_online")

        self.assertTrue(
            self.result.is_performed(10086)
        )
        self.assertTrue(
            self.result.is_performed(12345)
        )

        self.assertEqual(
            self.result.count_performed(),
            2
        )

    def test_calc_xor(self):
        self.agg.calc_xor("only_one_day_online", "day_1_online", "day_2_online")

        self.result = ActionRecorder(self.client, "only_one_day_online")

        self.assertTrue(
            self.result.is_performed(12345)
        )

        self.assertEqual(
            self.result.count_performed(),
            1
        )

    def test_calc_not(self):
        self.agg.calc_not("not_online_in_day_2", "day_2_online")

        self.result = ActionRecorder(self.client, "not_online_in_day_2")

        self.assertFalse(
            self.result.is_performed(12345)
        )

if __name__ == "__main__":
    unittest.main()
