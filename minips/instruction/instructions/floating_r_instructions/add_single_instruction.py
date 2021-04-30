from helpers.float2int import Float2Int
from minips.coprocessor import COProcessor
from minips.instruction.instructions.floating_r_instructions import \
    Floating_R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class AddSingleInstruction(Floating_R_BaseFunction):
    instruction_name = "ADD.S"
    funct_code = '000000'
    fmt = '00000'

    def __init__(self, word) -> None:
        super().__init__(word)
        self.fmt = self.word.get_k_bits_from(5, 21)
        self.ft = self.word.get_k_bits_from(5, 16)
        self.fs = self.word.get_k_bits_from(5, 11)
        self.fd = self.word.get_k_bits_from(5, 6)

        self.ft_number = self.ft
        self.fs_number = self.fs
        self.fd_number = self.fd

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

        fd = fs_register.to_single_precision() + \
            ft_register.to_single_precision()
        fd = Float2Int.convert(fd)
        local_registers.set_register_value(self.fd_number, fd)
        return registers, program_counter + 4, memory, local_registers
