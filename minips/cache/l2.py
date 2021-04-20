from minips.cache import Cache
class L2Cache(Cache):
    def __init__(self, size) -> None:
        super().__init__(size=size)