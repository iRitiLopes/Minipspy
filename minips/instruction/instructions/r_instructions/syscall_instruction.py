from helpers.float2bin import Float2Bin
from helpers.int2float import Int2Float
from helpers.float2int import Float2Int
from helpers.int2hex import Int2Hex
from helpers.bin2int import Bin2Int
from helpers.bin2float import Bin2Float
from minips.coprocessor import COProcessor
from helpers.bin2chr import Bin2Chr
from helpers.int2bin import Int2Bits
from minips.instruction.instructions.r_instructions import R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class SyscallInstruction(R_BaseFunction):
    instruction_name = "SYSCALL"
    funct_code = '001100'

    def __init__(self) -> None:
        super().__init__()
        self.v0 = 2
        self.a0 = 4
        self.f0 = 0
        self.f1 = 1
        self.f12 = 12
        self.f13 = 13
    
    def __call__(self, word) -> None:
        return super().__call__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        return "SYSCALL"

    def execute(self,
                registers: Registers,
                coprocessor: COProcessor,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        local_co_registers = coprocessor.registers
        new_pc = program_counter
        new_memory = memory

        v0_register = local_registers.get_register(self.v0)
        v0_value = v0_register.get_data()

        a0_register = local_registers.get_register(self.a0)

        f12_register = local_co_registers.get_register(self.f12)
        f13_register = local_co_registers.get_register(self.f13)

        if v0_value == 1:
            print(a0_register.get_data(), end='')
        elif v0_value == 2:
            print(f12_register.to_single_precision(), end='')
        elif v0_value == 3:
            f13_b = Int2Bits.convert(f13_register.get_data())
            f12_b = Int2Bits.convert(f12_register.get_data())
            f = f13_b + f12_b
            print(Bin2Float.convert(f, True), end='')
        elif v0_value == 4:
            a0_address = a0_register.get_data()
            string = self.__read_string(a0_address, memory=memory, pc=program_counter, logger=kwargs['logger'])
            print(string, end='')

        elif v0_value == 5:
            read = int(input())
            local_registers.set_register_value(self.v0, read)
        elif v0_value == 6:
            read = float(input())
            read_bit = Float2Int.convert(read)
            local_co_registers.set_register_value(self.f0, read_bit)
        elif v0_value == 7:
            read = float(input())
            read_bit = Float2Bin.convert(read, True)
            read_bit_high = Bin2Int.convert(read_bit[0:32])
            read_bit_low = Bin2Int.convert(read_bit[32:64])

            local_co_registers.set_register_value(self.f1, read_bit_high)
            local_co_registers.set_register_value(self.f0, read_bit_low)

        elif v0_value == 10:
            return local_registers, -1, new_memory, local_co_registers
        elif v0_value == 11:
            print(Bin2Chr.convert(Int2Bits.convert(a0_register.get_data())), end='')

        return local_registers, new_pc + 4, new_memory, local_co_registers

    def __read_string(self, address, memory: Memory, pc, logger):
        string = ""
        if address % 4 != 0:
            relative = address % 4
            relative_address = address - relative
            
            word = memory.load(relative_address)
            word = Int2Bits.convert(word.data)

            word_relative_data = word[:-8*relative]
            for x in range(len(word_relative_data), 0, -8):
                char = Bin2Chr.convert(word_relative_data[x-8:x])
                string += char
            address = relative_address + 4
        word = memory.load(address=address)
        d = Int2Bits.convert(word.data)
        while True:
            for x in range(len(d), 0, -8):
                char = Bin2Chr.convert(d[x-8:x])
                if char == '\0':
                    return string
                else:
                    string += char
            if address % 4 == 0:
                address = address + 4
            else:
                address = address + (4 - (address % 4))
            word = memory.load(address=address)
            d = Int2Bits.convert(word.data)
