from helpers.int2hex import Int2Hex
from helpers.bin2float import Bin2Float
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.coprocessor import COProcessor
from minips.instruction.instructions.floating_i_instructions import \
    Floating_I_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class LWC1Instruction(Floating_I_BaseFunction):
    instruction_name = "LWC1"
    funct_code = '110001'

    def __call__(self, word) -> None:
        return super().__call__(word)

    def decode(self, registers: Registers, coprocessor: COProcessor, *args, **kwargs) -> str:
        ft_name = coprocessor.registers.get_register_name(self.ft_number)
        rs_number = self.base
        rs_name = registers.get_register_name(rs_number)
        offset = self.offset

        return f"{self.instruction_name} {ft_name}, {offset}({rs_name})"

    def execute(self,
                registers: Registers,
                coprocessor: COProcessor,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_co_registers = coprocessor.registers
        local_registers = registers

        rs_number = self.base
        rs_register = local_registers.get_register(rs_number)
        rs_address = rs_register.get_data_unsigned()
        offset = self.offset

        word = memory.load(rs_address + offset).data
        kwargs['logger'].trace(f"R {hex(program_counter)} (line# {hex(rs_address + offset)})")
        local_co_registers.set_register_value(self.ft_number, word)
        return local_registers, program_counter + 4, memory, local_co_registers
