def make_edge_name_from_vertexs(start, end):
    """
    使用边的起点和终点组建边的名字。
    例子：对于 start 为 "a" 、 end 为 "b" 的输入，这个函数将返回 "a->b" 。
    """
    return str(start) + "->" + str(end)

def decompose_vertexs_from_edge_name(name):
    """
    从边的名字中分解出边的起点和终点。
    例子：对于输入 "a->b" ，这个函数将返回结果 ["a", "b"] 。
    """
    return name.split("->")


class Graph:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def add_edge(self, start, end, weight):
        """
        添加一条从顶点 start 连接至顶点 end 的边，并将边的权重设置为 weight 。
        """
        edge = make_edge_name_from_vertexs(start, end)
        self.client.hset(self.key, edge, weight)

    def remove_edge(self, start, end):
        """
        移除从顶点 start 连接至顶点 end 的一条边。
        这个方法在成功删除边时返回 True ，
        因为边不存在而导致删除失败时返回 False 。
        """
        edge = make_edge_name_from_vertexs(start, end)
        return self.client.hdel(self.key, edge)

    def get_edge_weight(self, start, end):
        """
        获取从顶点 start 连接至顶点 end 的边的权重，
        如果给定的边不存在，那么返回 None 。
        """
        edge = make_edge_name_from_vertexs(start, end)
        return self.client.hget(self.key, edge)

    def has_edge(self, start, end):
        """
        检查顶点 start 和顶点 end 之间是否有边，
        是的话返回 True ，否则返回 False 。
        """
        edge = make_edge_name_from_vertexs(start, end)
        return self.client.hexists(self.key, edge)

    def add_multi_edges(self, *tuples):
        """
        一次向图中添加多条边。
        这个方法接受任意多个格式为 (start, end, weight) 的三元组作为参数。
        """
        # redis-py 客户端的 hmset() 方法接受一个字典作为参数
        # 格式为 {field1: value1, field2: value2, ...}
        # 为了一次对图中的多条边进行设置
        # 我们要将待设置的各条边以及它们的权重储存在以下字典
        nodes_and_weights = {}

        # 遍历输入的每个三元组，从中取出边的起点、终点和权重
        for start, end, weight in tuples:
            # 根据边的起点和终点，创建出边的名字
            edge = make_edge_name_from_vertexs(start, end)
            # 使用边的名字作为字段，边的权重作为值，把边及其权重储存到字典里面
            nodes_and_weights[edge] = weight

        # 根据字典中储存的字段和值，对散列进行设置
        self.client.hmset(self.key, nodes_and_weights)

    def get_multi_edge_weights(self, *tuples):
        """
        一次获取多条边的权重。
        这个方法接受任意多个格式为 (start, end) 的二元组作为参数，
        然后返回一个列表作为结果，列表中依次储存着每条输入边的权重。
        """
        # hmget() 方法接受一个格式为 [field1, field2, ...] 的列表作为参数
        # 为了一次获取图中多条边的权重
        # 我们需要把所有想要获取权重的边的名字依次放入到以下列表里面
        edge_list = []

        # 遍历输入的每个二元组，从中获取边的起点和终点
        for start, end in tuples:
            # 根据边的起点和终点，创建出边的名字
            edge = make_edge_name_from_vertexs(start, end)
            # 把边的名字放入到列表中
            edge_list.append(edge)

        # 根据列表中储存的每条边的名字，从散列里面获取它们的权重
        return self.client.hmget(self.key, edge_list)

    def get_all_edges(self):
        """
        以集合形式返回整个图包含的所有边，
        集合包含的每个元素都是一个 (start, end) 格式的二元组。
        """
        # hkeys() 方法将返回一个列表，列表中包含多条边的名字
        # 例如 ["a->b", "b->c", "c->d"]
        edges = self.client.hkeys(self.key)

        # 创建一个集合，用于储存二元组格式的边
        result = set()
        # 遍历每条边的名字
        for edge in edges:
            # 根据边的名字，分解出边的起点和终点
            start, end = decompose_vertexs_from_edge_name(edge)
            # 使用起点和终点组成一个二元组，然后把它放入到结果集合里面
            result.add((start, end))

        return result

    def get_all_edges_with_weight(self):
        """
        以集合形式返回整个图包含的所有边，以及这些边的权重。
        集合包含的每个元素都是一个 (start, end, weight) 格式的三元组。
        """
        # hgetall() 方法将返回一个包含边和权重的字典作为结果
        # 格式为 {edge1: weight1, edge2: weight2, ...}
        edges_and_weights = self.client.hgetall(self.key)

        # 创建一个集合，用于储存三元组格式的边和权重
        result = set()
        # 遍历字典中的每个元素，获取边以及它的权重
        for edge, weight in edges_and_weights.items():
            # 根据边的名字，分解出边的起点和终点
            start, end = decompose_vertexs_from_edge_name(edge)
            # 使用起点、终点和权重构建一个三元组，然后把它添加到结果集合里面
            result.add((start, end, weight))

        return result
