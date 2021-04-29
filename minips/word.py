class Word(object):
    word_size = 32
    empty = 0x00000000

    def __init__(self, data="") -> None:
        self.data = data
        pass

    def get_opcode(self):
        return self.get_k_bits_from(6, 26)

    def is_empty(self):
        return self.data == ""

    def get_k_bits_from(self, k, from_idx) -> str:
        return ( ((1 << k) - 1)  &  (self.data >> (from_idx) ) )

    def __str__(self) -> str:
        return self.data
