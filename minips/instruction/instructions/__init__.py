from minips.memory import Memory
from typing import Tuple
from minips.registers import Registers
from minips.word import Word


class BaseInstruction(object):
    instruction_type = None

    def __init__(self, word: Word) -> None:
        pass

    def get_type(self):
        return self.instruction_type

    def decode(self, *args, **kwargs):
        pass

    def execute(self, registers: Registers, *args, **kwargs) -> Tuple[Registers, int, Memory]:  # noqa: E501
        pass
