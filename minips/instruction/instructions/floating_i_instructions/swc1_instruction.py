from helpers.bin2float import Bin2Float
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from helpers.int2hex import Int2Hex
from minips.coprocessor import COProcessor
from minips.instruction.instructions.floating_i_instructions import \
    Floating_I_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class SWC1Instruction(Floating_I_BaseFunction):
    instruction_name = "SWC1"
    funct_code = '111001'

    def __call__(self, word) -> None:
        return super().__call__(word)

    def decode(self, registers: Registers, coprocessor: COProcessor, *args, **kwargs) -> str:
        ft_name = coprocessor.registers.get_register_name(self.ft_number)
        rs_number = self.base
        rs_name = coprocessor.registers.get_register_name(rs_number)
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
        local_memory = memory

        ft_register = local_co_registers.get_register(self.ft_number)
        ft_bin = ft_register.get_data()

        rs_number = self.base
        rs_register = local_registers.get_register(rs_number)
        
        address = rs_register.get_data_unsigned()
        offset = self.offset

        local_memory.store(address + offset, ft_bin)
        kwargs['logger'].trace(f"W {hex(program_counter)} (line# {hex(address + offset)})")
        return local_registers, program_counter + 4, local_memory, local_co_registers
