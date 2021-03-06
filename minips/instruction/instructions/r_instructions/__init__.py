from helpers.bin2int import Bin2Int
from minips.memory import Memory
from typing import Tuple
from minips.registers import Registers


class R_BaseFunction:
    instruction_name = ""
    funct_code = ""
    
    def __call__(self, word) -> None:
        self.word = word
        self.rs = ( ((1 << 5) - 1)  &  (self.word.data >> (21) ) )
        self.rt = ( ((1 << 5) - 1)  &  (self.word.data >> (16) ) )
        self.rd = ( ((1 << 5) - 1)  &  (self.word.data >> (11) ) )
        self.shamt = ( ((1 << 5) - 1)  &  (self.word.data >> (6) ) )
        self.funct = ( ((1 << 6) - 1)  &  (self.word.data >> (0) ) )
        self.rs_number = self.rs
        self.rt_number = self.rt
        self.rd_number = self.rd
        self.shamt_value = self.shamt
        return self

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        pass

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int]:  # noqa: E501
        pass
