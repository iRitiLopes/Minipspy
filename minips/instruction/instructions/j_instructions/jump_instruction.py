from minips.memory import Memory
from minips.registers import Registers
from minips.instruction.instructions.j_instructions import J_BaseFunction
from helpers.bin2int import Bin2Int


class JumpInstruction(J_BaseFunction):
    instruction_name = "J"
    funct_code = '000010'

    def __init__(self, word) -> None:
        super().__init__(word)

    def decode(self, *args, **kwargs) -> str:
        jump_address = Bin2Int.convert(self.jump_address)
        return f"{self.instruction_name} {jump_address * 4}"

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        new_pc = (Bin2Int.convert(self.jump_address) * 4)

        branch_delayed_word = memory.load(program_counter + 4)
        branch_delayed_instruction = kwargs['instruction_factory'].factory(branch_delayed_word)
        delayed_registers, delayed_pc, delayed_memory, coproc = branch_delayed_instruction.execute(registers=registers, program_counter=program_counter + 4, memory=memory, *args, **kwargs)

        return delayed_registers, new_pc, delayed_memory, kwargs['coprocessor'].registers
