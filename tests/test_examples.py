from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import pytest

from minips import Minips


EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def run_example(name, mode):
    emulator = Minips(mode)
    emulator.load(str(EXAMPLES / name))
    output = StringIO()
    with redirect_stdout(output):
        # Bound execution so a cache regression cannot hang the test suite.
        for count, instruction in enumerate(emulator.read_instructions()):
            assert count < 100000, "Example exceeded instruction limit"
            (emulator.registers, emulator.program_counter, emulator.memory,
             emulator.coprocessor.registers) = instruction.execute(
                registers=emulator.registers,
                program_counter=emulator.program_counter,
                memory=emulator.memory, coprocessor=emulator.coprocessor,
                instruction_factory=emulator.factory, logger=emulator.log)
            if emulator.program_counter == -1:
                break
    assert emulator.program_counter == -1
    emulator.memory.flush()
    return output.getvalue(), {a: w.data for a, w in emulator.memory.mem_blocks.items()}


@pytest.mark.parametrize("name", [
    "01.soma", "02.hello", "04.branches", "07.loadstore", "08.sort",
    "09.contador", "10.hello++", "11.surpresinha", "12.branch_delay_slot",
    "13.arit",
])
@pytest.mark.parametrize("mode", range(2, 7))
def test_cache_matches_uncached_example(name, mode):
    assert run_example(name, mode) == run_example(name, 1)
