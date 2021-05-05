from helpers.twocomplement import TwoComp
from helpers.bin2str import Bin2Str
from minips.word import Word
from helpers.bin2int import Bin2Int


class Register:
    def __init__(self, name: str, value: Word = Word()):
        self.name = name
        self.value = value

    def to_signed_int(self):
        return TwoComp.two_complement(self.value.data, 32)

    def to_unsigned_int(self):
        return TwoComp.unsigned(self.value.data, 32)

    def to_string(self):
        Bin2Str.convert(self.value.data)

    def get_data(self):
        return TwoComp.two_complement(self.value.data, 32)
    
    def get_data_unsigned(self):
        return TwoComp.unsigned(self.value.data, 32)

class Registers:
    def __init__(self):
        self.registers = {
            0: Register("$zero"),
            1: Register("$at"),
            2: Register("$v0"),
            3: Register("$v1"),
            4: Register("$a0"),
            5: Register("$a1"),
            6: Register("$a2"),
            7: Register("$a3"),
            8: Register("$t0"),
            9: Register("$t1"),
            10: Register("$t2"),
            11: Register("$t3"),
            12: Register("$t4"),
            13: Register("$t5"),
            14: Register("$t6"),
            15: Register("$t7"),
            16: Register("$s0"),
            17: Register("$s1"),
            18: Register("$s2"),
            19: Register("$s3"),
            20: Register("$s4"),
            21: Register("$s5"),
            22: Register("$s6"),
            23: Register("$s7"),
            24: Register("$t8"),
            25: Register("$t9"),
            26: Register("$k0"),
            27: Register("$k1"),
            28: Register("$gp"),
            29: Register("$sp"),
            30: Register("$fp"),
            31: Register("$ra"),
            "HI": Register("HI"),
            "LO": Register("LO")
        }

    def get_hi(self):
        return self.registers.get("HI")

    def set_hi_value(self, value):
        self.registers["HI"].value = Word(value)

    def get_lo(self):
        return self.registers.get("LO")

    def set_lo_value(self, value):
        self.registers["LO"].value = Word(value)

    def get_register(self, num) -> Register:
        if self.__is_valid_register(num):
            return self.registers.get(num)
        else:
            raise InvalidRegister(
                "Invalid Register, there only 32 valid registers"
            )

    def get_register_value(self, num: int):
        if self.__is_valid_register(num):
            return self.get_register(num).value
        else:
            raise InvalidRegister(
                "Invalid Register, there only 32 valid registers"
            )

    def get_register_name(self, num: int):
        if self.__is_valid_register(num):
            return self.get_register(num).name
        else:
            raise InvalidRegister(
                "Invalid Register, there only 32 valid registers"
            )

    def set_register_value(self, num: int, value):
        if self.__is_valid_register(num):
            if num == 0:
                return
            self.registers[num].value = Word((value or 0))
        else:
            raise InvalidRegister(
                "Invalid Register, there only 32 valid registers"
            )

    def __is_valid_register(self, num: int):
        return num >= 0 and num <= 31


class InvalidRegister(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
