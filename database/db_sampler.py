def type_sample_result(type_name, type_counter, db_size):
    result = "{0}: {1} keys, {2}% of the total."
    return result.format(type_name, type_counter, type_counter*100.0/db_size)

class DbSampler:

    def __init__(self, client):
        self.client = client

    def sample(self):
        # 键类型计数器
        type_counter = {
            "string": 0,
            "list": 0,
            "hash": 0,
            "set": 0,
            "zset": 0,
            "stream": 0,
        }

        # 遍历整个数据库
        for key in self.client.scan_iter():
            # 获取键的类型
            type = self.client.type(key)
            # 对相应的类型计数器执行加一操作
            type_counter[type] += 1

        # 获取数据库大小
        db_size = self.client.dbsize()

        # 打印结果
        print("Sampled {0} keys.".format(db_size))
        print(type_sample_result("String", type_counter["string"], db_size))
        print(type_sample_result("List", type_counter["list"], db_size))
        print(type_sample_result("Hash", type_counter["hash"], db_size))
        print(type_sample_result("Set", type_counter["set"], db_size))
        print(type_sample_result("SortedSet", type_counter["zset"], db_size))
        print(type_sample_result("Stream", type_counter["stream"], db_size))
