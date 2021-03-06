from helpers.twocomplement import TwoComp
from helpers.bin2int import Bin2Int
from minips.memory import Memory
from typing import Tuple
from minips.registers import Registers


class I_BaseFunction:
    instruction_name = ""
    funct_code = ""

    def __init__(self) -> None:
        pass

    def __call__(self, word) -> None:
        self.word = word
        self.op_code = self.word.get_opcode()
        self.rs = ( ((1 << 5) - 1)  &  (self.word.data >> (21) ) )
        self.rt = ( ((1 << 5) - 1)  &  (self.word.data >> (16) ) )
        self.imediate =  TwoComp.two_complement(( ((1 << 16) - 1)  &  (self.word.data >> (0) ) ), 16) 
        self.rs_number = self.rs
        self.rt_number = self.rt
        return self

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        pass

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        pass
