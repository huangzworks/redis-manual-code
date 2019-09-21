def make_record_key(origin):
    return "forward_to_record::{0}".format(origin)

class Path:

    def __init__(self, client):
        self.client = client

    def forward_to(self, origin, destination):
        """
        记录一次从起点 origin 到目的地 destination 的访问。
        """
        key = make_record_key(origin)
        self.client.zincrby(key, 1, destination)

    def pagging_record(self, origin, number, count, with_time=False):
        """
        按照每页 count 个目的地计算，
        从起点 origin 的访问记录中取出位于第 number 页的访问记录，
        其中所有访问记录均按照访问次数从多到小进行排列。
        如果可选的 with_time 参数的值为 True ，那么将具体的访问次数也一并返回。
        """
        key = make_record_key(origin)
        start_index = (number-1)*count
        end_index = number*count-1
        return self.client.zrevrange(key, start_index, end_index, withscores=with_time, score_cast_func=int) # score_cast_func = int 用于将成员的分值从浮点数转换为整数
