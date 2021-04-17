from helpers.bin2int import Bin2Int
from minips.instruction.instructions.i_instructions import I_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class LBInstruction(I_BaseFunction):
    instruction_name = "LB"
    funct_code = '100000'

    def __init__(self, word) -> None:
        super().__init__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rt_name = registers.get_register_name(self.rt_number)
        rs_name = registers.get_register_name(self.rs_number)
        immediate_value = Bin2Int.convert(self.imediate)

        return f"{self.instruction_name} {rt_name}, {immediate_value}({rs_name})"  # noqa: E501

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        immediate_value = Bin2Int.convert(self.imediate)
        rs_register = local_registers.get_register(self.rs_number)
        rs_address = rs_register.to_unsigned_int()

        word = memory.load(rs_address + immediate_value).data[24:32].zfill(32)
        local_registers.set_register_value(self.rt_number, word)

        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
