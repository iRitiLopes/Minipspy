from helpers.int2bin import Int2Bits
from minips.instruction.instructions.r_instructions import R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class DivInstruction(R_BaseFunction):
    instruction_name = "DIV"
    funct_code = '011010'

    def __init__(self, word) -> None:
        super().__init__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rs_name = registers.get_register_name(self.rs_number)
        rt_name = registers.get_register_name(self.rt_number)

        return f"{self.instruction_name} {rs_name}, {rt_name}"

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        rs_register = local_registers.get_register(self.rs_number)
        rt_register = local_registers.get_register(self.rt_number)

        result_lo = rs_register.to_signed_int() // rt_register.to_signed_int()
        result_hi = rs_register.to_signed_int() % rt_register.to_signed_int()
        lo = Int2Bits.convert(result_lo)
        hi = Int2Bits.convert(result_hi)

        local_registers.set_hi_value(hi)
        local_registers.set_lo_value(lo)
        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
