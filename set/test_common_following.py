#coding:utf-8

import unittest

from redis import Redis
from relationship import Relationship
from common_following import CommonFollowing

class TestCommonFollow(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.peter = Relationship(self.client, "peter")
        self.jack = Relationship(self.client, "jack")

        self.common_following = CommonFollowing(self.client)

    def follow_users(self):
        self.peter.follow("tom")
        self.peter.follow("mary")
        self.peter.follow("david")

        self.jack.follow("tom")
        self.jack.follow("mary")
        self.jack.follow("john")

    def test_calculate(self):
        self.assertEqual(
            self.common_following.calculate("peter", "jack"),
            set()
        )

        self.follow_users()
        
        self.assertEqual(
            self.common_following.calculate("peter", "jack"),
            {"tom", "mary"}
        )

    def test_calculate_and_store(self):
        self.assertEqual(
            self.client.smembers("peter-and-jack-common-follow"),
            set()
        )

        self.follow_users()

        self.assertEqual(
            self.common_following.calculate_and_store("peter", "jack", "peter-and-jack-common-follow"),
            2
        )
        self.assertEqual(
            self.client.smembers("peter-and-jack-common-follow"),
            {"tom", "mary"}
        )

if __name__ == "__main__":
    unittest.main()
