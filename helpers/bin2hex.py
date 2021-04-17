from helpers.bin2int import Bin2Int


class Bin2Hex:
    @staticmethod
    def convert(bin, signed=True):
        return hex(Bin2Int.convert(bin, signed=signed))
