from functools import cache
from minips.cache.mapping.direct import DirectMapping
from minips.cache.policy.random_access import RandomAccess
from minips.cache.controller import CacheData
import math


class L1Cache:
    def __init__(self, size=1024, line_size=32, mode=DirectMapping(), policy=RandomAccess()) -> None:
        self.size = size
        self.line_size = line_size
        self.mode = mode
        self.policy = policy
        self.n_vias = self.mode.n_vias
        self.num_words = self.line_size
        self.block_size = self.line_size * self.mode.n_vias
        self.num_blocks = self.size // self.block_size
        self.nbits_byte_offset = math.floor(math.log2(self.num_words))
        self.nbits_block_offset = math.floor(math.log2(self.num_blocks))
        self.nbits_tag = 32 - (self.nbits_block_offset + self.nbits_byte_offset)
        self.cache: dict[int, list[list[CacheData]]] = {
            x: [[CacheData(data=None, tag=0, address=0)]*(self.num_words // 4)]*self.n_vias
            for x in range(self.num_blocks)
        }


    def hit(self, address, *args, **kwargs):
        block_idx = self.block_index(address)
        line_idx = self.byte_index(address)
        block = self.cache[block_idx]
        for via_idx, via in enumerate(block):
            if via[line_idx].valid and via[line_idx].compare_tag(self.tag(address)):
                return True, via_idx
        return False, -1

    def load(self, address, via, *args, **kwargs):
        block_idx = self.block_index(address)
        byte_idx = self.byte_index(address)
        self.cache[block_idx][via][byte_idx].set_time()
        return self.cache[block_idx][via][byte_idx].data

    def need_writeback(self, address, *args, **kwargs) -> bool:
        block_idx = self.block_index(address)
        byte_idx = self.byte_index(address)
        block = self.cache[block_idx]
        
        hit, via = self.hit(address)

        if hit:
            return False, via
        else:
            via = self.policy.run(from_n=0 , to_n=self.n_vias - 1, block=block)
            for word in block[via]:
                if word.valid:
                    return True, via
            return False, via

    def writeback(self, address, via, *args, **kwargs):
        block_idx = self.block_index(address)
        cache_line = self.cache[block_idx][via]
        return cache_line, self.block_address(address)

    def parse_address(self, address):
        byte_offset = (((1 << self.nbits_byte_offset) - 1) & (address >> (0)))
        block_offset = (((1 << self.nbits_block_offset) - 1) &
                        (address >> (self.nbits_byte_offset)))
        tag = (((1 << self.nbits_tag) - 1) & (address >>
               (self.nbits_block_offset + self.nbits_byte_offset)))
        return tag, block_offset, byte_offset

    def store(self, address, data, *aegs, **kwargs):
        block_index = self.block_index(address)
        byte_idx = self.byte_index(address)
        block = self.cache[block_index]
        tag = self.tag(address)
        
        hit, via = self.hit(address)
        if hit:
            block[via][byte_idx] = CacheData(data=data, tag=tag, address=address)
            block[via][byte_idx].valid_this()
            block[via][byte_idx].dirty_this()
            block[via][byte_idx].set_time()
        else:
            via = kwargs['via']
            block[via][byte_idx] = CacheData(data=data, tag=tag, address=address)
            block[via][byte_idx].valid_this()

    def byte_index(self, address):
        return (((1 << self.nbits_byte_offset) - 1) & (address >> (0))) // 4

    def block_index(self, address):
        return (((1 << self.nbits_block_offset) - 1) & (address >> (self.nbits_byte_offset)))
    
    def cache_index(self, address):
        pass
    
    def block_address(self, address):
        return address // self.line_size

    def tag(self, address):
        return (((1 << self.nbits_tag) - 1) & (address >> (self.nbits_block_offset + self.nbits_byte_offset)))
