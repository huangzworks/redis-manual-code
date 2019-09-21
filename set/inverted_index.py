def make_item_key(item):
    return "InvertedIndex::" + item + "::keywords"

def make_keyword_key(keyword):
    return "InvertedIndex::" + keyword + "::items"

class InvertedIndex:

    def __init__(self, client):
        self.client = client

    def add_index(self, item, *keywords):
        """
        为物品添加关键字。
        """
        # 将给定关键字添加到物品集合中
        item_key = make_item_key(item)
        result = self.client.sadd(item_key, *keywords)
        # 遍历每个关键字集合，把给定物品添加到这些集合当中
        for keyword in keywords:
            keyword_key = make_keyword_key(keyword)
            self.client.sadd(keyword_key, item)
        # 返回新添加关键字的数量作为结果
        return result

    def remove_index(self, item, *keywords):
        """
        移除物品的关键字。
        """
        # 将给定关键字从物品集合中移除
        item_key = make_item_key(item)
        result = self.client.srem(item_key, *keywords)
        # 遍历每个关键字集合，把给定物品从这些集合中移除
        for keyword in keywords:
            keyword_key = make_keyword_key(keyword)
            self.client.srem(keyword_key, item)
        # 返回被移除关键字的数量作为结果
        return result

    def get_keywords(self, item):
        """
        获取物品的所有关键字。
        """
        return self.client.smembers(make_item_key(item))

    def get_items(self, *keywords):
        """
        根据给定的关键字获取物品。
        """
        # 根据给定的关键字，计算出与之对应的集合键名
        keyword_key_list = map(make_keyword_key, keywords)
        # 然后对这些储存着各式物品的关键字集合执行并集计算
        # 从而查找出带有给定关键字的物品
        return self.client.sinter(*keyword_key_list)
