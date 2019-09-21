#coding:utf-8

import unittest

from redis import Redis
from relationship import Relationship
from recommend_follow import RecommendFollow

class TestRecommendFollow(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        # user
        self.peter = Relationship(self.client, "peter")

        # targets
        self.jack = Relationship(self.client, "jack")
        self.tom = Relationship(self.client, "tom")
        self.mary = Relationship(self.client, "mary")
        self.david = Relationship(self.client, "david")
        self.sam = Relationship(self.client, "sam")

        # user follow targets
        self.peter.follow("jack")
        self.peter.follow("tom")
        self.peter.follow("mary")
        self.peter.follow("david")
        self.peter.follow("sam")

        # create ten following user for each target
        self.jack_following_set = set()
        self.tom_following_set = set()
        self.mary_following_set = set()
        self.david_following_set = set()
        self.sam_following_set = set()
        for i in range(10):
            self.jack_following_set.add("J{0}".format(i))
            self.tom_following_set.add("T{0}".format(i))
            self.mary_following_set.add("M{0}".format(i))
            self.david_following_set.add("D{0}".format(i))
            self.sam_following_set.add("S{0}".format(i))

        for target in list(self.jack_following_set):
            self.jack.follow(target)
        for target in list(self.tom_following_set):
            self.tom.follow(target)
        for target in list(self.mary_following_set):
            self.mary.follow(target)
        for target in list(self.david_following_set):
            self.david.follow(target)
        for sam in list(self.sam_following_set):
            self.sam.follow(target)

        #
        self.peter_recommend_follow = RecommendFollow(self.client, "peter")

    def test_calculate(self):
        self.assertEqual(
            self.peter_recommend_follow.fetch_result(10),
            []
        )

        self.peter_recommend_follow.calculate(2)

        self.assertNotEqual(
            self.peter_recommend_follow.fetch_result(10),
            []
        )

    def test_fetch_result(self):
        self.assertEqual(
            self.peter_recommend_follow.fetch_result(10),
            []
        )

        self.peter_recommend_follow.calculate(3)
 
        result = set(self.peter_recommend_follow.fetch_result(10))
        all_possible_recommend_targets = self.jack_following_set | self.tom_following_set | self.mary_following_set | self.david_following_set | self.sam_following_set
        self.assertNotEqual(
            result & all_possible_recommend_targets,
            set()
        )

    def test_delete_result(self):
        self.peter_recommend_follow.calculate(3)
        self.peter_recommend_follow.delete_result()

        self.assertEqual(
            self.peter_recommend_follow.fetch_result(10),
            []
        )


if __name__ == "__main__":
    unittest.main()
