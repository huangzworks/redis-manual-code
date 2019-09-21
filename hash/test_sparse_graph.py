#coding:utf-8

from redis import Redis
from sparse_graph import SparseGraph

#

client = Redis()
client.flushdb()

#

graph = SparseGraph(client, 'graph::123')

#

assert(
    graph.get_node(1, 3) is None
)

#

graph.set_node(1, 3, "Hello")

assert(
    graph.get_node(1, 3) == "Hello"
)

#

graph.set_multi_nodes(
    {"row": 2, "col": 9, "value": "Good"},
    {"row": 7, "col": 3, "value": "Morning"},
    {"row": 11, "col": 8, "value": "Peter"}
)

assert(
    graph.get_node(2, 9) == "Good"
)
assert(
    graph.get_node(7, 3) == "Morning"
)
assert(
    graph.get_node(11, 8) == "Peter"
)

#

result = graph.get_multi_nodes(
    {"row": 2, "col": 9},
    {"row": 7, "col": 3},
    {"row": 11, "col": 8}
)

assert(
    result[0] == "Good" and \
    result[1] == "Morning" and \
    result[2] == "Peter"
)

#

client.flushdb()
print("all tests passed!")
