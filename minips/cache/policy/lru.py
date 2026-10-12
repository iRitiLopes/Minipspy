class LRUAccess:
    def run(self, from_n, to_n, block, **kwargs):
        return min(range(from_n, to_n + 1), key=lambda via: block[via][0].timestamp)
