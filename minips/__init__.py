from minips.word import Word
from helpers.int2hex import Int2Hex
from helpers.bin2int import Bin2Int
from minips.statistics import Mipstatics
from helpers.int2bin import Int2Bits
from helpers.databyte2bin import DataByte2Bits
from helpers.byte2bin import Byte2Bits
import os
from minips.memory import Memory
from minips.registers import Registers
from minips.coprocessor import COProcessor
from minips.instruction.factory import InstructionFactory
from helpers.log import Log


class Minips:
    def __init__(self, mem_mode) -> None:
        self.log = Log()
        self.memory = Memory(mem_mode=mem_mode, log=self.log)
        self.registers = Registers()
        self.coprocessor = COProcessor()
        self.registers.registers[0].value = Word(0x0)
        self.registers.set_register_value(
            28,
            self.memory.GLOBAL_POINTER
        )
        self.registers.set_register_value(
            29,
            self.memory.STACK_POINTER
        )
        self.program_counter = self.memory.TEXT_SECTION_START
        self.statistics = Mipstatics()
        self.factory = InstructionFactory()

    def get_memory(self) -> Memory:
        return self.memory

    def get_registers(self) -> Registers:
        return self.registers

    def get_program_counter(self):
        return self.program_counter

    def load(self, path):
        self.load_program(f"{path}.text")
        self.load_data(f"{path}.data")
        self.load_data_rodata(f"{path}.rodata")

    def load_program(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found!")
        with open(path, 'rb') as f:
            mem_address = self.memory.TEXT_SECTION_START
            while (byte := f.read(4)):
                self.memory.init_store(mem_address, Byte2Bits.convert(byte))
                mem_address = mem_address + 4

    def load_data(self, path):
        if not os.path.exists(path):
            return
        with open(path, 'rb') as f:
            mem_address = self.memory.DATA_SECTION_START
            while (byte := f.read(4)):
                self.memory.init_store(mem_address, DataByte2Bits.convert(byte))
                mem_address = mem_address + 4

    def load_data_rodata(self, path):
        if not os.path.exists(path):
            return
        with open(path, 'rb') as f:
            mem_address = self.memory.RODATA_SECION_START
            while (byte := f.read(4)):
                self.memory.init_store(mem_address, DataByte2Bits.convert(byte))
                mem_address = mem_address + 4

    def decode(self):
        for instruction in self.read_instructions():
            decoded_instruction = instruction.decode(self.registers, coprocessor=self.coprocessor)
            print(hex(self.program_counter), "\t", hex(instruction.word.data), "\t\t",  decoded_instruction)
            self.program_counter += 4

    def execute(self):
        self.statistics.start()
        for instruction in self.read_instructions():
            #decoded_instruction = instruction.decode(self.registers, coprocessor=self.coprocessor)
            #print(hex(self.program_counter), "\t", hex(instruction.word.data), "\t\t",  decoded_instruction)
            self.registers, self.program_counter, self.memory, self.coprocessor.registers = instruction\
                .execute(
                    registers=self.registers,
                    program_counter=self.program_counter,
                    memory=self.memory,
                    coprocessor=self.coprocessor,
                    instruction_factory=self.factory,
                    logger=self.log
                )
            self.statistics.increase_statistic(instruction)
            if self.program_counter == -1:
                self.statistics.memory_statistics(self.memory)
                self.statistics.finish()
                self.statistics.show_statistics()
                return
    def trace_mode(self):
        self.log = Log('trace')
        self.execute()
    
    def debug_mode(self):
        self.log = Log('debug')
        self.execute()

    def read_instructions(self):
        actual_word = self.memory.load(self.program_counter)
        while not actual_word.is_empty():
            instruction = self.factory.factory(actual_word)
            yield instruction
            actual_word = self.memory.load(self.program_counter)
