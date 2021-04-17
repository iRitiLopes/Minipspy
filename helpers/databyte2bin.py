class DataByte2Bits:
    @staticmethod
    def convert(byte, size=32):
        word = byte[::-1].hex()
        b_word = bin(int(word, 16))
        b_word = b_word[2:].zfill(size)
        return b_word
