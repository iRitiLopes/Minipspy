from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.instruction.instructions.i_instructions import I_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class LuiInstruction(I_BaseFunction):
    instruction_name = "LUI"
    funct_code = '001111'

    def __init__(self, word) -> None:
        super().__init__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rt_name = registers.get_register_name(self.rt_number)
        immediate_value = Bin2Int.convert(self.imediate)

        return f"{self.instruction_name} {rt_name}, {immediate_value}"  # noqa: E501

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        immediate_value = self.imediate
        rt = immediate_value * 2**16
        local_registers.set_register_value(self.rt_number, rt)
        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
