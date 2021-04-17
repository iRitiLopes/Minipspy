import struct


class Float2Bits:
    @staticmethod
    def convert(f_num, doubled=False):
        double_mask = 0b1111111111111111111111111111111111111111111111111111111111111111
        single_mask = 0b11111111111111111111111111111111
        if doubled:
            return bin(struct.unpack('L', struct.pack('d', f_num))[0] & double_mask)[2:].zfill(64)
        else:
            return bin(struct.unpack('I', struct.pack('f', f_num))[0] & single_mask)[2:].zfill(32)
