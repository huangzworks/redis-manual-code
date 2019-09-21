#coding:utf-8

import unittest

from redis import Redis
from like import Like

class TestLike(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.like = Like(self.client, "topic_12345::like")

    def test_cast(self):
        self.assertTrue(
            self.like.cast("peter")
        )
        self.assertFalse(
            self.like.cast("peter")
        )

    def test_is_liked(self):
        self.assertFalse(
            self.like.is_liked("peter")
        )
        self.like.cast("peter")
        self.assertTrue(
            self.like.is_liked("peter")
        )

    def test_undo(self):
        self.like.cast("peter")
        self.like.undo("peter")
        self.assertFalse(
            self.like.is_liked("peter")
        )

    def test_get_all_liked_users(self):
        self.assertEqual(
            self.like.get_all_liked_users(),
            set()
        )

        self.like.cast("peter")
        self.like.cast("jack")
        self.like.cast("mary")
        self.assertEqual(
            self.like.get_all_liked_users(),
            {"peter", "jack", "mary"}
        )

    def test_count(self):
        self.assertEqual(
            self.like.count(),
            0
        )
        self.like.cast("peter")
        self.assertEqual(
            self.like.count(),
            1
        )

if __name__ == "__main__":
    unittest.main()
