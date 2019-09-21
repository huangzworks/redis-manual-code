#coding:utf-8

import unittest

from redis import Redis
from vote import Vote

class TestVote(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.vote = Vote(self.client, "question::10086")

    def test_vote_up(self):
        self.assertTrue(
            self.vote.vote_up("peter")
        )
        self.assertFalse(
            self.vote.vote_up("peter")
        )

    def test_vote_down(self):
        self.assertTrue(
            self.vote.vote_down("peter")
        )
        self.assertFalse(
            self.vote.vote_down("peter")
        )

    def test_vote_up_and_vote_down_return_false_when_already_voted(self):
        self.vote.vote_up("peter")
        self.assertFalse(
            self.vote.vote_down("peter")
        )
        self.vote.vote_down("jack")
        self.assertFalse(
            self.vote.vote_up("jack")
        )

    def test_is_voted(self):
        self.assertFalse(
            self.vote.is_voted("peter")
        )
        self.vote.vote_up("peter")
        self.assertTrue(
            self.vote.is_voted("peter")
        )

        self.assertFalse(
            self.vote.is_voted("jack")
        )
        self.vote.vote_down("jack")
        self.assertTrue(
            self.vote.is_voted("jack")
        )

    def test_undo(self):
        self.vote.vote_up("peter")
        self.vote.undo("peter")
        self.assertFalse(
            self.vote.is_voted("peter")
        )

        self.vote.vote_down("jack")
        self.vote.undo("jack")
        self.assertFalse(
            self.vote.is_voted("jack")
        )

    def test_vote_up_count(self):
        self.assertEqual(
            self.vote.vote_up_count(),
            0
        )
        self.vote.vote_up("peter")
        self.assertEqual(
            self.vote.vote_up_count(),
            1
        )

    def test_get_all_vote_up_users(self):
        self.assertEqual(
            self.vote.get_all_vote_up_users(),
            set()
        )
        self.vote.vote_up("peter")
        self.assertEqual(
            self.vote.get_all_vote_up_users(),
            {"peter"}
        )

    def test_vote_down_count(self):
        self.assertEqual(
            self.vote.vote_down_count(),
            0
        )
        self.vote.vote_down("jack")
        self.assertEqual(
            self.vote.vote_down_count(),
            1
        )

    def test_get_all_vote_down_users(self):
        self.assertEqual(
            self.vote.get_all_vote_down_users(),
            set()
        )
        self.vote.vote_down("jack")
        self.assertEqual(
            self.vote.get_all_vote_down_users(),
            {"jack"}
        )

if __name__ == "__main__":
    unittest.main()
