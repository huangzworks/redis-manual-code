#coding:utf-8

import unittest

from redis import Redis
from timeline import Timeline

class TestTimeline(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.tl = Timeline(self.client, "blog::timeline")

        self.blogs = [
            {"id": "blog::100", "time": 1000},
            {"id": "blog::101", "time": 1500},
            {"id": "blog::102", "time": 1550},
            {"id": "blog::103", "time": 1700},
            {"id": "blog::104", "time": 1750},
            {"id": "blog::105", "time": 2500}
        ]

        self.reversed_blogs = list(reversed(self.blogs))

    def test_add(self):
        self.assertEqual(
            self.tl.pagging(1, 10),
            []
        )
        
        self.tl.add("hello world", 10086)
        
        self.assertNotEqual(
            self.tl.pagging(1, 10),
            []
        )
        
    def test_remove(self):
        self.tl.add("hello world", 10086)

        self.tl.remove("hello world")

        self.assertEqual(
            self.tl.pagging(1, 10),
            []
        )

    def test_count(self):
        self.assertEqual(
            self.tl.count(),
            0
        )

        self.tl.add("hello world", 10086)

        self.assertEqual(
            self.tl.count(),
            1
        )

    def test_pagging_when_timeline_empty(self):
        self.assertEqual(
            self.tl.pagging(1, 10),
            []
        )

    def test_pagging_when_timeline_not_empty(self):
        for blog in self.blogs:
            self.tl.add(blog["id"], blog["time"])

        result = self.tl.pagging(1, 10)

        for i in range(len(self.blogs)):
            self.assertEqual(
                result[i],
                self.reversed_blogs[i]["id"]
            )

        result_with_time = self.tl.pagging(1, 10, True)

        for i in range(len(self.blogs)):
            self.assertEqual(
                result_with_time[i][0],
                self.reversed_blogs[i]["id"]
            )
            self.assertEqual(
                result_with_time[i][1],
                self.reversed_blogs[i]["time"]
            )

    def test_pagging_with_indexing(self):
        for blog in self.blogs:
            self.tl.add(blog["id"], blog["time"])

        self.assertEqual(
            self.tl.pagging(1, 1)[0],
            self.reversed_blogs[0]["id"]
        )

        self.assertEqual(
            self.tl.pagging(2, 1)[0],
            self.reversed_blogs[1]["id"]
        )

    def test_fetch_by_time_range_when_timeline_empty(self):
        self.assertEqual(
            self.tl.fetch_by_time_range(
                self.blogs[0]["time"],
                self.blogs[5]["time"],
                1,
                10
            ),
            []
        )

    def test_fetch_by_time_range_when_timeline_not_empty(self):
        for blog in self.blogs:
            self.tl.add(blog["id"], blog["time"])

        result = self.tl.fetch_by_time_range(
                    self.blogs[0]["time"],
                    self.blogs[5]["time"],
                    1,
                    10
                )

        for i in range(len(self.reversed_blogs)):
            self.assertEqual(
                result[i],
                self.reversed_blogs[i]["id"]
            )

        result_with_time = self.tl.fetch_by_time_range(
                    self.blogs[0]["time"],
                    self.blogs[5]["time"],
                    1,
                    10,
                    True
                )

        for i in range(len(self.reversed_blogs)):
            self.assertEqual(
                result_with_time[i][0],
                self.reversed_blogs[i]["id"]
            )
            self.assertEqual(
                result_with_time[i][1],
                self.reversed_blogs[i]["time"]
            )

    def test_fetch_by_time_range_with_indexing(self):
        for blog in self.blogs:
            self.tl.add(blog["id"], blog["time"])

        self.assertEqual(
            self.tl.fetch_by_time_range(
                self.blogs[0]["time"],
                self.blogs[5]["time"],
                1,
                1
            )[0],
            self.reversed_blogs[0]["id"]
        )

        self.assertEqual(
            self.tl.fetch_by_time_range(
                self.blogs[0]["time"],
                self.blogs[5]["time"],
                2,
                1
            )[0],
            self.reversed_blogs[1]["id"]
        )

if __name__ == "__main__":
    unittest.main()
