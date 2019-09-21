#coding:utf-8

import unittest

from redis import Redis
from lottery import Lottery

class TestLottery(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.lottery = Lottery(self.client, "test-lottery")

    def test_add_player(self):
        self.assertEqual(
            self.lottery.get_all_players(),
            set()
        )

        self.lottery.add_player("peter")

        self.assertNotEqual(
            self.lottery.get_all_players(),
            set()
        )

    def test_get_all_players(self):
        self.assertEqual(
            self.lottery.get_all_players(),
            set()
        )

        self.lottery.add_player("peter")

        self.assertEqual(
            self.lottery.get_all_players(),
            {"peter"}
        )

    def test_player_count(self):
        self.assertEqual(
            self.lottery.player_count(),
            0
        )

        self.lottery.add_player("peter")

        self.assertEqual(
            self.lottery.player_count(),
            1
        )

    def test_draw(self):
        player_list = {"peter", "jack", "tom"} 
        for player in player_list:
            self.lottery.add_player(player)

        # 确保获奖者的数量跟我们要求的一致
        self.assertEqual(
            len(self.lottery.draw(1)),
            1
        )

        self.assertEqual(
            len(self.lottery.draw(2)),
            2
        )

        # 确保获奖者来源于参与抽奖的玩家
        winner = self.lottery.draw(1)[0]
        self.assertTrue(
            winner in player_list
        )

if __name__ == "__main__":
    unittest.main()
