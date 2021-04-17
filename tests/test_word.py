from minips.memory import Memory
from minips.word import Word


class TestWord:
    def test_is_syscall(self):
        mem = Memory()
        syscall_hex = 0x0000000c
        syscall_bin = bin(int(syscall_hex))[2:].zfill(32)
        mem.store(mem.TEXT_SECTION_START, syscall_bin)
        assert mem.load(mem.TEXT_SECTION_START).is_syscall()

    def test_is_empty(self):
        empty_word = Word()
        assert empty_word.is_empty()

    def test_get_opcode(self):
        mem = Memory()
        add_immediate_hex = 0x21490001
        add_immediate_bin = bin(int(add_immediate_hex))[2:].zfill(32)
        mem.store(mem.TEXT_SECTION_START, add_immediate_bin)

        op_code = mem.load(mem.TEXT_SECTION_START).get_opcode()
        assert len(op_code) == 6
