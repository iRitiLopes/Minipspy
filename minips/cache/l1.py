from minips.cache.mapping.direct import DirectMapping
from minips.cache.policy.random_access import RandomAccess
from minips.cache import Cache
from minips.word import Word
from minips.cache import CacheController

class L1Cache(Cache):
    def __init__(self, size=1024, mapping=DirectMapping(), policy=RandomAccess()) -> None:
        super().__init__(size=size)
        self.size = size
        self.mapping = mapping
        self.policy = policy
        self.cache = {x: Word("".zfill(32)) for x in range(0, size, 4)}
        self.cache_control = {x: CacheController() for x in range(0, size, 4)}

    def load(self, address):
        pass

    def store(self, address, data):
        pass

    def is_valid(self, address):
        return self.cache_control[address].valid