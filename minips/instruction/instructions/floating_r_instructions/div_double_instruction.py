from helpers.bin2float import Bin2Float
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.coprocessor import COProcessor
from minips.instruction.instructions.floating_r_instructions import \
    Floating_R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class DivDoubleInstruction(Floating_R_BaseFunction):
    instruction_name = "DIV.D"
    funct_code = '000011'
    fmt = '10001'

    def __init__(self, word) -> None:
        super().__init__(word)
        self.fmt = self.word.get_bits_between(25, 21)
        self.ft = self.word.get_bits_between(20, 16)
        self.fs = self.word.get_bits_between(15, 11)
        self.fd = self.word.get_bits_between(10, 6)

        self.ft_number = Bin2Int.convert(self.ft)
        self.fs_number = Bin2Int.convert(self.fs)
        self.fd_number = Bin2Int.convert(self.fd)

    def decode(self, coprocessor: COProcessor, *args, **kwargs) -> str:
        fd_name = coprocessor.registers.get_register_name(self.fd_number)
        fs_name = coprocessor.registers.get_register_name(self.fs_number)
        ft_name = coprocessor.registers.get_register_name(self.ft_number)

        return f"{self.instruction_name} {fd_name}, {fs_name}, {ft_name}"

    def execute(self,
                registers,
                coprocessor: COProcessor,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = coprocessor.registers
        fs_register = local_registers.get_register(self.fs_number)
        fs1_register = local_registers.get_register(self.fs_number + 1)

        ft_register = local_registers.get_register(self.ft_number)
        ft1_register = local_registers.get_register(self.ft_number + 1)

        fs = Bin2Float.convert(fs1_register.get_data() +
                               fs_register.get_data(), True)
        ft = Bin2Float.convert(ft1_register.get_data() +
                               ft_register.get_data(), True)

        fd = fs / ft
        fd_bin = Float2Bits.convert(fd, doubled=True)
        fd_bin_higher = fd_bin[0:32]
        fd_bin_lower = fd_bin[32:64]

        local_registers.set_register_value(self.fd_number + 1, fd_bin_higher)
        local_registers.set_register_value(self.fd_number, fd_bin_lower)
        return registers, program_counter + 4, memory, local_registers
