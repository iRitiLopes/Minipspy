class TwoComp:
    @staticmethod
    def negate(value):
        n_bits = len(bin(value)[2:])
        """compute the 2's complement of int value val"""
        if (value & (1 << (n_bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            value = value - (1 << n_bits)        # compute negative value
        return value       


