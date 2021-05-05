from helpers.twocomplement import TwoComp
from typing import Tuple
from minips.registers import Registers


class J_BaseFunction:
    instruction_name = ""
    funct_code = ""

    def __call__(self, word) -> None:
        self.word = word
        self.op_code = self.word.get_opcode()
        self.address_raw = ( ((1 << 26) - 1)  &  (self.word.data >> (0) ) )
        self.jump_address = TwoComp.two_complement(self.address_raw, 26)
        return self

    def decode(self, *args, **kwargs) -> str:
        pass

    def execute(self, registers: Registers, program_counter, *args, **kwargs) -> Tuple[Registers, int]:  # noqa: E501
        pass
