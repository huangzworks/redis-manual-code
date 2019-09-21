#coding:utf-8

def make_vertex_key(graph_name, vertex_name):
    return graph_name + "::vertex::" + vertex_name

class DirectedGraph:

    def __init__(self, client, graph_name):
        self.client = client
        self.graph_name = graph_name

    def add_edge(self, start, end):
        """
        添加一条从顶点 start 至到顶点 end 的边，
        添加成功时返回 True ，因为边已经存在而导致添加失败时返回 False 。
        """
        start_vertex_key = make_vertex_key(self.graph_name, start)
        return self.client.sadd(start_vertex_key, end) == 1

    def remove_edge(self, start, end):
        """
        移除从顶点 start 至顶点 end 的边，
        移除成功时返回 True ，因为边不存在而导致移除失败时返回 False 。
        """
        start_vertex_key = make_vertex_key(self.graph_name, start)
        return self.client.srem(start_vertex_key, end) == 1

    def has_edge(self, start, end):
        """
        检查顶点 start 至顶点 end 之间是否有边，
        是的话返回 True ，否则的话返回 False 。
        """
        start_vertex_key = make_vertex_key(self.graph_name, start)
        return self.client.sismember(start_vertex_key, end)

    def get_all_connected_vertexs(self, vertex):
        """
        返回所有与给定顶点相连接的其他顶点。
        """
        vertex_key = make_vertex_key(self.graph_name, vertex)
        return self.client.smembers(vertex_key)
