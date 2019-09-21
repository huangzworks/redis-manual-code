#coding:utf-8

import unittest

from redis import Redis
from paging import Paging

class TestPaging(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.paging = Paging(self.client, "blog page")

    def test_add(self):
        self.assertTrue(
            self.paging.get_page(1, 10) == []
        )
        self.paging.add("blog2151")
        self.assertTrue(
            self.paging.get_page(1, 10) != []
        )

    def test_get_page(self):
        self.assertEqual(
            self.paging.get_page(1, 10),
            []
        )

        # add items
        blog_post_list = ["blog2151", "blog2351", "blog2691", "blog3622", "blog5829"]
        for blog_post in blog_post_list:
            self.paging.add(blog_post)

        # single page case
        self.assertEqual(
            self.paging.get_page(1, 10),
            list(reversed(blog_post_list))
        )

        # multi page case
        self.assertEqual(
            self.paging.get_page(1, 2),
            list(reversed(blog_post_list))[:2]
        )
        self.assertEqual(
            self.paging.get_page(2, 2),
            list(reversed(blog_post_list))[2:4]
        )

    def test_size(self):
        self.assertEqual(
            self.paging.size(),
            0
        )
        self.paging.add("blog2151")
        self.assertEqual(
            self.paging.size(),
            1
        )

if __name__ == "__main__":
    unittest.main()
