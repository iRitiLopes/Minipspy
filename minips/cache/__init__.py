from minips.cache.l1splitted import L1Splitted
from minips.cache.policy.lru import LRUAccess
from minips.cache.mapping.nvias import NVias
#from minips.cache.l1splitted import L1Splitted
from minips.cache.l1 import L1Cache
from minips.cache.l2 import L2Cache
from minips.word import Word

class Cache:
    def __init__(self, config=2) -> None:
        self.l1 = None
        self.l2 = None
        self.instruction_address_upper_limit = 0X00800000 
        if config == 2:
            self.l1 = L1Cache(size=1024, line_size=32)
        elif config == 3:
            self.l1 = L1Splitted(size=512, line_size=32)
        elif config == 4:
            self.l1 = L1Splitted(size=512, line_size=32, policy=LRUAccess())
        elif config == 5:
            self.l1 = L1Splitted(size=512, line_size=32, mode=NVias(n_vias=4))
        elif config == 6:
            self.l1 = L1Splitted(size=512, line_size=64, mode=NVias(n_vias=4))
            self.l2 = L2Cache(size=2048, line_size=64, mode=NVias(n_vias=8))
    
    def need_writeback(address):
        pass
    
    def store(self, address, data) -> None:
        if self.l1.need_writeback(address):
            # TODO make writeback
        pass

    def load(self, address) -> Word:
        if address < self.instruction_address_upper_limit:
            return self.l1.load(address, address_type=0)
        else:
            return self.l1.load(address, address_type=1)

    def __is_valid_address(self, address):
        return address in self.mem_blocks or address % 4 == 0

    def __str__(self) -> str:
        return str({str(k): str(v) for k, v in self.cache.items()})


class CacheException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
