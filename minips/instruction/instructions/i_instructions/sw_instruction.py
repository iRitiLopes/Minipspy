from helpers.int2hex import Int2Hex
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.instruction.instructions.i_instructions import I_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class SWInstruction(I_BaseFunction):
    instruction_name = "SW"
    funct_code = '101011'

    def __call__(self, word):
        return super().__call__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rt_name = registers.get_register_name(self.rt_number)
        rs_name = registers.get_register_name(self.rs_number)

        return f"{self.instruction_name} {rt_name}, {self.imediate}({rs_name})"  # noqa: E501

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        local_memory = memory

        offset_mem = self.imediate
        rs_register = local_registers.get_register(self.rs_number)
        rs_address = rs_register.get_data()

        rt_register = local_registers.get_register(self.rt_number)
        rt_value = rt_register.get_data()

        local_memory.store(rs_address + offset_mem, rt_value)
        kwargs['logger'].trace(f"W {Int2Hex.convert(program_counter)} (line# {Int2Hex.convert(rs_address + offset_mem)})")
        return local_registers, program_counter + 4, local_memory, kwargs['coprocessor'].registers
