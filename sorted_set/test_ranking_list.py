#coding:utf-8

import unittest

from redis import Redis
from ranking_list import RankingList

class TestRankingList(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.music_ranking = RankingList(self.client, "today_music_ranking")

    def bulk_set_score(self):
        self.music_ranking.set_score("song1", 10)
        self.music_ranking.set_score("song2", 20)
        self.music_ranking.set_score("song3", 30)
        self.music_ranking.set_score("song4", 40)
        self.music_ranking.set_score("song5", 50)

    def test_get_score_when_item_not_exists(self):
        self.assertIsNone(
            self.music_ranking.get_score("song1")
        )

    def test_set_score_and_get_score(self):
        self.music_ranking.set_score("song1", 10)

        self.assertEqual(
            self.music_ranking.get_score("song1"),
            10
        )

    def test_set_score_when_item_exists(self):
        self.music_ranking.set_score("song1", 10)

        self.music_ranking.set_score("song1", 20)

        self.assertEqual(
            self.music_ranking.get_score("song1"),
            20
        )

    def test_remove(self):
        self.music_ranking.set_score("song1", 10)

        self.music_ranking.remove("song1")

        self.assertIsNone(
            self.music_ranking.get_score("song1")
        )

    def test_increase_score(self):
        self.music_ranking.set_score("song1", 10)

        self.music_ranking.increase_score("song1", 20)

        self.assertEqual(
            self.music_ranking.get_score("song1"),
            30
        )

    def test_decrease_score(self):
        self.music_ranking.set_score("song1", 35)

        self.music_ranking.decrease_score("song1", 22)

        self.assertEqual(
            self.music_ranking.get_score("song1"),
            13
        )

    def test_get_rank(self):
        self.bulk_set_score()
        self.assertEqual(
            self.music_ranking.get_rank("song1"),
            5
        )
        self.assertEqual(
            self.music_ranking.get_rank("song5"),
            1
        )

    def test_top(self):
        self.bulk_set_score()
        self.assertEqual(
            self.music_ranking.top(3),
            [
                "song5",
                "song4",
                "song3"
            ]
        )

    def test_top_with_score(self):
        self.bulk_set_score()
        self.assertEqual(
            self.music_ranking.top(3, True),
            [
                ("song5", 50),
                ("song4", 40),
                ("song3", 30)
            ]
        )

if __name__ == "__main__":
    unittest.main()
