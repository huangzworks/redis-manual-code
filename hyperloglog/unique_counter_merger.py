class UniqueCounterMerger:

    def __init__(self, client):
        self.client = client

    def merge(self, destination, *hyperloglogs):
        self.client.pfmerge(destination, *hyperloglogs)
