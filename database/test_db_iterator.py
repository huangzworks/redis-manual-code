#coding:utf-8

import unittest

from redis import Redis
from db_iterator import DbIterator

class TestDbIterator(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.iterator = DbIterator(self.client)

    def create_keys(self):
        self.input_key_set = set()
        for i in range(100):
            key = "key{0}".format(i)
            value = i
            self.input_key_set.add(key)
            self.client.set(key, value)

    def test_next(self):
        self.create_keys()

        result_key_set = set()
        while True:
            result = self.iterator.next()
            if result is None:
                break
            print("Iterator return this keys: {0}".format(result))
            result_key_set |= set(result)
        self.assertEqual(
            self.input_key_set,
            result_key_set
        )

    def test_match_argument(self):
        filter_iterator = DbIterator(self.client, match="target:*")

        # 创建一些无关的键
        self.create_keys()

        # 创建以 "target:" 为前缀的键
        input_key_set = set()
        for i in range(10):
            key = "target:{0}".format(i)
            value = i
            self.client.set(key, value)
            input_key_set.add(key)

        # 迭代数据库中所有以 "target:" 为前缀的键
        result_key_set = set()
        while True:
            result = filter_iterator.next()
            if result is None:
                break
            result_key_set |= set(result)

        self.assertEqual(
            input_key_set,
            result_key_set
        ) 

    def test_count_argument(self):
        # 因为 SCAN 命令的 count 参数只是返回元素数量的参数的一个期望值
        # 所以我们这里不是直接检测迭代器返回的键数量，
        # 而是基于以下这个假设进行判断：
        # 对于 count 值小的迭代器，它进行的迭代次数将比 count 值大的迭代器要多
        small_iterator = DbIterator(self.client, count=1)
        big_iterator = DbIterator(self.client, count=100)

        small_count = big_count = 0

        while small_iterator.next() is not None:
            small_count +=1
        
        while big_iterator.next() is not None:
            big_count += 1

        self.assertTrue(
            small_count >= big_count
        )

if __name__ == "__main__":
    unittest.main()
