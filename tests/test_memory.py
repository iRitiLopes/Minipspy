from minips.memory import Memory, MemoryException
from minips.word import Word
import pytest


class TestMemory:
    def test_load_in_address_multiple_4_bytes(self):
        mem = Memory()
        for x in range(0, 64, 4):
            data = mem.load(x)
            assert isinstance(data, Word)

    def test_not_load_int_address_not_multiple_4_bytes(self):
        mem = Memory()

        with pytest.raises(MemoryException):
            mem.load(1)
            mem.load(2)
            mem.load(3)
