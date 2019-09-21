#coding:utf-8

# 这个程序虽然可行，但是在每个 zset 上都为相同的物品添加相同的权重值太浪费空间了
# 还不如添加一个额外的散列来储存权重，然后在 sinter 之后使用 SORT ... BY weight_hash 来排序

def make_item_key(item):
    return "InvertedIndex::" + item + "::keywords"

def make_keyword_key(keyword):
    return "InvertedIndex::" + keyword + "::items"

def make_calculate_key(*keywords):
    # 根据输入的多个关键字
    # 生成一个 "keyword1+keyword2+...+keywordN" 格式的字符串
    keyword_list = reduce(lambda x, y: x + "+" + y, keywords)
    return "InvertedIndex::" + keyword_list + "::calculate"


class InvertedIndex:

    def __init__(self, client):
        self.client = client

    def add_index(self, item, weight, *keywords):
        """
        为物品添加关键字，并为该物品设置权重值。
        """
        # 将给定关键字添加到物品集合当中
        item_key = make_item_key(item)
        result = self.client.sadd(item_key, *keywords)
        # 遍历每个关键字有序集合，将给定物品添加到这些有序集合中
        # 并为每个物品关联权重值
        for keyword in keywords:
            keyword_key = make_keyword_key(keyword)
            self.client.zadd(keyword_key, item, weight)
        # 返回成功添加的关键字数量作为结果
        return result

    def remove_index(self, item, *keywords):
        item_key = make_item_key(item)
        result = self.client.srem(item_key, *keywords)
        for keyword in keywords:
            keyword_key = make_keyword_key(keyword)
            self.client.zrem(keyword_key, item)

    def get_keywords(self, item):
        return self.client.smembers(make_item_key(item))

    def get_items(self, *keywords):
        keyword_key_list = map(make_keyword_key, keywords)
        calculate_key = make_calculate_key(*keyword_key_list)
        self.client.zinterstore(calculate_key, keyword_key_list, "MAX")
        return self.client.zrevrange(calculate_key, 0, -1)

    def get_items_with_weight(self, *keywords):
        keyword_key_list = map(make_keyword_key, keywords)
        calculate_key = make_calculate_key(*keyword_key_list)
        self.client.zinterstore(calculate_key, keyword_key_list, "MAX")
        return self.client.zrevrange(calculate_key, 0, -1, withscores=True)
