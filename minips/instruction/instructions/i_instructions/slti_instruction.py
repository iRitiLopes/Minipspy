from helpers.twocomplement import TwoComp
from minips.instruction.instructions.r_instructions import R_BaseFunction
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.memory import Memory
from minips.registers import Registers
from minips.instruction.instructions.i_instructions import I_BaseFunction


class SLTIInstruction(I_BaseFunction):
    instruction_name = "SLTI"
    funct_code = '001010'

    def __call__(self, word):
        return super().__call__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        immediate_value = self.imediate
        rs_name = registers.get_register_name(self.rs_number)
        rt_name = registers.get_register_name(self.rt_number)

        return f"{self.instruction_name} {rt_name}, {rs_name}, {immediate_value}"

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        rs_register = local_registers.get_register(self.rs_number)
        immediate_value =  self.imediate

        rt = rs_register.get_data() < immediate_value
        local_registers.set_register_value(self.rt_number, rt)
        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
