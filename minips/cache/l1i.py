from minips.cache import Cache
from minips.word import Word
from minips.cache import CacheController

class L1ICache(Cache):
    def __init__(self, size=512, mode=1, policy=1) -> None:
        super().__init__(size=size)
        self.modes = {
            1: DirectAccess,
            2: Vias4
        }

        self.policies = {
            1: Random,
            2: LRUAccess
        }
        self.size = size
        self.cache = {x: Word("".zfill(32)) for x in range(0, size, 4)}
        self.cache_control = {x: CacheController() for x in range(0, size, 4)}