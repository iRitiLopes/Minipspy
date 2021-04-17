class Bin2Str:
    @staticmethod
    def convert(bin, size=32):
        bin = bin.zfill(size)

        char1 = chr(int(bin[0:8], 2))
        char2 = chr(int(bin[8:16], 2))
        char3 = chr(int(bin[16:24], 2))
        char4 = chr(int(bin[24:32], 2))
        print(f"{char4+char3+char2+char1}")
        if int(bin, 2) == 0:
            return '\0'

        string = ""
        for x in range(0, size, 8):
            char_bit = bin[x:x+8]
            char_int = int(char_bit, 2)
            if char_int == 0:
                string += chr(char_int)
            if char_int >= 32:
                char = chr(char_int)
                string += char
        return string[::-1]
