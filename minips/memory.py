from minips.cache import Cache
from minips.word import Word


class Memory(object):
    mem_blocks = {}
    TEXT_SECTION_START = 0x00400000
    DATA_SECTION_START = 0x10010000
    RODATA_SECION_START = 0X00800000
    STACK_POINTER = 0x7fffeffc
    GLOBAL_POINTER = 0x10008000

    def __init__(self, mem_mode, log) -> None:
        self.clean()
        self.log = log
        self.access_count = {
            3: 0, # Identificador memoria
            2: 0, # L2
            1: 0  # L1
        }
        self.mem_mode = mem_mode
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
            if self.mem_mode == 1:
                self.log.debug(f" mem store: {address} {data}")
                return self.__store(address, data)
            if self.cache.hit(address):
                self.log.debug(f" l1 store: {address} {data}")
                self.cache.store(address, data)
            elif self.cache.need_writeback(address):
                self.__writeback(address)
                self.log.debug(f" l1 store writeback: {address} {data}")
                self.cache.store(address, data)
            else:
                self.log.debug(f" l1 store: {address} {data}")
                self.cache.store(address, data)
        else:
            raise MemoryException("Not valid address")
    
    def __writeback(self, address):
        wb_data, wb_address = self.cache.writeback(address)
        self.__store(wb_address, wb_data.data)
    
    def __load(self, address) -> Word:
        self.access_count[3] += 1
        data = self.mem_blocks.get(address, Word())
        return data
    
    def init_store(self, address, data):
        return self.__store(address, data)

    def __store(self, address, data):
        self.mem_blocks[address] = Word(data)

    def load(self, address) -> Word:
        if self.__is_valid_address(address=address):
            if self.mem_mode == 1:
                self.log.debug(f" mem load: {address} {self.mem_blocks.get(address)}")
                return self.__load(address)
            if self.cache.hit(address):
                data = self.cache.load(address)
                self.access_count[1] += 1
                self.log.debug(f" l1 load: {address} {data.data}")
            else:
                data = self.__load(address)
                self.log.debug(f" miss mem load: {address} {self.mem_blocks.get(address)}")
                if self.cache.need_writeback(address):
                    self.log.debug(" writebacking")
                    self.__writeback(address)
                self.cache.store(address, data.data)
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
