from minips.cache import Cache
from minips.word import Word
from minips.cache import CacheController

class L1Cache(Cache):
    def __init__(self, size=1024) -> None:
        super().__init__(size=size)
        self.size = size
        self.cache = {x: Word("".zfill(32)) for x in range(0, size, 4)}
        self.cache_control = {x: CacheController() for x in range(0, size, 4)}