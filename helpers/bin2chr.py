from helpers.bin2int import Bin2Int


class Bin2Chr:
    @staticmethod
    def convert(bin, size=8):
        bin = bin.zfill(size)
        char_int = Bin2Int.convert(bin, False)
        if char_int == 0:
            return '\0'
        return chr(char_int)
