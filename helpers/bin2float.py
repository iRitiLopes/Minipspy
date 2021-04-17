import struct


class Bin2Float:
    @staticmethod
    def convert(bin, doubled=False):
        if doubled:
            return struct.unpack('d', struct.pack('L', int(bin, 2)))[0]
        else:
            return struct.unpack('f', struct.pack('I', int(bin, 2)))[0]
