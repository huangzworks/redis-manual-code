#coding:utf-8

import unittest

from redis import Redis
from inverted_index import InvertedIndex

class TestInvertedIndex(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.laptops = InvertedIndex(self.client)

    def test_add_index(self):
        self.assertEqual(
            self.laptops.get_keywords("laptop1"),
            set()
        )

        self.laptops.add_index("laptop1", 10, "kw1", "kw2", "kw3")

        self.assertNotEqual(
            self.laptops.get_keywords("laptop1"),
            set()
        )

    def test_remove_index(self):
        self.laptops.add_index("laptop1", 10, "kw1", "kw2", "kw3")
        self.laptops.remove_index("laptop1", "kw1", "kw2")
        self.assertEqual(
            self.laptops.get_keywords("laptop1"),
            {"kw3"}
        )

    def test_get_keywords(self):
        self.assertEqual(
            self.laptops.get_keywords("laptop1"),
            set()
        )

        self.laptops.add_index("laptop1", 10, "kw1")
        self.assertEqual(
            self.laptops.get_keywords("laptop1"),
            {"kw1"}
        )

        self.laptops.add_index("laptop1", 10, "kw2", "kw3")
        self.assertEqual(
            self.laptops.get_keywords("laptop1"),
            {"kw1", "kw2", "kw3"}
        )

    def test_get_items_return_empty_list_when_no_related_items(self):
        self.assertEqual(
            self.laptops.get_items("kw1", "kw2", "kw3"),
            []
        )

    def test_get_items_only_return_items_with_give_keywords_in_orders(self):
        self.laptops.add_index("laptop1", 10, "kw1", "kw2", "kw3")
        self.laptops.add_index("laptop2", 20, "kw1", "kw2", "kw3")
        self.laptops.add_index("laptop3", 30, "kw4")

        self.assertEqual(
            self.laptops.get_items("kw1", "kw2", "kw3"),
            ["laptop2", "laptop1"]
        )

        self.assertEqual(
            self.laptops.get_items("kw4"),
            ["laptop3"]
        )

    def test_get_items_with_weight(self):
        self.laptops.add_index("laptop1", 10, "kw1", "kw2", "kw3")
        self.laptops.add_index("laptop2", 20, "kw1", "kw2", "kw3")
        self.laptops.add_index("laptop3", 30, "kw4")

        self.assertEqual(
            self.laptops.get_items_with_weight("kw1", "kw2", "kw3"),
            [("laptop2", 20), ("laptop1", 10)]
        )


if __name__ == "__main__":
    unittest.main()
