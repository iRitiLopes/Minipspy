from minips.cache.policy.random_access import RandomAccess
from minips.cache.mapping.direct import DirectMapping
from minips.memory import Memory
from minips.cache.l1 import L1Cache
from minips.cache.l1d import L1DCache
from minips.cache.l1i import L1ICache
from minips.cache.l2 import L2Cache

class MemoryController:
    def __init__(self, mem_mode):
        self.mem_mode = mem_mode
        self.memory = Memory()
        self.l1 = L1Cache(size=1024, mapping='direct')
        self.l1d = L1DCache(size=512)
        self.l1i = L1ICache(size=512)
        self.l2 = L2Cache(size=2048)

        self.mem_config = {
            1: {
                "levels": 1,
                "mapping": DirectMapping(),
                "policy": RandomAccess()
            },
            2: {
                "levels": 1,
                ""
            }
        }
    
    def load(self, address):
        if self.mem_mode == 1:
            return self.memory.load(address)

    def store(self, address, data):
        if self.mem_mode == 1:
            return self.memory.store(address, data)