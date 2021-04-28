from minips.cache.policy.random_access import RandomAccess
from minips.cache.mapping.direct import DirectMapping
from minips.cache.l1d import L1DCache
from minips.cache.l1i import L1ICache
from minips.cache import Cache
from minips.word import Word

class L1Splitted:
    def __init__(self, size=512, line_size=32, mode=DirectMapping(), policy=RandomAccess()) -> None:
        super().__init__(size=size)
        self.mode = mode
        self.policy = policy
        self.l1i = L1ICache(size=size, line_size=line_size, mode=self.mode, policy=self.policy)
        self.l1d = L1DCache(size=size, line_size=line_size, mode=self.mode, policy=self.policy)
        self.size = size
        self.line_size = line_size
    
    def hit(self, address, address_type) -> bool:
        if address_type == 0:
            if self.l1i.hit(address):
                return True
            else:
                return self.l1d.hit(address)
        else:
            return self.l1d.hit(address)

    def load(self, address, address_type):
        if address_type == 0:
            if self.l1i.hit(address):
                return self.l1i.load(address)
            elif self.l1d.hit(address):
                return self.l1d.load(address)
        elif self.l1d.hit(address):
            return self.l1d.load(address)
    
    def store(self, address, data, address_type):
        block = self.block_index(address)
        self.cache_control[block].valid_this()
        self.cache_control[block].clean_this()
        self.cache_control[block].set_tag(address)
        self.cache[block] = Word(data)

    def block_index(self, address):
        return (address // (self.line_size // 8) % self.num_blocks)