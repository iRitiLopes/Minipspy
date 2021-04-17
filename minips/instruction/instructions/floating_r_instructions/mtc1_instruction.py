from helpers.float2bin import Float2Bits
from helpers.bin2float import Bin2Float
from minips.registers import Registers
from minips.coprocessor import COProcessor
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.instruction.instructions.floating_r_instructions import \
    Floating_R_BaseFunction
from minips.memory import Memory


class MTC1Instruction(Floating_R_BaseFunction):
    instruction_name = "MTC1"
    funct_code = '00000000000'
    fmt = '00100'

    def __init__(self, word) -> None:
        super().__init__(word)
        self.fmt = self.word.get_bits_between(25, 21)
        self.rt = self.word.get_bits_between(20, 16)
        self.fs = self.word.get_bits_between(15, 11)

        self.rt_number = Bin2Int.convert(self.rt, False)
        self.fs_number = Bin2Int.convert(self.fs, False)

    def decode(self, registers: Registers, coprocessor: COProcessor, *args, **kwargs) -> str:
        fs_name = coprocessor.registers.get_register_name(self.fs_number)
        rt_name = registers.get_register_name(self.rt_number)

        return f"{self.instruction_name} {rt_name}, {fs_name}"

    def execute(self,
                registers: Registers,
                coprocessor: COProcessor,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):

        local_registers = registers
        local_co_registers = coprocessor.registers

        rt_register = local_registers.get_register(self.rt_number)
        rt_bin = rt_register.get_data()

        local_co_registers.set_register_value(self.fs_number, rt_bin)
        return local_registers, program_counter + 4, memory, local_co_registers
