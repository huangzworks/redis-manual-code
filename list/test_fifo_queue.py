#coding:utf-8

import unittest

from redis import Redis
from fifo_queue import FIFOqueue

class TestFIFOqueue(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.q = FIFOqueue(self.client, "my_queue")

    def test_dequeue_return_none_when_queue_empty(self):
        self.assertIsNone(
            self.q.dequeue()
        )

    def test_enqueue_and_dequeue(self):
        self.assertIsNotNone(
            self.q.enqueue("hello")
        )
        self.assertEqual(
            self.q.dequeue(),
            "hello"
        )

    def test_enqueue_return_right_number(self):
        for i in range(10):
            self.assertEqual(
                self.q.enqueue(i),
                i+1
            )

    def test_items_dequeue_in_fifo_order(self):
        world_list = ["hello", "world", "again"]
        for item in world_list:
            self.q.enqueue(item)
        for i in range(3):
            self.assertEqual(
                self.q.dequeue(),
                world_list[i]
            )

if __name__ == "__main__":
    unittest.main()
