class Int2Bits:
    @staticmethod
    def convert(int_n, size=32):
        b_word = bin(int_n & 0b11111111111111111111111111111111) # from stackoverflow https://stackoverflow.com/questions/28631301/negative-integer-to-signed-32-bit-binary
        b_word = b_word[2:].zfill(size)
        return b_word
