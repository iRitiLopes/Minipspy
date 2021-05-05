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
        elif config == 2:
            self.l1 = L1Splitted(size=512, line_size=32)
        elif config == 4:
            self.l1 = L1Splitted(size=512, line_size=32, policy=LRUAccess())
        elif config == 5:
            self.l1 = L1Splitted(size=512, line_size=32, mode=NVias(n_vias=4))
        elif config == 6:
            self.l1 = L1Splitted(size=512, line_size=64, mode=NVias(n_vias=4))
            self.l2 = L2Cache(size=2048, line_size=64, mode=NVias(n_vias=8))
    
    def l1_line(self, address):
        return self.l1.block_address(address)
    
    def hit(self, address):
        if address < self.instruction_address_upper_limit:
            return self.l1.hit(address, address_type=0)
        else:
            return self.l1.hit(address, return_type=1)

    def writeback(self, address, via):
        if address < self.instruction_address_upper_limit:
            return self.l1.writeback(address, via=via, address_type=0)
        return self.l1.writeback(address, via=via, address_type=1)
    
    def store_line(self, address, data_line, via):
        address_line = (address // self.l1.line_size) * self.l1.line_size
        for offset, data in enumerate(data_line):
            self.store(address_line + offset * 4, data, via=via)

    
    def need_writeback(self, address):
        if address < self.instruction_address_upper_limit:
            return self.l1.need_writeback(address, address_type=0)
        return self.l1.need_writeback(address, address_type=1)
    
    def store(self, address, data, *args, **kwargs) -> None:
        if address < self.instruction_address_upper_limit:
            self.l1.store(address, data, address_type=0, *args, **kwargs)
        else:
            self.l1.store(address, data, address_type=1, *args, **kwargs)

    def load(self, address, via) -> Word:
        if address < self.instruction_address_upper_limit:
            return self.l1.load(address, via, ddress_type=0)
        else:
            return self.l1.load(address, via, address_type=1)

    def __is_valid_address(self, address):
        return address in self.mem_blocks or address % 4 == 0

    def __str__(self) -> str:
        return str({str(k): str(v) for k, v in self.cache.items()})


class CacheException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
