#coding:utf-8

import unittest

from redis import Redis
from graph import Graph

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.graph = Graph(self.client, "test-graph")

    def test_add_edge(self):
        self.assertEqual(
            self.graph.get_all_connected_vertexs("a"),
            set()
        )

        self.graph.add_edge("a", "b")

        self.assertNotEqual(
            self.graph.get_all_connected_vertexs("a"),
            set()
        )

    def test_remove_edge(self):
        self.graph.add_edge("a", "b")

        self.graph.remove_edge("a", "b")

        self.assertEqual(
            self.graph.get_all_connected_vertexs("a"),
            set()
        )

    def test_has_edge(self):
        self.assertFalse(
            self.graph.has_edge("a", "b")
        )

        self.graph.add_edge("a", "b")

        self.assertTrue(
            self.graph.has_edge("a", "b")
        )

    def test_get_all_connected_vertexs(self):
        self.assertEqual(
            self.graph.get_all_connected_vertexs("a"),
            set()
        )

        self.graph.add_edge("a", "b")

        self.assertEqual(
            self.graph.get_all_connected_vertexs("a"),
            {"b"}
        )

if __name__ == "__main__":
    unittest.main()
