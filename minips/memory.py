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
        self.cache = Cache(config=mem_mode)

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
            self.log.trace(f"W {hex(address)} (line# {hex(address // 32)})")
            if self.mem_mode == 1:
                self.log.debug(f" mem store: {address} {data}")
                return self.__store(address, data)
            self.log.debug(f"\tL1: write: {hex(self.cache.l1_line(address))}")
            hit, via = self.cache.hit(address)

            if hit:
                self.cache.store(address, data, via=via)
            else:
                self.log.debug(f"\tL1: Miss")
                self.log.debug(f"\t\tRAM: read line# {hex(self.cache.l1_line(address))}")
                self.__store(address, data)
                data_line = self.__load_line(address, self.cache.l1.line_size)
                self.log.debug(f"\t\tRAM: Hit")
                self.log.debug(f"\tL1: Replace to include line# {hex(self.cache.l1_line(address))}")
                need_writeback, via = self.cache.need_writeback(address)
                self.log.debug("\tL1: Random replacement policy. Way#0")
                if need_writeback:
                    self.__writeback(address, via)
                else:
                    self.log.debug(f"\tL1: Line clean/invalid. No need to write back.")
                self.cache.store_line(address, data_line, via)
        else:
            raise MemoryException("Not valid address")
    
    def __writeback(self, address, via):
        wb_data, wb_address = self.cache.writeback(address, via=via)
        self.log.debug(f"\t\tRAM: write: {hex(address)}")
        self.log.debug(f"\t\tRAM: Hit")
        for idx_offset, data in enumerate(wb_data):
            self.__store(wb_address + idx_offset * 4, data.data)
    
    def __load(self, address) -> Word:
        self.access_count[3] += 1
        data = self.mem_blocks.get(address, Word())
        return data
    
    def __load_line(self, line, line_size):
        line = (line // line_size) * line_size
        data_line = []
        for offset in range(0, line_size, 4):
            data = self.mem_blocks.get(line + offset, Word()).data
            data_line.append(data)
        return data_line
            
    
    def init_store(self, address, data):
        return self.__store(address, data)

    def __store(self, address, data):
        self.mem_blocks[address] = Word(data)

    def load(self, address) -> Word:
        if self.__is_valid_address(address=address):
            if address >= self.TEXT_SECTION_START and address < self.RODATA_SECION_START:
                self.log.trace(f"I {hex(address)} (line# { hex(address // 32)} )")
            else:
                self.log.trace(f"R {hex(address)} (line# { hex(address // 32)} )")
            if self.mem_mode == 1:
                data = self.__load(address)
            else:
                data = self.__load_from_cache(address)
            return data

        else:
            raise MemoryException("Not valid address")
    
    def __load_from_cache(self, address):
        self.log.debug(f"\tL1: read line# {hex(self.cache.l1_line(address))}")
        hit, via = self.cache.hit(address)
        if hit:
            data = self.cache.load(address, via)
            self.access_count[1] += 1
            self.log.debug(f"\tL1: Hit")
        else:
            self.log.debug(f"\tL1: Miss")
            data = self.__load(address)
            data_line = self.__load_line(address, self.cache.l1.line_size)
            self.log.debug(f"\t\tRAM: read line# {hex(self.cache.l1_line(address))}")
            self.log.debug(f"\t\tRAM: Hit")
            self.log.debug(f"\tL1: Replace to include line# {hex(self.cache.l1_line(address))}")
            need_writeback, via = self.cache.need_writeback(address)
            self.log.debug("\tL1: Random replacement policy. Way#0")

            if need_writeback:
                self.__writeback(address, via)
            else:
                self.log.debug(f"\tL1: Line clean/invalid. No need to write back.")
            self.cache.store_line(address, data_line, via=via)
        return data

    def __is_valid_address(self, address):
        return address in self.mem_blocks or address % 4 == 0

    def __str__(self) -> str:
        return str({str(k): str(v) for k, v in self.mem_blocks.items()})


class MemoryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
