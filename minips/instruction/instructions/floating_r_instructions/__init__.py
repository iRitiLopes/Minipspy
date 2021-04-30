from minips.word import Word
from helpers.bin2int import Bin2Int
from minips.memory import Memory
from typing import Tuple
from minips.coprocessor.registers import Registers


class Floating_R_BaseFunction:
    instruction_name = ""
    funct_code = ""

    def __init__(self, word: Word) -> None:
        self.word = word
        self.op_code = self.word.get_opcode()
        self.fmt = self.word.get_k_bits_from(5, 21)
        self.ft = self.word.get_k_bits_from(5, 16)
        self.fs = self.word.get_k_bits_from(5, 11)
        self.fd = self.word.get_k_bits_from(5, 6)

        self.ft_number = self.ft
        self.fs_number = self.fs
        self.fd_number = self.fd

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        pass

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        pass
