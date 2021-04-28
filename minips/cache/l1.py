from minips.cache.mapping.direct import DirectMapping
from minips.cache.policy.random_access import RandomAccess
from minips.word import Word
from minips.cache.controller import CacheController

class L1Cache:
    def __init__(self, size=1024, line_size=32, mode=DirectMapping(), policy=RandomAccess()) -> None:
        self.size = size
        self.line_size = line_size
        self.mode = mode
        self.policy = policy
        self.set_size = self.line_size * self.mode.n_vias
        self.num_blocks = self.size // self.set_size
        self.cache = {x: Word("".zfill(32)) for x in range(self.num_blocks)}
        self.cache_control = {x: CacheController() for x in range(self.num_blocks)}

    
    def hit(self, address, *args, **kwargs):
        block = self.block_index(address)
        if not self.cache_control[block].compare_tag(address):
            return False
        return True
    
    def load(self, address, *args, **kwargs):
        block = self.block_index(address)
        return self.cache[block]

    def need_writeback(self, address, *args, **kwargs):
        block_id = self.block_index(address)
        if not self.hit(address):
            return self.cache_control[block_id].dirty and self.cache_control[block_id].valid
        return False
    
    def writeback(self, address, *args, **kwargs):
        block_id = self.block_index(address)
        wb_address = self.cache_control[block_id].address
        wb_data = self.cache[block_id]
        return wb_data, wb_address

    
    def store(self, address, data, *aegs, **kwargs):
        block_index = self.block_index(address)
        if not self.hit(address):
            self.cache_control[block_index].valid_this()
            self.cache_control[block_index].clean_this()
            self.cache_control[block_index].set_tag(self.tag(address))
            self.cache_control[block_index].set_address(address)
            self.cache[block_index] = Word(data)
        else:
            self.cache_control[block_index].dirty_this()
            self.cache[block_index] = Word(data)


    def block_index(self, address):
        return (address // self.line_size) % self.num_blocks
    
    def tag(self, address):
        return (address // self.line_size) // self.num_blocks