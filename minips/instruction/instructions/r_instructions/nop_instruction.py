from minips.instruction.instructions.r_instructions import R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class NopInstruction(R_BaseFunction):
    instruction_name = "nop"
    funct_code = '001101'

    def __init__(self) -> None:
        super().__init__()
    
    def __call__(self, word) -> None:
        return super().__call__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        return "nop"

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):

        return registers, program_counter + 4, memory, kwargs['coprocessor'].registers
