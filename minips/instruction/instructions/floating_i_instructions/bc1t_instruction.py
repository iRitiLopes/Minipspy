from atexit import register
from minips.word import Word
from helpers.int2hex import Int2Hex
from helpers.bin2float import Bin2Float
from helpers.bin2int import Bin2Int
from helpers.int2bin import Int2Bits
from minips.coprocessor import COProcessor
from minips.instruction.instructions.floating_i_instructions import \
    Floating_I_BaseFunction
from minips.memory import Memory
from minips.registers import Registers


class BC1TInstruction(Floating_I_BaseFunction):
    instruction_name = "BC1"
    funct_code = '01000'

    def __call__(self, word: Word) -> None:
        self.ft = word.get_k_bits_from(1,16)
        self.instruction_name = self.instruction_name + 'T' if int(self.ft) == 1 else self.instruction_name + 'F'
        super().__call__(word)
        return self

    def decode(self, registers: Registers, coprocessor: COProcessor, *args, **kwargs) -> str:
        offset = self.offset

        return f"{self.instruction_name} {offset}"

    def execute(self,
                registers: Registers,
                coprocessor: COProcessor,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_co_registers = coprocessor.registers
        local_registers = registers
        local_memory = memory

        offset = self.offset
        cc_register = local_co_registers.get_cc()
        cc_value = cc_register.to_unsigned_int()
        new_pc = program_counter
        if cc_value == int(self.ft):
            new_pc = new_pc + offset * 4
            branch_delayed_word = memory.load(program_counter + 4)
            kwargs['logger'].trace(f"I {Int2Hex.convert(program_counter)} (line# {Int2Hex.convert(program_counter + 4)})")
            branch_delayed_instruction = kwargs['instruction_factory'].factory(branch_delayed_word)
            delayed_registers, delayed_pc, delayed_memory, coproc = branch_delayed_instruction.execute(registers=local_registers, program_counter=program_counter + 4, memory=memory, coprocessor=coprocessor, *args, **kwargs)
            local_registers = delayed_registers
            local_co_registers = coproc
            local_memory = delayed_memory

        return local_registers, new_pc + 4, local_memory, local_co_registers