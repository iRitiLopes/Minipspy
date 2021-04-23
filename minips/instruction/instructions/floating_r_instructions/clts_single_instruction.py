from helpers.float2bin import Float2Bits
from minips.registers import Registers
from minips.coprocessor import COProcessor
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.instruction.instructions.floating_r_instructions import \
    Floating_R_BaseFunction
from minips.memory import Memory


class CLTSingleInstruction(Floating_R_BaseFunction):
    instruction_name = "C.LT.S"
    funct_code = '0010'
    fmt = '10000'

    def __init__(self, word) -> None:
        super().__init__(word)
        self.fmt = self.word.get_bits_between(25, 21)
        self.ft = self.word.get_bits_between(20, 16)
        self.fs = self.word.get_bits_between(15, 11)
        self.fd = self.word.get_bits_between(10, 6)

        self.ft_number = Bin2Int.convert(self.ft, False)
        self.fs_number = Bin2Int.convert(self.fs, False)
        self.fd_number = Bin2Int.convert(self.fd, False)

    def decode(self, coprocessor: COProcessor, *args, **kwargs) -> str:
        fd_name = coprocessor.registers.get_register_name(self.fd_number)
        fs_name = coprocessor.registers.get_register_name(self.fs_number)
        ft_name = coprocessor.registers.get_register_name(self.ft_number)

        return f"{self.instruction_name} {fd_name}, {fs_name}, {ft_name}"

    def execute(self,
                registers: Registers,
                coprocessor: COProcessor,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = coprocessor.registers
        fs_register = local_registers.get_register(self.fs_number)
        ft_register = local_registers.get_register(self.ft_number)

        if fs_register.to_single_precision() < ft_register.to_single_precision():
            cc = 1
        else:
            cc = 0

        cc_bin = Int2Bits.convert(cc)

        local_registers.set_register_value(32, cc_bin)
        return registers, program_counter + 4, memory, local_registers
