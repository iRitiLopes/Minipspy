from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.coprocessor import COProcessor
from minips.instruction.instructions.floating_r_instructions import \
    Floating_R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class MOVSingleInstruction(Floating_R_BaseFunction):
    instruction_name = "MOV.S"
    funct_code = '000110'
    fmt = ''

    def __call__(self, word) -> None:
        super().__call__(word)
        self.fmt = self.word.get_k_bits_from(5, 21)
        self.fs = self.word.get_k_bits_from(5, 11)
        self.fd = self.word.get_k_bits_from(5, 6)

        self.fs_number = self.fs
        self.fd_number = self.fd
        return self

    def decode(self, coprocessor: COProcessor, *args, **kwargs) -> str:
        fd_name = coprocessor.registers.get_register_name(self.fd_number)
        fs_name = coprocessor.registers.get_register_name(self.fs_number)

        return f"{self.instruction_name} {fd_name}, {fs_name}"

    def execute(self,
                registers,
                coprocessor: COProcessor,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = coprocessor.registers
        fs_register = local_registers.get_register(self.fs_number)
        local_registers.set_register_value(
            self.fd_number, fs_register.get_data()
        )
        return registers, program_counter + 4, memory, local_registers
