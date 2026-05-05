import struct


class Int2Float:
    @staticmethod
    def convert(n, doubled=False):
        if doubled:
            return struct.unpack('d', struct.pack('Q', n))[0]
        else:
            return struct.unpack('f', struct.pack('I', n))[0]
