class Word(object):
    word_size = 32
    empty = 0x00000000

    def __init__(self, data=0) -> None:
        self.data = data
        pass

    def get_opcode(self):
        return ( ((1 << 6) - 1)  &  (self.data >> (26) ) )

    def is_empty(self):
        return self.data is None

    def get_k_bits_from(self, k, from_idx) -> int:
        return ( ((1 << k) - 1)  &  (self.data >> (from_idx) ) )

    def __str__(self) -> str:
        return hex(self.data)
