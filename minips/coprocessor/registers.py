from helpers.bin2int import Bin2Int
from helpers.bin2float import Bin2Float
from helpers.bin2str import Bin2Str
from minips.word import Word


class Register:
    def __init__(self, name: str, value: Word = Word()):
        self.name = name
        self.value = value

    def to_signed_int(self):
        return Bin2Int.convert(self.value.data)

    def to_unsigned_int(self):
        return Bin2Int.convert(self.value.data, signed=False)

    def to_single_precision(self):
        return Bin2Float.convert(self.get_data())

    def to_double_precision(self):
        return Bin2Float.convert(self.get_data(), doubled=True)

    def to_string(self):
        Bin2Str.convert(self.value.data)

    def get_data(self):
        return self.value.data


class Registers:
    def __init__(self):
        self.registers = {
            0: Register("$f0"),
            1: Register("$f1"),
            2: Register("$f2"),
            3: Register("$f3"),
            4: Register("$f4"),
            5: Register("$f5"),
            6: Register("$f6"),
            7: Register("$f7"),
            8: Register("$f8"),
            9: Register("$f9"),
            10: Register("$f10"),
            11: Register("$f11"),
            12: Register("$f12"),
            13: Register("$f13"),
            14: Register("$f14"),
            15: Register("$f15"),
            16: Register("$f16"),
            17: Register("$f17"),
            18: Register("$f18"),
            19: Register("$f19"),
            20: Register("$f20"),
            21: Register("$f21"),
            22: Register("$f22"),
            23: Register("$f23"),
            24: Register("$f24"),
            25: Register("$f25"),
            26: Register("$f26"),
            27: Register("$f27"),
            28: Register("$f28"),
            29: Register("$f29"),
            30: Register("$f30"),
            31: Register("$f31"),
        }

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
            self.registers[num].value = Word(value)
        else:
            raise InvalidRegister(
                "Invalid Register, there only 32 valid registers"
            )

    def __is_valid_register(self, num: int):
        return num >= 0 and num <= 31


class InvalidRegister(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
