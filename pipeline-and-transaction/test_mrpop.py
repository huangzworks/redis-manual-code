#coding:utf-8

import unittest

from redis import Redis
from mrpop import mrpop

class TestMrpop(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.list_key = "lst"

    def test_mrpop_return_nones_when_list_empty(self):
        self.assertEqual(
            mrpop(self.client, self.list_key, 3),
            [None, None, None]
        )

    def test_mrpop_return_items_when_list_not_empty(self):
        items = ["123", "456", "789"]
        self.client.rpush(self.list_key, *items)

        self.assertEqual(
            mrpop(self.client, self.list_key, 3),
            list(reversed(items))
        )

if __name__ == "__main__":
    unittest.main()
