#coding:utf-8

import unittest

from redis import Redis
from cache import Cache

class TestCache(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.cache = Cache(self.client, "hash-key")

    def test_set_and_get(self):
        self.assertIsNone(
            self.cache.get("msg")
        )
        self.cache.set("msg", "hello world")
        self.assertEqual(
            self.cache.get("msg"),
            "hello world"
        )

    def test_is_exists(self):
        self.assertFalse(
            self.cache.is_exists("msg")
        )
        self.cache.set("msg", "hello world")
        self.assertTrue(
            self.cache.is_exists("msg")
        )

    def test_size(self):
        self.assertEqual(
            self.cache.size(),
            0
        )
        self.cache.set("msg", "hello world")
        self.assertEqual(
            self.cache.size(),
            1
        )

    def test_delete(self):
        self.assertFalse(
            self.cache.delete("msg")
        )
        self.cache.set("msg", "hello world")
        self.assertTrue(
            self.cache.delete("msg")
        )

if __name__ == "__main__":
    unittest.main()
