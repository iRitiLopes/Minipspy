from helpers.bin2float import Bin2Float
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.coprocessor import COProcessor
from minips.instruction.instructions.floating_r_instructions import \
    Floating_R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class CVTSDoubleInstruction(Floating_R_BaseFunction):
    instruction_name = "CVT.S.D"
    funct_code = '100000'
    fmt = '10001'

    def __init__(self, word) -> None:
        super().__init__(word)
        self.fmt = self.word.get_bits_between(25, 21)
        self.fs = self.word.get_bits_between(15, 11)
        self.fd = self.word.get_bits_between(10, 6)

        self.fs_number = Bin2Int.convert(self.fs)
        self.fd_number = Bin2Int.convert(self.fd)

    def decode(self, coprocessor: COProcessor, *args, **kwargs) -> str:
        fd_name = coprocessor.registers.get_register_name(self.fd_number)
        fs_name = coprocessor.registers.get_register_name(self.fs_number)

        return f"{self.instruction_name} {fd_name}, {fs_name}"

    def execute(self,
                registers: Registers,
                coprocessor: COProcessor,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = coprocessor.registers
        fs_register = local_registers.get_register(self.fs_number)
        fs1_register = local_registers.get_register(self.fs_number + 1)
        fs_bits = fs1_register.get_data() + fs_register.get_data()

        fs = Bin2Float.convert(fs_bits, doubled=True)
        fs_bits = Float2Bits.convert(fs)

        local_registers.set_register_value(self.fd_number, fs_bits)
        return registers, program_counter + 4, memory, local_registers
