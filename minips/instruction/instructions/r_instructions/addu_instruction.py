from helpers.twocomplement import TwoComp
from helpers.int2bin import Int2Bits
from minips.instruction.instructions.r_instructions import R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers

class AdduInstruction(R_BaseFunction):
    instruction_name = "ADDU"
    funct_code = '100001'

    def __init__(self) -> None:
        super().__init__()
    
    def __call__(self, word) -> None:
        return super().__call__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rd_name = registers.get_register_name(self.rd_number)
        rs_name = registers.get_register_name(self.rs_number)
        rt_name = registers.get_register_name(self.rt_number)

        return f"{self.instruction_name} {rd_name}, {rs_name}, {rt_name}"

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        rs_register = local_registers.get_register(self.rs_number)
        rt_register = local_registers.get_register(self.rt_number)

        rd = rs_register.to_unsigned_int() + rt_register.to_unsigned_int()

        local_registers.set_register_value(self.rd_number, rd)
        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
