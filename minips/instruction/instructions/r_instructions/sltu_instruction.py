from helpers.int2bin import Int2Bits
from minips.instruction.instructions.r_instructions import R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class SLTUInstruction(R_BaseFunction):
    instruction_name = "SLTU"
    funct_code = '101011'

    def __init__(self, word) -> None:
        super().__init__(word)

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

        rd = rs_register.get_data_unsigned() < rt_register.get_data_unsigned()
        local_registers.set_register_value(self.rd_number, rd)
        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
