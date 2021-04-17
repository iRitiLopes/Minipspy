from helpers.bin2int import Bin2Int
from minips.memory import Memory
from typing import Tuple
from minips.registers import Registers


class I_BaseFunction:
    instruction_name = ""
    funct_code = ""

    def __init__(self, word) -> None:
        self.word = word
        self.op_code = self.word.get_opcode()
        self.rs = self.word.get_bits_between(25, 21)
        self.rt = self.word.get_bits_between(20, 16)
        self.imediate = self.word.get_bits_between(15, 0)
        self.rs_number = Bin2Int.convert(self.rs, signed=False)
        self.rt_number = Bin2Int.convert(self.rt, signed=False)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        pass

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        pass
