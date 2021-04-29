from helpers.twocomplement import TwoComp
from helpers.int2hex import Int2Hex
from helpers.bin2int import Bin2Int
from minips.instruction.instructions.i_instructions import I_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class BNEInstruction(I_BaseFunction):
    instruction_name = "BNE"
    funct_code = '000101'

    def __init__(self, word) -> None:
        super().__init__(word)

    def decode(self, registers: Registers, *args, **kwargs) -> str:
        rs_name = registers.get_register_name(self.rs_number)
        rt_name = registers.get_register_name(self.rt_number)
        immediate_value = self.imediate

        return f"{self.instruction_name} {rt_name}, {rs_name}, {immediate_value}"  # noqa: E501

    def execute(self,
                registers: Registers,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_registers = registers
        local_memory = memory
        rs_register = local_registers.get_register(self.rs_number)
        rt_register = local_registers.get_register(self.rt_number)
        immediate_value = TwoComp.negate(self.imediate)

        new_pc = program_counter
        if rs_register.get_data() != rt_register.get_data():
            new_pc = new_pc + immediate_value * 4

            branch_delayed_word = memory.load(program_counter + 4)
            kwargs['logger'].trace(f"I {Int2Hex.convert(program_counter)} (line# {Int2Hex.convert(program_counter + 4)})")
            branch_delayed_instruction = kwargs['instruction_factory'].factory(branch_delayed_word)
            delayed_registers, delayed_pc, delayed_memory, coproc = branch_delayed_instruction.execute(registers=local_registers, program_counter=program_counter + 4, memory=memory, *args, **kwargs)
            local_registers = delayed_registers
            local_memory = delayed_memory

        return local_registers, new_pc + 4, local_memory, kwargs['coprocessor'].registers
