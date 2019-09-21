#coding:utf-8

import unittest

from redis import Redis
from stack2 import Stack

class TestStack(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.stack = Stack(self.client, "test-stack")

    def test_push(self):
        self.assertEqual(
            self.stack.push(1),
            1
        )
        self.assertEqual(
            self.stack.push(2),
            2
        )

    def test_pop_return_none_when_stack_empty(self):
        self.assertIsNone(
            self.stack.pop()
        )

    def test_pop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(
            self.stack.pop(),
            "2"
        )
        self.assertEqual(
            self.stack.pop(),
            "1"
        )

    def test_count(self):
        self.assertEqual(
            self.stack.count(),
            0
        )
        self.stack.push(1)
        self.assertEqual(
            self.stack.count(),
            1
        )

if __name__ == "__main__":
    unittest.main()
