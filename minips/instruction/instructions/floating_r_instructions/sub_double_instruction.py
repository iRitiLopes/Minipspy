from helpers.bin2float import Bin2Float
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.coprocessor import COProcessor
from minips.instruction.instructions.floating_r_instructions import \
    Floating_R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers
from helpers.float2bin import Float2Bin


class SubDoubleInstruction(Floating_R_BaseFunction):
    instruction_name = "SUB.D"
    funct_code = '000001'
    fmt = '10001'

    def __call__(self, word) -> None:
        super().__call__(word)
        self.fmt = self.word.get_bits_between(25, 21)
        self.ft = self.word.get_bits_between(20, 16)
        self.fs = self.word.get_bits_between(15, 11)
        self.fd = self.word.get_bits_between(10, 6)

        self.ft_number = self.ft
        self.fs_number = self.fs
        self.fd_number = self.fd
        return self

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

        fs = Bin2Float.convert(Int2Bits.convert(fs1_register.to_signed_int()) + Int2Bits.convert(fs_register.to_signed_int()), True)
        ft = Bin2Float.convert(Int2Bits.convert(ft1_register.to_signed_int()) + Int2Bits.convert(ft_register.to_signed_int()), True)
        
        fd = fs - ft
        fd_bin = Float2Bin.convert(fd, doubled=True)
        fd_bin_higher = Bin2Int.convert(fd_bin[0:32])
        fd_bin_lower = Bin2Int.convert(fd_bin[32:64])

        local_registers.set_register_value(self.fd_number + 1, fd_bin_higher)
        local_registers.set_register_value(self.fd_number, fd_bin_lower)
        return registers, program_counter + 4, memory, local_registers
