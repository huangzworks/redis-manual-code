#coding:utf-8

import unittest

from redis import Redis
from id_generator import IdGenerator

class TestIdGenerator(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.id_generator = IdGenerator(self.client, 'user::id')

    def test_produce_works(self):
        self.assertEqual(
            self.id_generator.produce(),
            1
        )
        self.assertEqual(
            self.id_generator.produce(),
            2
        )

    def test_reserve_return_true_when_produce_not_executed(self):
        self.assertTrue(
            self.id_generator.reserve(100)
        )

        self.assertEqual(
            self.id_generator.produce(),
            101
        )

    def test_reserve_return_false_when_produce_already_executed(self):
        self.id_generator.produce()

        self.assertFalse(
            self.id_generator.reserve(100)
        )

if __name__ == "__main__":
    unittest.main()
