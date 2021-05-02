from minips.word import Word
from helpers.bin2int import Bin2Int
from minips.memory import Memory
from typing import Tuple
from minips.coprocessor.registers import Registers


class Floating_R_BaseFunction:
    instruction_name = ""
    funct_code = ""

    def __call__(self, word: Word) -> None:
        self.word = word
        self.op_code = self.word.get_opcode()
        self.fmt = ( ((1 << 5) - 1)  &  (self.word.data >> (21) ) )
        self.ft = ( ((1 << 5) - 1)  &  (self.word.data >> (16) ) )
        self.fs = ( ((1 << 5) - 1)  &  (self.word.data >> (11) ) )
        self.fd = ( ((1 << 5) - 1)  &  (self.word.data >> (6) ) )

        self.ft_number = self.ft
        self.fs_number = self.fs
        self.fd_number = self.fd
        return self

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        pass

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        pass
