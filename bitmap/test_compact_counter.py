import unittest

from redis import Redis
from compact_counter import CompactCounter

class TestCompactCounter(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.c = CompactCounter(self.client, "counter", 16, True)

        self.index = 10086

    def tearDown(self):
        self.client = Redis()
        self.client.flushdb()

    def test_get(self):
        self.assertEqual(
            self.c.get(self.index),
            0
        )

    def test_increase(self):
        self.assertEqual(
            self.c.increase(self.index),
            1
        )

        self.assertEqual(
            self.c.increase(self.index, 100),
            101
        )

        self.assertEqual(
            self.c.get(self.index),
            101
        )

    def test_decrease(self):
        self.assertEqual(
            self.c.decrease(self.index),
            -1
        )

        self.assertEqual(
            self.c.decrease(self.index, 50),
            -51
        )

        self.assertEqual(
            self.c.get(self.index),
            -51
        )

if __name__ == "__main__":
    unittest.main()
