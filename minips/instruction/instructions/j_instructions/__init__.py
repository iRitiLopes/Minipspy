from helpers.twocomplement import TwoComp
from typing import Tuple
from minips.registers import Registers


class J_BaseFunction:
    instruction_name = ""
    funct_code = ""

    def __init__(self, word) -> None:
        self.word = word
        self.op_code = self.word.get_opcode()
        self.jump_address = TwoComp.two_complement(self.word.get_k_bits_from(26, 0), 26)

    def decode(self, *args, **kwargs) -> str:
        pass

    def execute(self, registers: Registers, program_counter, *args, **kwargs) -> Tuple[Registers, int]:  # noqa: E501
        pass
