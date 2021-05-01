from helpers.int2bin import Int2Bits
from minips.instruction.instructions.r_instructions import R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class MFLOInstruction(R_BaseFunction):
    instruction_name = "MFLO"
    funct_code = '010010'

    def __init__(self) -> None:
        super().__init__()
    
    def __call__(self, word) -> None:
        return super().__call__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rd_name = registers.get_register_name(self.rd_number)

        return f"{self.instruction_name} {rd_name}"

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        lo_register = local_registers.get_lo()
        local_registers.set_register_value(self.rd_number, lo_register.to_signed_int())
        
        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
