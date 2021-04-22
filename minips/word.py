class Word(object):
    word_size = 32
    empty = 0x00000000

    def __init__(self, data="") -> None:
        self.data = data
        pass

    def get_opcode(self):
        return self.get_bits_between(31, 26)

    def is_empty(self):
        return self.data == ""

    def get_bits_between(self, a, b) -> str:
        assert a > b
        return self.data[32 - a - 1:32 - b]

    def __str__(self) -> str:
        return self.data
