#coding:utf-8

import unittest

from redis import Redis
from undirected_graph import UndirectedGraph

class TestUndirectedGraph(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.graph = UndirectedGraph(self.client, "test-graph")

    def test_add_edge(self):
        self.assertEqual(
            self.graph.get_all_connected_vertexs("a"),
            set()
        )
        self.assertEqual(
            self.graph.get_all_connected_vertexs("b"),
            set()
        )
       
        self.graph.add_edge("a", "b")

        self.assertNotEqual(
            self.graph.get_all_connected_vertexs("a"),
            set()
        )
        self.assertNotEqual(
            self.graph.get_all_connected_vertexs("b"),
            set()
        )

    def test_remove_edge(self):
        self.graph.add_edge("a", "b")
        
        self.graph.remove_edge("a", "b")

        self.assertEqual(
            self.graph.get_all_connected_vertexs("a"),
            set()
        )
        self.assertEqual(
            self.graph.get_all_connected_vertexs("b"),
            set()
        )

    def test_has_edge(self):
        self.assertFalse(
            self.graph.has_edge("a", "b")
        )
        self.assertFalse(
            self.graph.has_edge("b", "a")
        )

        self.graph.add_edge("a", "b")

        self.assertTrue(
            self.graph.has_edge("a", "b")
        )
        self.assertTrue(
            self.graph.has_edge("b", "a")
        )

    def test_get_all_connected_vertexs(self):
        self.assertEqual(
            self.graph.get_all_connected_vertexs("a"),
            set()
        )
        self.assertEqual(
            self.graph.get_all_connected_vertexs("b"),
            set()
        )

        self.graph.add_edge("a", "b")

        self.assertEqual(
            self.graph.get_all_connected_vertexs("a"),
            {"b"}
        )
        self.assertEqual(
            self.graph.get_all_connected_vertexs("b"),
            {"a"}
        )

if __name__ == "__main__":
    unittest.main()
