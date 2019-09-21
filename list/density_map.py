#coding:utf-8

def map_key(map_name, row_number):
    return "{0}[{1}]".format(map_name, row_number) 

class DensityMap:

    def __init__(self, client, map_name):
        self.client = client
        self.map_name = map_name

    def set_map(self, list_of_rows):
        """
        根据给定的二维嵌套列表，创建整个图。
        """
        for row_number in range(len(list_of_rows)):
            self.set_row(row_number, *list_of_rows[row_number])

    def get_map(self, row_count):
        """
        根据给定的行数，获取整个图。
        """
        # TODO:需要像个办法来储存图的 row 数量，这样就可以免去 row_count 参数
        whole_map = []
        for row_number in range(row_count):
            whole_map.append(self.get_row(row_number))
        return whole_map

    def set_row(self, row_number, *values):
        """
        将 map[row_number] 这一行设置为 values 中指定的值。
        """
        # 假设 self.map 的值为 "matrix" ，那么得出的键名为 matrix[0]
        key = map_key(self.map_name, row_number)
        self.client.rpush(key, *values)

    def get_row(self, row_number):
        """
        获取 map[row_number] 整个行。
        """
        key = map_key(self.map_name, row_number)
        return self.client.lrange(key, 0, -1)

    def set_value(self, row_number, col_number, value):
        """
        将 map[row_number, col_number] 设置为指定的值。
        """
        key = map_key(self.map_name, row_number)
        self.client.lset(key, col_number, value)

    def get_value(self, row_number, col_number):
        """
        获取 map[row_number, col_number] 的值。
        """
        key = map_key(self.map_name, row_number)
        return self.client.lindex(key, col_number)
