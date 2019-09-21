#coding:utf-8

import unittest

from redis import Redis
from location import Location

class TestLocation(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.location = Location(self.client)

        self.peter = {"long": 113.20996731519699, "lati": 23.593675019671288}
        self.jack = {"long": 113.22784155607224, "lati": 23.125598202060807}
        self.tom = {"long": 113.10631066560745, "lati": 23.00883120241354}

    def test_pin(self):
        self.assertIsNone(
            self.location.get("peter")
        )

        self.location.pin("peter", self.peter["long"], self.peter["lati"])

        self.assertIsNotNone(
            self.location.get("peter")
        )

    def test_get(self):
        self.assertIsNone(
            self.location.get("peter")
        )

        self.location.pin("peter", self.peter["long"], self.peter["lati"])

        self.assertEqual(
            self.location.get("peter"),
            (self.peter["long"], self.peter["lati"])
        )

    def test_calculate_distance(self):
        self.location.pin("peter", self.peter["long"], self.peter["lati"])
        self.location.pin("jack", self.jack["long"], self.jack["lati"])

        self.assertGreater(
            self.location.calculate_distance("peter", "jack"),
            0
        )
        self.assertLess(
            self.location.calculate_distance("peter", "jack"),
            100
        )

    def test_find_nearby(self):
        self.location.pin("peter", self.peter["long"], self.peter["lati"])
        self.location.pin("jack", self.jack["long"], self.jack["lati"])
        self.location.pin("tom", self.tom["long"], self.tom["lati"])

        self.assertEqual(
            len(self.location.find_nearby("peter", 50)),
            0
        )
        self.assertEqual(
            len(self.location.find_nearby("peter", 60)),
            1
        )
        self.assertEqual(
            len(self.location.find_nearby("peter", 70)),
            2
        )

    def test_random_nearby(self):
        self.location.pin("peter", self.peter["long"], self.peter["lati"])
        self.location.pin("jack", self.jack["long"], self.jack["lati"])
        self.location.pin("tom", self.tom["long"], self.tom["lati"])

        random_user = self.location.find_random_nearby("peter", 100)
        self.assertTrue(
            random_user == "jack" or random_user == "tom"
        )

if __name__ == "__main__":
    unittest.main()
