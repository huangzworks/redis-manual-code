#coding:utf-8

def make_vertex_key(graph_name, vertex_name):
    return graph_name + "::vertex::" + vertex_name

class UndirectedGraph:

    def __init__(self, client, graph_name):
        self.client = client
        self.graph_name = graph_name
        
    def add_edge(self, start, end):
        start_vertex_key = make_vertex_key(self.graph_name, start)
        end_vertex_key = make_vertex_key(self.graph_name, end)
        self.client.sadd(start_vertex_key, end)
        self.client.sadd(end_vertex_key, start)

    def remove_edge(self, start, end):
        start_vertex_key = make_vertex_key(self.graph_name, start)
        end_vertex_key = make_vertex_key(self.graph_name, end)
        self.client.srem(start_vertex_key, end)
        self.client.srem(end_vertex_key, start)

    def has_edge(self, start, end):
        start_vertex_key = make_vertex_key(self.graph_name, start)
        return self.client.sismember(start_vertex_key, end)

    def get_all_connected_vertexs(self, vertex):
        vertex_key = make_vertex_key(self.graph_name, vertex)
        return self.client.smembers(vertex_key)
