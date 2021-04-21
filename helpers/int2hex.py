class Int2Hex:
    @staticmethod
    def convert(int_n):
        hex_n = hex(int_n)
        return '0x' + hex_n[2:].zfill(8)
