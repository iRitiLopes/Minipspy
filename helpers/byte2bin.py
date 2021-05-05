class Byte2Bits:
    @staticmethod
    def convert(byte, size=32):
        word = byte[::-1].hex()
        b_word = int(word, 16)
        return b_word
        b_word = b_word[2:].zfill(size)
        return b_word
