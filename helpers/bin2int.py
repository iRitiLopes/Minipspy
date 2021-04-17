class Bin2Int:
    @staticmethod
    def convert(bin, signed=True):
        #bin = bin.zfill(32)
        if not bin:
            return 0
        if signed:
            if bin[0] == '1':
                return int(bin[1:len(bin)], 2)-2**(len(bin)-1)
            else:
                return int(bin[1:len(bin)], 2)
        else:
            return int(bin, 2)
