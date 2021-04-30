from minips.instruction.instructions.floating_i_instructions.swc1_instruction import SWC1Instruction
from minips.instruction.instructions.floating_i_instructions.ldc1_instruction import LDC1Instruction
from minips.instruction.instructions.floating_i_instructions.lwc1_instruction import LWC1Instruction
from typing import Tuple

from minips.instruction.instructions import BaseInstruction
from minips.memory import Memory
from minips.registers import Registers
from minips.word import Word


class Floating_I_Instruction(BaseInstruction):

    def __init__(self, word: Word) -> None:
        super().__init__(word)
        self.word = word
        self.instruction_type = 3
        self.opcode = self.word.get_k_bits_from(6, 26)
        self.functions = {
            0x31: LWC1Instruction,
            0x35: LDC1Instruction,
            0x39: SWC1Instruction
        }

    def decode(self, registers: Registers, coprocessor, *args, **kwargs) -> str:
        """
        Receive the registers to be able to translate the register numbers by the name of the registers  # noqa: E501
        """
        return self.functions.get(self.opcode)(self.word).decode(
            registers=registers,
            coprocessor=coprocessor,
            *args,
            **kwargs
        )  # noqa: E501

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        return self.functions[self.opcode](self.word).execute(
            registers=registers,
            program_counter=program_counter,
            memory=memory,
            *args,
            **kwargs
        )
