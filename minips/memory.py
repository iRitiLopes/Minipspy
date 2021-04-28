from minips.cache import Cache
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
        self.cache = Cache()

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
            if self.cache.hit(address):
                self.cache.store(address, data)
            elif self.cache.need_writeback(address):
                    self.__writeback(address)
        else:
            raise MemoryException("Not valid address")
    
    def __writeback(self, address):
        wb_data, wb_address = self.cache.writeback(address)
        self.__store(wb_address, wb_data)
    
    def __load(self, address) -> Word:
        self.access_count[3] += 1
        data = self.mem_blocks.get(address, Word())
        return data

    def __store(self, address, data):
        self.mem_blocks[address] = Word(data)
        self.access_count[3] += 1

    def load(self, address) -> Word:
        if self.__is_valid_address(address=address):
            if self.mem_mode == 1:
                return self.__load(address)
            if self.cache.hit(address):
                data = self.cache.load(address)
            else:
                data = self.__load(address)
                if self.cache.need_writeback(address):
                    self.__writeback(address)
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
