from minips.instruction.instructions.r_instructions.sra_instruction import SRAInstruction
from minips.instruction.instructions.r_instructions.xor_instruction import XorInstruction
from minips.instruction.instructions.r_instructions.mfhi_instruction import MFHIInstruction
from minips.instruction.instructions.r_instructions.div_instruction import DivInstruction
from minips.instruction.instructions.r_instructions.mflo_instruction import MFLOInstruction
from minips.instruction.instructions.r_instructions.mult_instruction import MultInstruction
from typing import Tuple

from minips.instruction.instructions import BaseInstruction
from minips.instruction.instructions.r_instructions.add_instruction import \
    AddInstruction
from minips.instruction.instructions.r_instructions.addu_instruction import \
    AdduInstruction
from minips.instruction.instructions.r_instructions.and_instruction import \
    AndInstruction
from minips.instruction.instructions.r_instructions.jalr_instruction import \
    JalrInstruction
from minips.instruction.instructions.r_instructions.jr_instruction import \
    JRInstruction
from minips.instruction.instructions.r_instructions.nop_instruction import \
    NopInstruction
from minips.instruction.instructions.r_instructions.nor_instruction import \
    NorInstruction
from minips.instruction.instructions.r_instructions.or_instruction import \
    OrInstruction
from minips.instruction.instructions.r_instructions.sll_instruction import \
    SLLInstruction
from minips.instruction.instructions.r_instructions.slt_instruction import \
    SLTInstruction
from minips.instruction.instructions.r_instructions.sltu_instruction import \
    SLTUInstruction
from minips.instruction.instructions.r_instructions.srl_instruction import \
    SRLInstruction
from minips.instruction.instructions.r_instructions.sub_instruction import \
    SubInstruction
from minips.instruction.instructions.r_instructions.subu_instruction import \
    SubuInstruction
from minips.instruction.instructions.r_instructions.syscall_instruction import \
    SyscallInstruction
from minips.memory import Memory
from minips.registers import Registers
from minips.word import Word


class R_Instruction(BaseInstruction):

    def __init__(self) -> None:
        super().__init__()
        self.instruction_type = 1
        self.functions = {
            0x20: AddInstruction(),
            0x21: AdduInstruction(),
            0x24: AndInstruction(),
            0x08: JRInstruction(),
            0X27: NorInstruction(),
            0x25: OrInstruction(),
            0X26: XorInstruction(),
            0x2a: SLTInstruction(),
            0x2b: SLTUInstruction(),
            0x00: SLLInstruction(),
            0x02: SRLInstruction(),
            0x03: SRAInstruction(),
            0x22: SubInstruction(),
            0x23: SubuInstruction(),
            0x0c: SyscallInstruction(),
            0x0d: NopInstruction(),
            0x09: JalrInstruction(),
            0x18: MultInstruction(),
            0x1a: DivInstruction(),
            0x12: MFLOInstruction(),
            0X10: MFHIInstruction(),
        }
    def __call__(self, word):
        super().__call__(word)
        self.funct = ( ((1 << 6) - 1)  &  (self.word.data >> (0) ) )
        return self
    

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        """
        Receive the registers to be able to translate the register numbers by the name of the registers  # noqa: E501
        """
        return self.functions[self.funct](self.word).decode(registers, *args, **kwargs)  # noqa: E501

    def execute(self, registers: Registers, program_counter, memory: Memory, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        return self.functions[self.funct](self.word).execute(
            registers=registers,
            program_counter=program_counter,
            memory=memory,
            *args,
            **kwargs
        )
