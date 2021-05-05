from minips.instruction.instructions import BaseInstruction
from minips.instruction.instructions.floating_i_instruction import \
    Floating_I_Instruction
from minips.instruction.instructions.floating_r_instruction import \
    Floating_R_Instruction
from minips.instruction.instructions.i_instruction import I_Instruction
from minips.instruction.instructions.j_instruction import J_Instruction
from minips.instruction.instructions.r_instruction import R_Instruction
from minips.word import Word


class InstructionFactory:
    def __init__(self):
        self.i_inst = I_Instruction()
        self.instructions = {
            0x0: R_Instruction(),
            0x2: J_Instruction(),
            0x3: J_Instruction(),
            0x11: Floating_R_Instruction(),
            0x31: Floating_I_Instruction(),
            0x35: Floating_I_Instruction(),
            0x39: Floating_I_Instruction(),
            0x3d: Floating_I_Instruction()
        }

    def factory(self, word: Word) -> BaseInstruction:
        op_code = word.get_opcode()
        if word.is_empty():
            raise Exception("Empty instruction")
        return self.instructions.get(op_code, self.i_inst)(word)
