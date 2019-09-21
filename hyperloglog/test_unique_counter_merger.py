#coding:utf-8

import unittest

from redis import Redis
from unique_counter_merger import UniqueCounterMerger

class TestUniqueCounterMerger(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        # key names
        self.h1 = 'h1'
        self.h2 = 'h2'
        self.h3 = 'h3'
        self.union = 'union-of-h1-h2-h3'

        # init data
        self.client.pfadd(self.h1, 'a', 'b', 'c')
        self.client.pfadd(self.h2, 'b', 'c', 'd')
        self.client.pfadd(self.h3, 'c', 'd', 'e')

        # object
        self.merger = UniqueCounterMerger(self.client)

    def test_merge(self):
        self.assertEqual(
            self.client.pfcount(self.union),
            0
        )

        self.client.pfmerge(self.union, self.h1, self.h2, self.h3)

        self.assertNotEqual(
            self.client.pfcount(self.union),
            0
        )

if __name__ == "__main__":
    unittest.main()
