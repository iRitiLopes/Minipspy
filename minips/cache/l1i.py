import math
from minips.cache.controller import CacheData
from minips.cache.policy.random_access import RandomAccess
from minips.cache.mapping.direct import DirectMapping
from minips.word import Word

class L1ICache:
    def __init__(self, size=512, line_size=32, mode=DirectMapping(), policy=RandomAccess()) -> None:
        self.size = size
        self.line_size = line_size
        self.mode = mode
        self.policy = policy
        self.set_size = self.line_size * self.mode.n_vias
        self.num_blocks = self.size // self.set_size
        self.n_words = self.line_size // 4
        self.nbits_byte_offset = math.floor(math.log2(self.n_words))
        self.nbits_block_offset = math.floor(math.log2(self.num_blocks))
        self.nbits_tag = math.floor( math.log2(32 - (self.nbits_block_offset + self.nbits_byte_offset)))
        self.cache: dict[int, list[CacheData]] = {
            x: [CacheData(data=None, tag=0)]*self.n_words 
            for x in range(self.num_blocks)
        }
    
    
    def hit(self, address):
        pass
    
    def load(self, address):
        block = self.block_index(address)
        if not self.cache_control[block].compare_tag(address):
            raise Exception("Invalid")
        return self.cache[block]
    
    def store(self, address, data):
        block = self.block_index(address)
        self.cache_control[block].valid_this()
        self.cache_control[block].clean_this()
        self.cache_control[block].set_tag(address)
        self.cache[block] = Word(data)

    def block_index(self, address):
        return (address // (self.line_size // 8) % self.num_blocks)