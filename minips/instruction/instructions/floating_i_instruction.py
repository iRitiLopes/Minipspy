from minips.instruction.instructions.floating_i_instructions.swc1_instruction import SWC1Instruction
from minips.instruction.instructions.floating_i_instructions.ldc1_instruction import LDC1Instruction
from minips.instruction.instructions.floating_i_instructions.lwc1_instruction import LWC1Instruction
from typing import Tuple

from minips.instruction.instructions import BaseInstruction
from minips.memory import Memory
from minips.registers import Registers
from minips.word import Word


class Floating_I_Instruction(BaseInstruction):

    def __init__(self) -> None:
        super().__init__()
        self.instruction_type = 3
        self.functions = {
            0x31: LWC1Instruction(),
            0x35: LDC1Instruction(),
            0x39: SWC1Instruction()
        }
    
    def __call__(self, word):
        super().__call__(word)
        self.opcode = ( ((1 << 6) - 1)  &  (self.word.data >> (26) ) )
        return self

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
