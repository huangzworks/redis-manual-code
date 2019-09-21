#coding:utf-8

import unittest

from redis import Redis
from lottery2 import Lottery

class TestLottery(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
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

    def test_draw_return_specify_number_of_elements_1(self):
        # 确保获奖者的数量跟我们要求的一致
        # 因为 SPOP 会从抽奖者名单中移除获奖者
        # 所以这里使用了多个 case 进行测试
        player_list = {"peter", "jack", "tom"} 
        for player in player_list:
            self.lottery.add_player(player)

        self.assertEqual(
            len(self.lottery.draw(1)),
            1
        )

    def test_draw_return_specify_number_of_elements_2(self):
        # 确保获奖者的数量跟我们要求的一致
        player_list = {"peter", "jack", "tom"} 
        for player in player_list:
            self.lottery.add_player(player)

        self.assertEqual(
            len(self.lottery.draw(2)),
            2
        )

    def test_draw_result_come_from_players(self):
        player_list = {"peter", "jack", "tom"} 
        for player in player_list:
            self.lottery.add_player(player)

        winner = self.lottery.draw(1)[0]
        self.assertTrue(
            winner in player_list
        )

if __name__ == "__main__":
    unittest.main()
