from minips.instruction.instructions.r_instructions import R_BaseFunction
from minips.memory import Memory
from minips.registers import Registers
from helpers.int2bin import Int2Bits
from helpers.int2hex import Int2Hex

class JalrInstruction(R_BaseFunction):
    instruction_name = "JALR"
    funct_code = "001001"

    def __init__(self, word) -> None:
        super().__init__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rs_name = registers.get_register_name(self.rs_number)
        rd_name = registers.get_register_name(self.rd_number)
        return f"{self.instruction_name} {rs_name} {rd_name}"

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        rs_register = registers.get_register(self.rs_number)
        local_registers = registers
        local_registers.set_register_value(self.rd_number, Int2Bits.convert(program_counter + 8))
        new_pc = rs_register.to_unsigned_int()

        branch_delayed_word = memory.load(program_counter + 4)
        kwargs['logger'].trace(f"I {Int2Hex.convert(program_counter)} (line# {Int2Hex.convert(program_counter + 4)})")
        branch_delayed_instruction = kwargs['instruction_factory'].factory(branch_delayed_word)
        delayed_registers, delayed_pc, delayed_memory, coproc = branch_delayed_instruction.execute(registers=local_registers, program_counter=program_counter + 4, memory=memory, *args, **kwargs)

        return delayed_registers, new_pc, delayed_memory, kwargs['coprocessor'].registers
