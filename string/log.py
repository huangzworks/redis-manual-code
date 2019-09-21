LOG_SEPARATOR = "\n"

class Log:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def add(self, new_log):
        """
        将给定的日志储存起来。
        """
        new_log += LOG_SEPARATOR
        self.client.append(self.key, new_log)

    def get_all(self):
        """
        以列表形式返回所有日志。
        """
        all_logs = self.client.get(self.key)
        if all_logs is not None:
            log_list = all_logs.split(LOG_SEPARATOR)
            log_list.remove("")
            return log_list
        else:
            return []
