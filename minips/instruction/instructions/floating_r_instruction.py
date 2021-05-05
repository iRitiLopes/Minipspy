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

    def __init__(self) -> None:
        super().__init__()
        self.instruction_type = 4
        self.functions_extra = {
            0x0: {
                0x0: MFC1Instruction(),
                0x4: MTC1Instruction(),
            }
        }
        self.functions_cond = {
            0xc: {
                0x10: CLTSingleInstruction()
            },
        }
        self.functions = {
            0x8: BC1TInstruction(),
            0x0: {
                0x10: AddSingleInstruction(),
                0x11: AddDoubleInstruction()
            },
            0x1: {
                0x10: SubSingleInstruction(),
                0x11: SubDoubleInstruction()
            },
            0x6: {
                0x10: MOVSingleInstruction(),
                0x11: MOVDoubleInstruction()
            },
            0x21: {
                0x14: CVTDWordInstruction(),
            },
            0x20: {
                0x11: CVTSDoubleInstruction(),
            },
            0x2: {
                0x10: MulSingleInstruction(),
                0x11: MulDoubleInstruction(),
            },
            0x3: {
                0x11: DivDoubleInstruction()
            },

        }
    
    def __call__(self, word):
        super().__call__(word)
        self.funct = ( ((1 << 6) - 1)  &  (self.word.data >> (0) ) )
        self.large_funct = ( ((1 << 11) - 1)  &  (self.word.data >> (0) ) )
        self.opcode = ( ((1 << 6) - 1)  &  (self.word.data >> (26) ) )
        self.fmt = ( ((1 << 5) - 1)  &  (self.word.data >> (21) ) )
        self.cond = ( ((1 << 4) - 1)  &  (self.word.data >> (0) ) )
        return self

    def decode(self, registers: Registers, coprocessor, *args, **kwargs) -> str:
        """
        Receive the registers to be able to translate the register numbers by the name of the registers  # noqa: E501
        """
        base_operation = self.functions_extra.get(self.large_funct, {}).get(self.fmt) \
            or self.functions.get(self.funct, {}).get(self.fmt) \
            or self.functions_cond.get(self.cond, {}).get(self.fmt) \
            or self.functions.get(self.fmt)

        return base_operation(self.word).decode(
            registers=registers,
            coprocessor=coprocessor,
            *args,
            **kwargs
        )  # noqa: E501

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        base_operation = self.functions_extra.get(self.large_funct, {}).get(self.fmt) \
            or self.functions.get(self.funct, {}).get(self.fmt) \
            or self.functions_cond.get(self.cond, {}).get(self.fmt) \
            or self.functions.get(self.fmt)
        return base_operation(self.word).execute(
            registers=registers,
            program_counter=program_counter,
            memory=memory,
            *args,
            **kwargs
        )
