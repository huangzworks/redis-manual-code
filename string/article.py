from time import time  # time() 函数用于获取当前 Unix 时间戳

class Article:

    def __init__(self, client, article_id):
        self.client = client
        self.id = str(article_id)
        self.title_key = "article::" + self.id + "::title"
        self.content_key = "article::" + self.id + "::content"
        self.author_key = "article::" + self.id + "::author"
        self.create_at_key = "article::" + self.id + "::create_at"

    def create(self, title, content, author):
        """
        创建一篇新的文章，创建成功时返回 True ，
        因为文章已存在而导致创建失败时返回 False 。
        """
        article_data = {
            self.title_key: title,
            self.content_key: content,
            self.author_key: author,
            self.create_at_key: time()
        }
        return self.client.msetnx(article_data)

    def get(self):
        """
        返回 ID 对应的文章信息。
        """
        result = self.client.mget(self.title_key,
                                  self.content_key,
                                  self.author_key,
                                  self.create_at_key)
        return {"id": self.id, "title": result[0], "content": result[1],
                "author": result[2], "create_at": result[3]}

    def update(self, title=None, content=None, author=None):
        """
        对文章的各项信息进行更新，
        更新成功时返回 True ，失败时返回 False 。
        """
        article_data = {}
        if title is not None:
            article_data[self.title_key] = title
        if content is not None:
            article_data[self.content_key] = content
        if author is not None:
            article_data[self.author_key] = author
        return self.client.mset(article_data)

    def get_content_len(self):
        """
        返回文章内容的字节长度。
        """
        return self.client.strlen(self.content_key)

    def get_content_preview(self, preview_len):
        """
        返回指定长度的文章预览内容。
        """
        start_index = 0
        end_index = preview_len-1
        return self.client.getrange(self.content_key, start_index, end_index)
