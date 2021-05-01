from minips.memory import Memory
from typing import Tuple

from minips.instruction.instructions import BaseInstruction
from minips.instruction.instructions.j_instructions.jump_instruction import \
    JumpInstruction
from minips.instruction.instructions.j_instructions.jumpal_instruction import \
    JumpalInstruction
from minips.registers import Registers
from minips.word import Word


class J_Instruction(BaseInstruction):
    def __init__(self) -> None:
        super().__init__()
        self.instruction_type = 2
        self.functions = {
            0x2: JumpInstruction(),
            0x3: JumpalInstruction(),
        }
    
    def __call__(self, word):
        super().__call__(word)
        self.op_code = self.word.get_opcode()
        self.jump_address = self.word.get_k_bits_from(26, 0)
        return self

    def decode(self, *args, **kwargs):
        return self.functions[self.op_code](self.word).decode(*args, **kwargs)

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        return self.functions[self.op_code](self.word).execute(
            registers=registers,
            program_counter=program_counter,
            memory=memory,
            *args,
            **kwargs
        )
