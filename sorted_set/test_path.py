#coding:utf-8

import unittest

from redis import Redis
from path import Path

class TestPath(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.path = Path(self.client)

    def test_forward_to(self):
        self.assertEqual(
            self.path.pagging_record("a", 1, 10),
            []
        )
        
        self.path.forward_to("a", "b")

        result = self.path.pagging_record("a", 1, 10)

        self.assertNotEqual(
            result,
            []
        )

        self.assertEqual(
            result[0],
            "b"
        )

    def test_pagging_record(self):
        self.assertEqual(
            self.path.pagging_record("a", 1, 10),
            []
        )

        self.path.forward_to("a", "b")  # 访问 b 一次
        self.path.forward_to("a", "c")  # 访问 c 两次
        self.path.forward_to("a", "c")
        self.path.forward_to("a", "d")  # 访问 d 三次
        self.path.forward_to("a", "d")
        self.path.forward_to("a", "d")

        result = self.path.pagging_record("a", 1, 10)
        self.assertEqual(
            result,
            ["d", "c", "b"]
        )

        # more indexing test...
        self.assertEqual(
            self.path.pagging_record("a", 1, 1)[0],
            "d"
        )
        self.assertEqual(
            self.path.pagging_record("a", 2, 1)[0],
            "c"
        )

    def test_pagging_record_with_time(self):
        self.path.forward_to("a", "b")  # 访问 b 一次
        self.path.forward_to("a", "c")  # 访问 c 两次
        self.path.forward_to("a", "c")
        self.path.forward_to("a", "d")  # 访问 d 三次
        self.path.forward_to("a", "d")
        self.path.forward_to("a", "d")

        self.assertEqual(
            self.path.pagging_record("a", 1, 10, with_time=True),
            [("d", 3), ("c", 2), ("b", 1)]
        )
   

if __name__ == "__main__":
    unittest.main()
