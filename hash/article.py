from time import time

class Article:

    def __init__(self, client, article_id):
        self.client = client
        self.article_id = str(article_id)
        self.article_hash = "article::" + self.article_id

    def is_exists(self):
        """
        检查给定 ID 对应的文章是否存在。
        """
        # 如果文章散列里面已经设置了标题，那么我们认为这篇文章存在
        return self.client.hexists(self.article_hash, "title")

    def create(self, title, content, author):
        """
        创建一篇新文章，创建成功时返回 True ，
        因为文章已经存在而导致创建失败时返回 False 。
        """
        # 文章已存在，放弃执行创建操作
        if self.is_exists(): 
            return False

        # 把所有文章数据都放到字典里面
        article_data = {
            "title": title,
            "content": content,
            "author": author,
            "create_at": time()
        }
        # redis-py 的 hmset() 方法接受一个字典作为参数，
        # 并根据字典内的键和值对散列的字段和值进行设置。
        return self.client.hmset(self.article_hash, article_data)

    def get(self):
        """
        返回文章的各项信息。
        """
        # hgetall() 方法会返回一个包含标题、内容、作者和创建日期的字典
        article_data = self.client.hgetall(self.article_hash)
        # 把文章 ID 也放到字典里面，以便用户操作
        article_data["id"] = self.article_id
        return article_data

    def update(self, title=None, content=None, author=None):
        """
        对文章的各项信息进行更新，
        更新成功时返回 True ，失败时返回 False 。
        """
        # 如果文章并不存在，那么放弃执行更新操作
        if not self.is_exists(): 
            return False

        article_data = {}
        if title is not None:
            article_data["title"] = title
        if content is not None:
            article_data["content"] = content
        if author is not None:
            article_data["author"] = author
        return self.client.hmset(self.article_hash, article_data)
