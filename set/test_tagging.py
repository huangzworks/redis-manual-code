#coding:utf-8

import unittest

from redis import Redis
from tagging import Tagging

class TestTagging(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.article_tags = Tagging(self.client, "article::123")

    def test_add_and_is_included(self):
        self.assertFalse(
            self.article_tags.is_included("redis")
        )
        self.article_tags.add("redis")
        self.assertTrue(
            self.article_tags.is_included("redis")
        )

    def test_add_multi_element_in_once(self):
        self.article_tags.add("redis", "database", "nosql")
        self.assertTrue(
            self.article_tags.is_included("redis")
        )
        self.assertTrue(
            self.article_tags.is_included("database")
        )
        self.assertTrue(
            self.article_tags.is_included("nosql")
        )

    def test_remove(self):
        self.article_tags.add("redis")
        self.article_tags.remove("redis")
        self.assertFalse(
            self.article_tags.is_included("redis")
        )

    def test_remove_multi_elements_in_once(self):
        self.article_tags.add("redis", "database", "nosql")
        self.article_tags.remove("redis", "database", "nosql")
        self.assertFalse(
            self.article_tags.is_included("redis")
        )
        self.assertFalse(
            self.article_tags.is_included("database")
        )
        self.assertFalse(
            self.article_tags.is_included("nosql")
        )

    def test_get_all_tags(self):
        self.assertEqual(
            self.article_tags.get_all_tags(),
            set()
        )
        self.article_tags.add("redis", "database", "nosql")
        self.assertEqual(
            self.article_tags.get_all_tags(),
            {"redis", "database", "nosql"}
        )

    def test_count(self):
        self.assertEqual(
            self.article_tags.count(),
            0
        )
        self.article_tags.add("redis")
        self.assertEqual(
            self.article_tags.count(),
            1
        )

if __name__ == "__main__":
    unittest.main()
