from helpers.twocomplement import TwoComp
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.instruction.instructions.i_instructions import I_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class OriInstruction(I_BaseFunction):
    instruction_name = "ORI"
    funct_code = '001101'

    def __call__(self, word):
        return super().__call__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rs_name = registers.get_register_name(self.rs_number)
        rt_name = registers.get_register_name(self.rt_number)
        immediate_value = ( ((1 << 16) - 1)  &  (self.word.data >> (0) ) )
        return f"{self.instruction_name} {rt_name}, {rs_name}, {immediate_value}"  # noqa: E501

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        rs_register = local_registers.get_register(self.rs_number)
        immediate_value = ( ((1 << 16) - 1)  &  (self.word.data >> (0) ) )

        rt_value = rs_register.to_unsigned_int() | immediate_value

        local_registers.set_register_value(self.rt_number, rt_value)
        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
