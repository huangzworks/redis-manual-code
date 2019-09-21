class Paging:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def add(self, item):
        """
        将给定元素添加到分页列表中。
        """
        self.client.lpush(self.key, item)

    def get_page(self, page_number, item_per_page):
        """
        从指定页数中取出指定数量的元素。
        """
        # 根据给定的 page_number （页数）和 item_per_page （每页包含的元素数量）
        # 计算出指定分页元素在列表中所处的索引范围
        # 例子：如果 page_number = 1 ， item_per_page = 10
        # 那么程序计算得出的起始索引就是 0 ，而结束索引则是 9
        start_index = (page_number - 1) * item_per_page
        end_index = page_number * item_per_page - 1
        # 根据索引范围从列表中获取分页元素
        return self.client.lrange(self.key, start_index, end_index)

    def size(self):
        """
        返回列表目前包含的分页元素数量。
        """
        return self.client.llen(self.key)
