from minips.cache.l1splitted import L1Splitted
from minips.cache.policy.lru import LRUAccess
from minips.cache.mapping.nvias import NVias
from minips.cache.l1 import L1Cache
from minips.cache.l2 import L2Cache


class Cache:
    def __init__(self, config=2):
        self.l1 = None
        self.l2 = None
        if config == 2:
            self.l1 = L1Cache(size=1024, line_size=32)
        elif config in (3, 4, 5, 6):
            self.l1 = L1Splitted(
                size=512, line_size=64 if config == 6 else 32,
                mode=(NVias(4) if config >= 5 else
                      NVias(16) if config == 4 else None),
                policy=LRUAccess() if config == 4 else None)
            if config == 6:
                self.l2 = L2Cache(size=2048, line_size=64, mode=NVias(8))
        elif config != 1:
            raise ValueError("Memory mode must be between 1 and 6")

    def _type(self, address):
        return 0 if 0x00400000 <= address < 0x00800000 else 1

    def l1_line(self, address):
        return self.l1.block_address(address)

    def hit(self, address):
        return self.l1.hit(address, address_type=self._type(address))

    def load(self, address, via):
        return self.l1.load(address, via, address_type=self._type(address))

    def store(self, address, data, via=None):
        self.l1.store(address, data, via=via, address_type=self._type(address))

    def store_line(self, address, data_line, via):
        self.l1.store_line(address, data_line, via, address_type=self._type(address))

    def need_writeback(self, address):
        return self.l1.need_writeback(address, address_type=self._type(address))

    def writeback(self, address, via):
        return self.l1.writeback(address, via, address_type=self._type(address))
