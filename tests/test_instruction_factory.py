import pytest
from minips.word import Word
from minips.instruction.factory import InstructionFactory
from minips.instruction.instructions.r_instruction import R_Instruction
from minips.instruction.instructions.i_instruction import I_Instruction
from minips.instruction.instructions.j_instruction import J_Instruction
from minips.instruction.instructions.floating_r_instruction import \
    Floating_R_Instruction
from minips.instruction.instructions.floating_i_instruction import \
    Floating_I_Instruction


class TestInstructionFactory:
    def test_opcode_0x00_returns_r_instruction(self):
        factory = InstructionFactory()
        word = Word(0x00000020)
        instr = factory.factory(word)
        assert isinstance(instr, R_Instruction)
        assert instr.instruction_type == 1

    def test_opcode_0x02_returns_j_instruction(self):
        factory = InstructionFactory()
        word = Word(0x08000000)
        instr = factory.factory(word)
        assert isinstance(instr, J_Instruction)
        assert instr.instruction_type == 2

    def test_opcode_0x03_returns_j_instruction(self):
        factory = InstructionFactory()
        word = Word(0x0C000000)
        instr = factory.factory(word)
        assert isinstance(instr, J_Instruction)
        assert instr.instruction_type == 2

    def test_opcode_0x11_returns_floating_r_instruction(self):
        factory = InstructionFactory()
        word = Word(0x46000000)
        instr = factory.factory(word)
        assert isinstance(instr, Floating_R_Instruction)
        assert instr.instruction_type == 4

    def test_opcode_0x31_returns_floating_i_instruction(self):
        factory = InstructionFactory()
        word = Word(0xC4000000)
        instr = factory.factory(word)
        assert isinstance(instr, Floating_I_Instruction)
        assert instr.instruction_type == 3

    def test_opcode_0x35_returns_floating_i_instruction(self):
        factory = InstructionFactory()
        word = Word(0xD4000000)
        instr = factory.factory(word)
        assert isinstance(instr, Floating_I_Instruction)
        assert instr.instruction_type == 3

    def test_opcode_0x39_returns_floating_i_instruction(self):
        factory = InstructionFactory()
        word = Word(0xE4000000)
        instr = factory.factory(word)
        assert isinstance(instr, Floating_I_Instruction)
        assert instr.instruction_type == 3

    def test_opcode_0x3d_returns_floating_i_instruction(self):
        factory = InstructionFactory()
        word = Word(0xF4000000)
        instr = factory.factory(word)
        assert isinstance(instr, Floating_I_Instruction)
        assert instr.instruction_type == 3

    def test_unknown_opcode_returns_i_instruction_as_default(self):
        factory = InstructionFactory()
        word = Word(0x20000000)
        instr = factory.factory(word)
        assert isinstance(instr, I_Instruction)
        assert instr.instruction_type == 0

    def test_factory_reuses_same_instances(self):
        factory = InstructionFactory()
        word = Word(0x00000020)
        instr1 = factory.factory(word)
        word2 = Word(0x00000021)
        instr2 = factory.factory(word2)
        assert instr1 is instr2

    def test_empty_word_raises(self):
        factory = InstructionFactory()
        word = Word(data=None)
        with pytest.raises(TypeError):
            factory.factory(word)
