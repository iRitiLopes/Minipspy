from minips.cache import Cache
from minips.word import Word


class Memory:
    TEXT_SECTION_START = 0x00400000
    DATA_SECTION_START = 0x10010000
    RODATA_SECION_START = 0x00800000
    STACK_POINTER = 0x7fffeffc
    GLOBAL_POINTER = 0x10008000

    def __init__(self, mem_mode, log):
        self.mem_mode = mem_mode
        self.log = log
        self.clean()

    def clean(self):
        self.mem_blocks = {address: Word() for address in (
            self.TEXT_SECTION_START, self.DATA_SECTION_START,
            self.STACK_POINTER, self.GLOBAL_POINTER)}
        self.access_count = {1: 0, 2: 0, 3: 0}
        self.l1_access_count = {'instruction': 0, 'data': 0}
        self.cache = Cache(self.mem_mode)

    def _validate(self, address):
        if not isinstance(address, int) or not 0 <= address <= 0xfffffffc or address % 4:
            raise MemoryException("Not valid aligned 32-bit address")

    def init_store(self, address, data):
        """Load program sections before execution (bypasses caches)."""
        self._validate(address)
        self.mem_blocks[address] = Word(data)

    def _ram_line(self, address, size):
        self.access_count[3] += 1
        base = address - address % size
        self.log.debug(f"RAM: read line at {hex(base)}")
        return [self.mem_blocks.get(base + offset, Word(None)).data
                for offset in range(0, size, 4)]

    def _ram_writeback(self, line):
        self.access_count[3] += 1
        self.log.debug(f"RAM: write line at {hex(line[0].address)}")
        for word in line:
            if word.data.data is not None:
                self.mem_blocks[word.address] = Word(word.data.data)
            word.clean_this()

    def _l2_line(self, address):
        l2 = self.cache.l2
        self.access_count[2] += 1
        hit, via = l2.hit(address)
        self.log.debug(f"L2: {'Hit' if hit else 'Miss'} {hex(address)}")
        if not hit:
            dirty, via = l2.need_writeback(address)
            if dirty:
                self._ram_writeback(l2.writeback(address, via)[0])
            l2.store_line(address, self._ram_line(address, l2.line_size), via)
        l2.load(address, via)  # Touch the whole line for replacement policy.
        return via

    def _lower_writeback(self, line):
        if self.cache.l2 is None:
            self._ram_writeback(line)
        else:
            l2 = self.cache.l2
            via = self._l2_line(line[0].address)
            for word in line:
                if word.data.data is not None:
                    l2.store(word.address, word.data.data, via=via)
                word.clean_this()

    def _ensure_l1(self, address):
        self.access_count[1] += 1
        kind = ('instruction' if self.TEXT_SECTION_START <= address < self.RODATA_SECION_START
                else 'data')
        self.l1_access_count[kind] += 1
        hit, via = self.cache.hit(address)
        self.log.debug(f"L1: {'Hit' if hit else 'Miss'} {hex(address)}")
        if not hit:
            dirty, via = self.cache.need_writeback(address)
            if dirty:
                self._lower_writeback(self.cache.writeback(address, via)[0])
            if self.cache.l2 is None:
                data = self._ram_line(address, self.cache.l1.line_size)
            else:
                l2_via = self._l2_line(address)
                data = [w.data.data for w in self.cache.l2.writeback(address, l2_via)[0]]
            self.cache.store_line(address, data, via)
        return via

    def load(self, address):
        self._validate(address)
        kind = 'I' if self.TEXT_SECTION_START <= address < self.RODATA_SECION_START else 'R'
        self.log.trace(f"{kind} {hex(address)}")
        if self.mem_mode == 1:
            self.access_count[3] += 1
            return Word(self.mem_blocks.get(address, Word(None)).data)
        return self.cache.load(address, self._ensure_l1(address))

    def store(self, address, data):
        self._validate(address)
        self.log.trace(f"W {hex(address)}")
        if self.mem_mode == 1:
            self.access_count[3] += 1
            self.mem_blocks[address] = Word(data)
        else:
            self.cache.store(address, data, via=self._ensure_l1(address))

    def flush(self):
        """Write all dirty levels to RAM, retaining clean cached copies."""
        if self.cache.l1 is not None:
            for line in self.cache.l1.dirty_lines():
                self._lower_writeback(line)
        if self.cache.l2 is not None:
            for line in self.cache.l2.dirty_lines():
                self._ram_writeback(line)

    def __str__(self):
        return str({str(k): str(v) for k, v in self.mem_blocks.items()})


class MemoryException(Exception):
    pass
