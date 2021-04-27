from minips.cache.mapping.nvias import NVias
from minips.cache.policy.lru import LRUAccess
from minips.cache.l2 import L2Cache
from minips.cache.l1splitted import L1Splitted
from minips.cache.l1 import L1Cache
from helpers.bin2int import Bin2Int
from minips.word import Word


class Memory(object):
    mem_blocks = {}
    TEXT_SECTION_START = 0x00400000
    DATA_SECTION_START = 0x10010000
    RODATA_SECION_START = 0X00800000
    STACK_POINTER = 0x7fffeffc
    GLOBAL_POINTER = 0x10008000

    def __init__(self, config) -> None:
        self.clean()
        self.mem_mode = config
        self.l1 = None
        self.l2 = None
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

    def clean(self) -> None:
        """
        Clean each address of memory with empty words
        """
        self.mem_blocks[self.TEXT_SECTION_START] = Word()
        self.mem_blocks[self.DATA_SECTION_START] = Word()
        self.mem_blocks[self.STACK_POINTER] = Word()
        self.mem_blocks[self.GLOBAL_POINTER] = Word()

    def store(self, address, data) -> None:
        if self.__is_valid_address(address=address):
            self.mem_blocks[address] = Word(data)
            self.access_count[3] += 1
        else:
            raise MemoryException("Not valid address")

    def load(self, address) -> Word:
        if self.__is_valid_address(address=address):
            if self.l1 and self.l1.hit(address):
                return self.l1.load(address)
            elif self.l2 and self.l2.hit(address):
                return self.l2.load(address)
            self.access_count[3] += 1
            data = self.mem_blocks.get(address, Word())

            if self.l2 and self.l2.need_writeback(address):
                # TODO writeback on mem -> L2
                pass
            
            return data
        else:
            raise MemoryException("Not valid address")

    def __is_valid_address(self, address):
        return address in self.mem_blocks or address % 4 == 0

    def __str__(self) -> str:
        return str({str(k): str(v) for k, v in self.mem_blocks.items()})


class MemoryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
