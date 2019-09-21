#coding:utf-8

import unittest

from time import sleep

from redis import Redis
from auto_complete import AutoComplete

class TestAutoComplete(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.ac = AutoComplete(self.client)

        self.timeout = 3

    def test_feed_and_hint(self):
        self.ac.feed("黄晓明", 100)
        self.ac.feed("黄健翔", 70)
        self.ac.feed("黄健宏", 50)

        self.assertEqual(
            self.ac.hint("黄", 5),
            ["黄晓明", "黄健翔", "黄健宏"]
        )

        self.assertEqual(
            self.ac.hint("黄健", 5),
            ["黄健翔", "黄健宏"]
        )

        self.assertEqual(
            self.ac.hint("黄健", 1),
            ["黄健翔"]
        )

    def test_expire_feature_works(self):
        print("创建一个只存在 {0} 秒钟的自动补全结果。".format(self.timeout))
        self.ac.feed("Redis", timeout=self.timeout)
        i = self.timeout
        while i != 0:
            print("倒数 {0} 秒钟……".format(i))
            sleep(1)
            i -= 1

        self.assertEqual(
            self.ac.hint("Re", 10),
            []
        )
        print("时间到，自动补全结果已自动被移除！")

if __name__ == "__main__":
    unittest.main()
