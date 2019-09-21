#coding:utf-8

import unittest

from redis import Redis
from action_recorder import ActionRecorder

class TestActionRecorder(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.online_recorder = ActionRecorder(self.client, "8-10::online_users")

    def test_perform_by(self):
        self.assertEqual(
            self.online_recorder.count_performed(),
            0
        )

        self.online_recorder.perform_by(123)

        self.assertNotEqual(
            self.online_recorder.count_performed(),
            0
        )

    def test_is_performed_by(self):
        self.assertFalse(
            self.online_recorder.is_performed_by(123)
        )

        self.online_recorder.perform_by(123)

        self.assertTrue(
            self.online_recorder.is_performed_by(123)
        )

    def test_count_performed(self):
        self.assertEqual(
            self.online_recorder.count_performed(),
            0
        )

        self.online_recorder.perform_by(123)

        self.assertEqual(
            self.online_recorder.count_performed(),
            1
        )

if __name__ == "__main__":
    unittest.main()
