#coding:utf-8

import unittest

from redis import Redis
from inverted_index import InvertedIndex

class TestInvertedIndex(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.laptops = InvertedIndex(self.client)

    def test_add_index(self):
        self.assertEqual(
            self.laptops.get_keywords("MacBook Pro MF840CH"),
            set()
        )

        self.laptops.add_index("MacBook Pro MF840CH", "Apple", "MacOS", "13.3inch")

        self.assertNotEqual(
            self.laptops.get_keywords("MacBook Pro MF840CH"),
            set()
        )

    def test_remove_index(self):
        self.laptops.add_index("MacBook Pro MF840CH", "Apple", "MacOS", "13.3inch")
        self.laptops.remove_index("MacBook Pro MF840CH", "Apple", "MacOS", "13.3inch")
        self.assertEqual(
            self.laptops.get_keywords("MacBook Pro MF840CH"),
            set()
        )

    def test_get_keywords(self):
        self.assertEqual(
            self.laptops.get_keywords("MacBook Pro MF840CH"),
            set()
        )

        self.laptops.add_index("MacBook Pro MF840CH", "Apple", "MacOS", "13.3inch")

        self.assertEqual(
            self.laptops.get_keywords("MacBook Pro MF840CH"),
            {"Apple", "MacOS", "13.3inch"}
        )

    def test_get_items(self):
        self.assertEqual(
            self.laptops.get_items("Apple"),
            set()
        )
        self.assertEqual(
            self.laptops.get_items("Apple", "MacOS"),
            set()
        )

        self.laptops.add_index("MacBook Pro MF840CH", "Apple", "MacOS", "13.3inch")
        self.laptops.add_index("MacBook Air MMGF2CH", "Apple", "MacOS", "13.3inch")

        self.assertEqual(
            self.laptops.get_items("Apple"),
            {"MacBook Pro MF840CH", "MacBook Air MMGF2CH"}
        )
        self.assertEqual(
            self.laptops.get_items("Apple", "MacOS", "13.3inch"),
            {"MacBook Pro MF840CH", "MacBook Air MMGF2CH"}
        )

if __name__ == "__main__":
    unittest.main()
