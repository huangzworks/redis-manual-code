#coding:utf-8

import unittest

from redis import Redis
from relationship import Relationship

class TestRelationship(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.peter = Relationship(self.client, "peter")
        self.jack = Relationship(self.client, "jack")

    def test_follow(self):
        self.assertEqual(
            self.peter.get_all_following(),
            set()
        )
        self.assertEqual(
            self.jack.get_all_follower(),
            set()
        )

        self.peter.follow("jack")

        self.assertNotEqual(
            self.peter.get_all_following(),
            set()
        )
        self.assertNotEqual(
            self.jack.get_all_follower(),
            set()
        )

    def test_unfollow(self):
        self.peter.follow("jack")
        self.peter.unfollow("jack")

        self.assertEqual(
            self.peter.get_all_following(),
            set()
        )
        self.assertEqual(
            self.jack.get_all_follower(),
            set()
        )

    def test_is_following(self):
        self.assertFalse(
            self.peter.is_following("jack")
        )

        self.peter.follow("jack")

        self.assertTrue(
            self.peter.is_following("jack")
        )

    def test_get_all_following(self):
        self.assertEqual(
            self.peter.get_all_following(),
            set()
        )

        self.peter.follow("jack")

        self.assertEqual(
            self.peter.get_all_following(),
            {"jack"}
        )

    def test_get_all_follower(self):
        self.assertEqual(
            self.jack.get_all_follower(),
            set()
        )

        self.peter.follow("jack")

        self.assertEqual(
            self.jack.get_all_follower(),
            {"peter"}
        )

    def test_count_following(self):
        self.assertEqual(
            self.peter.count_following(),
            0
        )

        self.peter.follow("jack")

        self.assertEqual(
            self.peter.count_following(),
            1
        )

    def test_count_follower(self):
        self.assertEqual(
            self.jack.count_follower(),
            0
        )

        self.peter.follow("jack")

        self.assertEqual(
            self.jack.count_follower(),
            1
        )

if __name__ == "__main__":
    unittest.main()
