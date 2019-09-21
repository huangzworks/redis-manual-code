class IdGenerator:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def produce(self):
        """
        生成并返回下一个 ID 。
        """
        return self.client.incr(self.key)

    def reserve(self, n):
        """
        保留前 n 个 ID ，使得之后执行的 produce() 方法产生的 ID 都大于 n 。
        为了避免 produce() 方法产生重复 ID ，
        这个方法只能在 produce() 方法和 reserve() 方法都没有执行过的情况下使用。
        这个方法在 ID 被成功保留时返回 True ，
        在 produce() 方法或 reserve() 方法已经执行过而导致保留失败时返回 False 。
        """
        result = self.client.set(self.key, n, nx=True)
        return result is True
