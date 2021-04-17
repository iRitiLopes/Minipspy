from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.instruction.instructions.i_instructions import I_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class AddiInstruction(I_BaseFunction):
    instruction_name = "ADDI"
    funct_code = '001000'

    def __init__(self, word) -> None:
        super().__init__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rs_name = registers.get_register_name(self.rs_number)
        rt_name = registers.get_register_name(self.rt_number)
        immediate_value = Bin2Int.convert(self.imediate, signed=True)

        return f"{self.instruction_name} {rt_name}, {rs_name}, {immediate_value}"  # noqa: E501

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        rs_register = local_registers.get_register(self.rs_number)
        immediate_value = Bin2Int.convert(self.imediate, signed=True)

        rt_value = rs_register.to_signed_int() + immediate_value
        rt_bits = Int2Bits.convert(rt_value)

        local_registers.set_register_value(self.rt_number, rt_bits)
        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
