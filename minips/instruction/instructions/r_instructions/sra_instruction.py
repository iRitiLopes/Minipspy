from helpers.twocomplement import TwoComp
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.instruction.instructions.r_instructions import R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class SRAInstruction(R_BaseFunction):
    instruction_name = "SRA"
    funct_code = '000011'

    def __init__(self) -> None:
        super().__init__()
    
    def __call__(self, word) -> None:
        return super().__call__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rd_name = registers.get_register_name(self.rd_number)
        rt_name = registers.get_register_name(self.rt_number)

        return (f"{self.instruction_name} "
                f"{rd_name}, {rt_name}, {self.shamt_value}")

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        rt_register = local_registers.get_register(self.rt_number)

        s = self.shamt_value
        rt = rt_register.to_signed_int()
        bits = Int2Bits.convert(rt)
        rd_bits = bits[0]*self.shamt_value + bits[:32-self.shamt_value]
        rd = Bin2Int.convert(rd_bits, False)

        local_registers.set_register_value(self.rd_number, rd)
        return local_registers, program_counter + 4, memory, kwargs['coprocessor'].registers
