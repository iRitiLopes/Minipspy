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
    r_opcode = '000000'
    jump_opcode = '000010'
    jump_al_opcode = '000011'
    floating_r_opcode = '010001'
    floating_i_instructions = ['110001', '110101', '111001', '111101']

    def factory(self, word: Word) -> BaseInstruction:
        op_code = word.get_opcode()
        if word.is_empty():
            raise Exception("Empty instruction")
        if op_code == self.r_opcode:
            return R_Instruction(word)
        elif op_code == self.jump_opcode or op_code == self.jump_al_opcode:
            return J_Instruction(word)
        elif op_code == self.floating_r_opcode:
            return Floating_R_Instruction(word)
        elif op_code in self.floating_i_instructions:
            return Floating_I_Instruction(word)
        else:
            return I_Instruction(word)
