from helpers.int2bin import Int2Bits
from minips.instruction.instructions.r_instructions import R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class MFHIInstruction(R_BaseFunction):
    instruction_name = "MFHI"
    funct_code = '010000'

    def __init__(self, word) -> None:
        super().__init__(word)

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
        hi_register = local_registers.get_hi()
        local_registers.set_register_value(self.rd_number, hi_register.get_data())
        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
