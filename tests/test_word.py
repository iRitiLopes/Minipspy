from minips.word import Word


class TestWord:
    def test_is_syscall(self):
        syscall_hex = 0x0000000c
        word = Word(syscall_hex)
        assert word.get_opcode() == 0
        assert word.get_k_bits_from(6, 0) == 0x0c

    def test_is_empty(self):
        empty_word = Word(data=None)
        assert empty_word.is_empty()
        assert not Word().is_empty()

    def test_get_opcode(self):
        add_immediate_hex = 0x21490001
        assert Word(add_immediate_hex).get_opcode() == 0x08
