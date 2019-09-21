#coding:utf-8

import unittest

from redis import Redis
from zero_one_matrix import ZeroOneMatrix

class TestZeroOneMatrix(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.matrix = ZeroOneMatrix(self.client, "test-matrix", 4, 4)

    def test_set_and_get(self):
        self.assertEqual(
            self.matrix.get(2, 2),
            0
        )

        self.matrix.set(2, 2, 1)

        self.assertEqual(
            self.matrix.get(2, 2),
            1
        )

        self.matrix.set(2, 2, 0)

        self.assertEqual(
            self.matrix.get(2, 2),
            0
        )

    def test_raise_error_when_row_out_of_range(self):
        with self.assertRaises(ValueError):
            self.matrix.set(100, 2, 1)
        with self.assertRaises(ValueError):
            self.matrix.get(100, 2)

    def test_raise_error_when_col_out_of_range(self):
        with self.assertRaises(ValueError):
            self.matrix.set(2, 100, 1)
        with self.assertRaises(ValueError):
            self.matrix.get(2, 100)

if __name__ == "__main__":
    unittest.main()
