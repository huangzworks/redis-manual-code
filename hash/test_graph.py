#coding:utf-8

import unittest

from redis import Redis
from graph import Graph

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.graph = Graph(self.client, "my-graph")

    def test_add_edge(self):
        self.assertFalse(
            self.graph.has_edge("a", "b")
        )
        self.graph.add_edge("a", "b", 10086)
        self.assertTrue(
            self.graph.has_edge("a", "b")
        )

    def test_remove_edge(self):
        self.graph.add_edge("a", "b", 10086)
        self.graph.remove_edge("a", "b")
        self.assertFalse(
            self.graph.has_edge("a", "b")
        )

    def test_get_edge_weight(self):
        self.assertIsNone(
            self.graph.get_edge_weight("a", "b"),
        )
        self.graph.add_edge("a", "b", 10086)
        self.assertEqual(
            self.graph.get_edge_weight("a", "b"),
            "10086"
        )

    def test_add_multi_edges(self):
        self.graph.add_multi_edges(
            ("a", "b", 10),
            ("b", "c", 20),
            ("c", "d", 30)
        )
        self.assertEqual(
            self.graph.get_edge_weight("a", "b"),
            "10"
        )
        self.assertEqual(
            self.graph.get_edge_weight("b", "c"),
            "20"
        )
        self.assertEqual(
            self.graph.get_edge_weight("c", "d"),
            "30"
        )

    def test_get_multi_edge_weights(self):
        self.graph.add_multi_edges(
            ("a", "b", 10),
            ("b", "c", 20),
            ("c", "d", 30)
        )   
        e1, e2, e3 = self.graph.get_multi_edge_weights(
            ("a", "b"),
            ("b", "c"),
            ("c", "d")
        )
        self.assertEqual(
            e1, 
            "10"
        )
        self.assertEqual(
            e2, 
            "20"
        )
        self.assertEqual(
            e3,
            "30"
        )

    def test_get_all_edges(self):
        self.graph.add_multi_edges(
            ("a", "b", 10),
            ("b", "c", 20),
            ("c", "d", 30)
        )      

        self.assertEqual(
            self.graph.get_all_edges(),
            {
                ("a", "b"),
                ("b", "c"),
                ("c", "d")
            }
        )

    def test_get_all_edges_with_weight(self):
        self.graph.add_multi_edges(
            ("a", "b", 10),
            ("b", "c", 20),
            ("c", "d", 30)
        )      

        self.assertEqual(
            self.graph.get_all_edges_with_weight(),
            {
                ("a", "b", "10"),
                ("b", "c", "20"),
                ("c", "d", "30")
            }
        )

if __name__ == "__main__":
    unittest.main()
