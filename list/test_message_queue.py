#coding:utf-8

import unittest

from time import time
from redis import Redis
from message_queue import MessageQueue

class TestMessageQueue(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.mq = MessageQueue(self.client, "mq")

        self.msg = "hello world"

        self.blocktime = 1

    def test_add(self):
        self.mq.add_message(self.msg)
        self.assertEqual(
            self.mq.len(),
            1
        )

    def test_get_message_non_block(self):
        self.mq.add_message(self.msg)
        self.assertEqual(
            self.mq.get_message(),
            self.msg
        )

    def test_get_message_blocking(self):
        before = time()
        print("blocking, wait for {0} second(s)".format(self.blocktime))
        self.assertIsNone(
            self.mq.get_message(self.blocktime)
        )
        self.assertTrue(
            time() - before >= self.blocktime
        )

    def test_len(self):
        self.assertEqual(
            self.mq.len(),
            0
        )

        self.mq.add_message(self.msg)

        self.assertEqual(
            self.mq.len(),
            1
        )

if __name__ == "__main__":
    unittest.main()
