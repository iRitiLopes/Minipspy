class TwoComp:
    @staticmethod
    def two_complement(value, n_bits):
        if value <= 0:
            return value
        """compute the 2's complement of int value val"""
        if (value & (1 << (n_bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            value = value - (1 << n_bits)        # compute negative value
        return value       

    def unsigned(value, n_bits):
        if value <= 0:
            value = value & ((1 << n_bits) - 1)
        return value

