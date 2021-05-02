from helpers.twocomplement import TwoComp
from helpers.int2hex import Int2Hex
from helpers.bin2int import Bin2Int
from minips.instruction.instructions.i_instructions import I_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class LHUInstruction(I_BaseFunction):
    instruction_name = "LHU"
    funct_code = '100101'

    def __call__(self, word):
        return super().__call__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rt_name = registers.get_register_name(self.rt_number)
        rs_name = registers.get_register_name(self.rs_number)
        immediate_value = self.imediate

        return f"{self.instruction_name} {rt_name}, {immediate_value}({rs_name})"  # noqa: E501

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        immediate_value = self.imediate
        rs_register = local_registers.get_register(self.rs_number)
        rs_address = rs_register.to_unsigned_int()

        word = memory.load(rs_address + immediate_value * 4)
        word = ( ((1 << 16) - 1)  &  (word >> (0) ) )
        word = TwoComp.unsigned(word, 16)
        kwargs['logger'].trace(f"R {Int2Hex.convert(program_counter)} (line# {Int2Hex.convert(rs_address + immediate_value)})")
        local_registers.set_register_value(self.rt_number, word)

        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
