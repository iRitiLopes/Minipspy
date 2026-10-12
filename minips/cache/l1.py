from minips.cache.mapping.direct import DirectMapping
from minips.cache.policy.random_access import RandomAccess
from minips.cache.controller import CacheData
from minips.word import Word


class L1Cache:
    """Set associative, write-back cache; sizes are measured in bytes."""

    def __init__(self, size=1024, line_size=32, mode=None, policy=None):
        self.size = size
        self.line_size = line_size
        self.mode = mode if mode is not None else DirectMapping()
        self.policy = policy if policy is not None else RandomAccess()
        self.n_vias = self.mode.n_vias
        self.block_size = line_size * self.n_vias
        if (line_size < 4 or line_size & (line_size - 1)
                or self.n_vias < 1 or size % self.block_size):
            raise ValueError("Invalid cache geometry")
        self.num_blocks = size // self.block_size
        if not self.num_blocks or self.num_blocks & (self.num_blocks - 1):
            raise ValueError("Number of cache sets must be a power of two")
        self.num_words = line_size // 4
        self.nbits_byte_offset = line_size.bit_length() - 1
        self.nbits_block_offset = self.num_blocks.bit_length() - 1
        self.nbits_tag = 32 - self.nbits_byte_offset - self.nbits_block_offset
        self.cache = {
            i: [[CacheData(None, 0, 0) for _ in range(self.num_words)]
                for _ in range(self.n_vias)]
            for i in range(self.num_blocks)
        }
        self.clock = 0

    def _touch(self, line):
        self.clock += 1
        for word in line:
            word.timestamp = self.clock

    def hit(self, address, **kwargs):
        for via, line in enumerate(self.cache[self.block_index(address)]):
            if line[0].valid and line[0].tag == self.tag(address):
                return True, via
        return False, -1

    def load(self, address, via, **kwargs):
        line = self.cache[self.block_index(address)][via]
        self._touch(line)
        return Word(line[self.byte_index(address)].data.data)

    def need_writeback(self, address, **kwargs):
        hit, via = self.hit(address)
        if hit:
            return False, via
        block = self.cache[self.block_index(address)]
        for via, line in enumerate(block):
            if not line[0].valid:
                return False, via
        via = self.policy.run(from_n=0, to_n=self.n_vias - 1, block=block)
        return any(w.valid and w.dirty for w in block[via]), via

    def writeback(self, address, via, **kwargs):
        line = self.cache[self.block_index(address)][via]
        return line, line[0].address

    def store_line(self, address, data_line, via, **kwargs):
        if len(data_line) != self.num_words:
            raise ValueError("Incorrect cache line length")
        base = address - address % self.line_size
        line = [CacheData(data, self.tag(address), base + i * 4)
                for i, data in enumerate(data_line)]
        for word in line:
            word.valid_this()
        self.cache[self.block_index(address)][via] = line
        self._touch(line)

    def store(self, address, data, via=None, **kwargs):
        hit, found = self.hit(address)
        if not hit:
            raise ValueError("Allocate a cache line before storing")
        line = self.cache[self.block_index(address)][found]
        word = line[self.byte_index(address)]
        word.set_data(data)
        word.dirty_this()
        self._touch(line)

    def byte_index(self, address):
        return address % self.line_size // 4

    def block_index(self, address):
        return address // self.line_size % self.num_blocks

    def block_address(self, address):
        return address // self.line_size

    def tag(self, address):
        return address // self.line_size // self.num_blocks

    def parse_address(self, address):
        return self.tag(address), self.block_index(address), address % self.line_size

    def dirty_lines(self):
        for block in self.cache.values():
            for line in block:
                if any(w.valid and w.dirty for w in line):
                    yield line
