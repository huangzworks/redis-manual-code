#coding:utf-8

import unittest

from redis import Redis
from cache import Cache

class TestCache(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.cache = Cache(self.client)

        self.key = "message"
        self.value = "hello world"
        self.another_value = "good morning"

    def test_get_return_none_when_key_not_set(self):
        self.assertIsNone(
            self.cache.get(self.key)
        )

    def test_set_and_get_works(self):
        self.cache.set(self.key, self.value)
        self.assertEqual(
            self.cache.get(self.key),
            self.value
        )

    def test_set_overwrite_exists_value(self):
        self.cache.set(self.key, self.value)
        self.cache.set(self.key, self.another_value)
        self.assertEqual(
            self.cache.get(self.key),
            self.another_value
        )

    def test_update_return_none_when_key_not_set(self):
        self.assertIsNone(
            self.cache.update(self.key, self.value)
        )
        self.assertEqual(
            self.cache.get(self.key),
            self.value
        )

    def test_update_return_old_value(self):
        self.cache.set(self.key, self.value)
        self.assertEqual(
            self.cache.update(self.key, self.another_value),
            self.value
        )

if __name__ == "__main__":
    unittest.main()
