from helpers.int2hex import Int2Hex
from helpers.int2bin import Int2Bits
from minips.memory import Memory
from minips.registers import Registers
from minips.instruction.instructions.j_instructions import J_BaseFunction
from helpers.bin2int import Bin2Int


class JumpalInstruction(J_BaseFunction):
    instruction_name = "JAL"
    funct_code = '000011'

    def __init__(self, word) -> None:
        super().__init__(word)

    def decode(self, *args, **kwargs) -> str:
        jump_address = self.jump_address
        return f"{self.instruction_name} {jump_address * 4}"

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        new_pc_address = (self.jump_address * 4)
        local_registers = registers
        ra_bits = program_counter + 8
        local_registers.set_register_value(31, ra_bits)

        branch_delayed_word = memory.load(program_counter + 4)
        kwargs['logger'].trace(f"I {Int2Hex.convert(program_counter)} (line# {Int2Hex.convert(program_counter + 4)})")
        branch_delayed_instruction = kwargs['instruction_factory'].factory(branch_delayed_word)
        delayed_registers, delayed_pc, delayed_memory, coproc = branch_delayed_instruction.execute(registers=local_registers, program_counter=program_counter + 4, memory=memory, *args, **kwargs)

        return delayed_registers, new_pc_address, delayed_memory, kwargs['coprocessor'].registers
