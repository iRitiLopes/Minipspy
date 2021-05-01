from helpers.twocomplement import TwoComp
from minips.word import Word
from helpers.bin2int import Bin2Int
from minips.memory import Memory
from typing import Tuple
from minips.registers import Registers


class Floating_I_BaseFunction:
    instruction_name = ""
    funct_code = ""

    def __call__(self, word: Word) -> None:
        self.word = word
        self.op_code = self.word.get_opcode()
        self.base = self.word.get_k_bits_from(5, 21)
        self.ft = self.word.get_k_bits_from(5, 16)
        self.offset = TwoComp.two_complement(self.word.get_k_bits_from(16, 0), 16)
        self.ft_number = self.ft
        return self

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        pass

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        pass
