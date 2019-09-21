#coding:utf-8

def get_index(row, col):
    # 构建并返回一个 "row:col" 格式的索引，用作散列的键
    return str(row) + ":" + str(col)

class SparseGraph:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def set_node(self, row, col, value):
        """
        为给定索引上的节点设置值。
        """
        index = get_index(row, col)
        self.client.hset(self.key, index, value)

    def get_node(self, row, col):
        """
        获取给定索引上的节点的值。
        """
        index = get_index(row, col)
        return self.client.hget(self.key, index)

    def set_multi_nodes(self, *nodes):
        """
        一次为图的多个节点设置值。
        这个方法接受多个字典作为参数，每个字典的格式为：  {"row": r1, "col": c1, "value": v1} 。
        """
        index_to_value_mapping = {}
        for node in nodes:
            index = get_index(node["row"], node["col"])
            index_to_value_mapping[index] = node["value"]
        self.client.hmset(self.key, index_to_value_mapping)

    def get_multi_nodes(self, *nodes):
        """
        一次获取图中多个节点的值。
        这个方法接受多个字典作为参数，每个字典的格式为：  {"row": r1, "col": c1} 。
        """
        indexes = []
        for node in nodes:
            index = get_index(node["row"], node["col"])
            indexes.append(index)
        return self.client.hmget(self.key, *indexes)
