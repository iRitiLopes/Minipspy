from minips.instruction.instructions.floating_i_instructions.bc1t_instruction import BC1TInstruction
from minips.instruction.instructions.floating_r_instructions.clts_single_instruction import CLTSingleInstruction
from minips.instruction.instructions.floating_r_instructions.sub_double_instruction import SubDoubleInstruction
from minips.instruction.instructions.floating_r_instructions.sub_single_instruction import SubSingleInstruction
from minips.instruction.instructions.floating_r_instructions.mul_double_instruction import MulDoubleInstruction
from minips.instruction.instructions.floating_r_instructions.mul_single_instruction import MulSingleInstruction
from minips.instruction.instructions.floating_r_instructions.cvts_double_instruction import CVTSDoubleInstruction
from minips.instruction.instructions.floating_r_instructions.div_double_instruction import DivDoubleInstruction
from minips.instruction.instructions.floating_r_instructions.cvtd_word_instruction import CVTDWordInstruction
from minips.instruction.instructions.floating_r_instructions.mov_double_instruction import MOVDoubleInstruction
from minips.instruction.instructions.floating_r_instructions.mov_single_instruction import MOVSingleInstruction
from minips.instruction.instructions.floating_r_instructions.mtc1_instruction import MTC1Instruction
from helpers.bin2int import Bin2Int
from minips.instruction.instructions.floating_r_instructions.mfc1_instruction import MFC1Instruction
from helpers.bin2hex import Bin2Hex
from minips.instruction.instructions.floating_r_instructions.add_double_instruction import AddDoubleInstruction
from minips.instruction.instructions.floating_r_instructions.add_single_instruction import AddSingleInstruction
from typing import Tuple

from minips.instruction.instructions import BaseInstruction

from minips.memory import Memory
from minips.registers import Registers
from minips.word import Word


class Floating_R_Instruction(BaseInstruction):

    def __init__(self, word: Word) -> None:
        super().__init__(word)
        self.word = word
        self.instruction_type = 4
        self.funct = self.word.get_bits_between(5, 0)
        self.large_funct = self.word.get_bits_between(10, 0)
        self.opcode = self.word.get_bits_between(31, 26)
        self.fmt = self.word.get_bits_between(25, 21)
        self.cond = self.word.get_bits_between(3, 0)
        self.functions = {
            '1100': {
                '10000': CLTSingleInstruction
            },
            '01000': BC1TInstruction,
            '000000': {
                '10000': AddSingleInstruction,
                '10001': AddDoubleInstruction
            },
            '000001': {
                '10000': SubSingleInstruction,
                '10001': SubDoubleInstruction
            },
            '000110': {
                '10000': MOVSingleInstruction,
                '10001': MOVDoubleInstruction
            },
            '100001': {
                '10100': CVTDWordInstruction,
                '10001': '',
                '10010': ''
            },
            '100000': {
                '10100': '',
                '10001': CVTSDoubleInstruction,
                '10010': ''
            },
            '000010': {
                '10000': MulSingleInstruction,
                '10001': MulDoubleInstruction,
            },
            '000011': {
                '10000': '',
                '10001': DivDoubleInstruction
            },
            '00000000000': {
                '00000': MFC1Instruction,
                '00100': MTC1Instruction,
            }
        }

    def decode(self, registers: Registers, coprocessor, *args, **kwargs) -> str:
        """
        Receive the registers to be able to translate the register numbers by the name of the registers  # noqa: E501
        """
        base_operation = self.functions.get(self.large_funct,{}).get(self.fmt) \
            or self.functions.get(self.funct, {}).get(self.fmt) \
            or self.functions.get(self.cond, {}).get(self.fmt) \
            or self.functions.get(self.fmt)
        
        return base_operation(self.word).decode(
            registers=registers,
            coprocessor=coprocessor,
            *args,
            **kwargs
        )  # noqa: E501

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        base_operation = self.functions.get(self.large_funct,{}).get(self.fmt) \
            or self.functions.get(self.funct, {}).get(self.fmt) \
            or self.functions.get(self.cond, {}).get(self.fmt) \
            or self.functions.get(self.fmt)
        return base_operation(self.word).execute(
            registers=registers,
            program_counter=program_counter,
            memory=memory,
            *args,
            **kwargs
        )
