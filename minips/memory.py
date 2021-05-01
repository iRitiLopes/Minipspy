from helpers.bin2int import Bin2Int
from minips.word import Word
from minips.cache.l1 import L1Cache
from minips.cache.l1d import L1DCache
from minips.cache.l1i import L1ICache
from minips.cache.l2 import L2Cache


class Memory(object):
    mem_blocks = {}
    TEXT_SECTION_START = 0x00400000
    DATA_SECTION_START = 0x10010000
    RODATA_SECION_START = 0X00800000
    STACK_POINTER = 0x7fffeffc
    GLOBAL_POINTER = 0x10008000

    def __init__(self, mem_mode) -> None:
        self.clean()
        self.access_count = {
            3: 0, # Identificador memoria
            2: 0,
            1: 0
        }
        self.mem_mode = mem_mode
        self.l1 = L1Cache()

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
            self.access_count[3] += 1
            data = self.mem_blocks.get(address, Word(data=None))
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
