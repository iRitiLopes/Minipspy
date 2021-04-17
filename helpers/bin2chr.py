class Bin2Chr:
    @staticmethod
    def convert(bin, size=8):
        bin = bin.zfill(size)
        char_int = int(bin, 2)
        if char_int == 0:
            return '\0'
        return chr(char_int)
