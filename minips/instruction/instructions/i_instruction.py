from minips.instruction.instructions.i_instructions.bgez_instruction import BGEZInstruction
from minips.instruction.instructions.i_instructions.lhu_instruction import LHUInstruction
from minips.instruction.instructions.i_instructions.blez_instruction import BLEZInstruction
from minips.instruction.instructions.i_instructions.lb_instruction import LBInstruction
from minips.instruction.instructions.i_instructions.slti_instruction import SLTIInstruction
from typing import Tuple

from minips.instruction.instructions import BaseInstruction
from minips.instruction.instructions.i_instructions.addi_instruction import \
    AddiInstruction
from minips.instruction.instructions.i_instructions.addiu_instruction import \
    AddiuInstruction
from minips.instruction.instructions.i_instructions.andi_instruction import \
    AndiInstruction
from minips.instruction.instructions.i_instructions.beq_instruction import \
    BEQInstruction
from minips.instruction.instructions.i_instructions.bne_instruction import \
    BNEInstruction
from minips.instruction.instructions.i_instructions.lui_instruction import \
    LuiInstruction
from minips.instruction.instructions.i_instructions.lw_instruction import \
    LWInstruction
from minips.instruction.instructions.i_instructions.ori_instruction import \
    OriInstruction
from minips.instruction.instructions.i_instructions.sw_instruction import \
    SWInstruction
from minips.memory import Memory
from minips.registers import Registers
from minips.word import Word


class I_Instruction(BaseInstruction):
    def __init__(self, word: Word) -> None:
        super().__init__(word)
        self.word = word
        self.instruction_type = 0
        self.op_code = self.word.get_opcode()
        self.rs = self.word.get_k_bits_from(5, 21)
        self.rt = self.word.get_k_bits_from(5, 16)
        self.imediate = self.word.get_k_bits_from(16, 0)
        self.functions = {
            0x8: AddiInstruction,
            0x9: AddiuInstruction,
            0xc: AndiInstruction,
            0x4: BEQInstruction,
            0x5: BNEInstruction,
            0x6: BLEZInstruction,
            0x1: BGEZInstruction,
            '100000': LBInstruction,
            '100100': {'name': 'LBU', 'funct': ''},
            '100101': LHUInstruction,
            '110000': {'name': 'LL', 'funct': ''},
            0xf: LuiInstruction,
            0x23: LWInstruction,
            0xd: OriInstruction,
            0xa: SLTIInstruction,
            '001011': {'name': 'SLTIU', 'funct': ''},
            '101000': {'name': 'SB', 'funct': ''},
            '111000': {'name': 'SC', 'funct': ''},
            '101001': {'name': 'SH', 'funct': ''},
            0x2b: SWInstruction
        }

    def decode(self, registers: Registers, *args, **kwargs):
        return self.functions[self.op_code](self.word).decode(registers, *args, **kwargs)  # noqa: E501

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        return self.functions[self.op_code](self.word).execute(
            registers=registers,
            program_counter=program_counter,
            memory=memory,
            *args,
            **kwargs
        )
