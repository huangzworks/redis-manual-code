#coding:utf-8

import unittest
from time import sleep

from redis import Redis
from location_with_cache import Location, RADIUS_CACHE_TIME

class TestLocation(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
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

    def test_cached_find_nearby(self):
        self.location.pin("peter", self.peter["long"], self.peter["lati"])
        self.location.pin("jack", self.jack["long"], self.jack["lati"])

        self.assertEqual(
            len(self.location.find_nearby("peter", 70)),
            1
        )

        # 因为缓存的作用，即使我们现在向 peter 附近添加一个新用户
        # find_nearby() 也还是会返回 1 个附近用户
        self.location.pin("tom", self.tom["long"], self.tom["lati"])
        self.assertEqual(
            len(self.location.find_nearby("peter", 70)),
            1
        )

        # 等待 60 秒钟，静候缓存过期
        print("Testing cache:")
        print("Sleep {0} seconds, wait for the cache to expire.".format(RADIUS_CACHE_TIME))
        sleep(RADIUS_CACHE_TIME)

        # 缓存过期之后，再次执行 find_nearby() 就会看见新添加的用户
        self.assertEqual(
            len(self.location.find_nearby("peter", 70)),
            2
        )

if __name__ == "__main__":
    unittest.main()
