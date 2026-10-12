"""Compatibility facade for the former experimental memory controller."""
from helpers.log import Log
from minips.memory import Memory


class MemoryController:
    def __init__(self, mem_mode=1, log=None):
        self.mem_mode = mem_mode
        self.memory = Memory(mem_mode, log if log is not None else Log())
        self.l1 = self.memory.cache.l1
        self.l2 = self.memory.cache.l2

    def load(self, address):
        return self.memory.load(address)

    def store(self, address, data):
        self.memory.store(address, data)

    def flush(self):
        self.memory.flush()
