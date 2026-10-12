from minips.cache.l1d import L1DCache
from minips.cache.l1i import L1ICache


class L1Splitted:
    def __init__(self, size=512, line_size=32, mode=None, policy=None):
        self.size = size
        self.line_size = line_size
        self.l1i = L1ICache(size, line_size, mode, policy)
        self.l1d = L1DCache(size, line_size, mode, policy)

    def select(self, address_type):
        return self.l1i if address_type == 0 else self.l1d

    def block_address(self, address):
        return address // self.line_size

    def hit(self, address, address_type=1):
        return self.select(address_type).hit(address)

    def load(self, address, via, address_type=1):
        return self.select(address_type).load(address, via)

    def store(self, address, data, via=None, address_type=1):
        self.select(address_type).store(address, data, via=via)

    def need_writeback(self, address, address_type=1):
        return self.select(address_type).need_writeback(address)

    def writeback(self, address, via, address_type=1):
        return self.select(address_type).writeback(address, via)

    def store_line(self, address, data_line, via, address_type=1):
        self.select(address_type).store_line(address, data_line, via)

    def dirty_lines(self):
        yield from self.l1i.dirty_lines()
        yield from self.l1d.dirty_lines()
