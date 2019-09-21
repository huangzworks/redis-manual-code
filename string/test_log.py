#coding:utf-8

import unittest

from redis import Redis
from log import Log

class TestLog(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.log = Log(self.client, '25, March')

        self.log1 = "03:00 server up online"
        self.log2 = "03:15 handle request 1"
        self.log3 = "03:16 handle request 2"

    def test_add_works(self):
        self.assertTrue(
            len(self.log.get_all()) == 0
        )

        self.log.add(self.log1)

        self.assertTrue(
            len(self.log.get_all()) == 1
        )

    def test_get_all_works(self):
        self.assertEqual(
            self.log.get_all(),
            []
        )

        self.log.add(self.log1)
        self.log.add(self.log2)
        self.log.add(self.log3)

        result = self.log.get_all()

        self.assertEqual(
            self.log1,
            result[0]
        )

        self.assertEqual(
            self.log2,
            result[1],
        )

        self.assertEqual(
            self.log3,
            result[2]
        )

if __name__ == "__main__":
    unittest.main()
