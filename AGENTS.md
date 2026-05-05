# AGENTS.md

## Project overview

Mini MIPS emulator (education project, UFABC 2021). Single-package Python 3.9 project managed with pipenv.

## Setup & commands

```bash
pipenv install --dev    # install all deps including dev tools
pip install -e .        # install minipspy CLI globally
```

- **Run a single test**: `pipenv run pytest tests/test_word.py -v`
- **Run all tests**: `pipenv run pytest tests/ -v`
- **Lint**: `pipenv run flake8 minips/`
- **Format**: `pipenv run autopep8 -r minips/`

The CLI entry point is `minipspy` (defined in `setup.py` → `main.py:run`).

## Architecture

```
main.py               → CLI dispatch (decode|run|trace|debug)
minips/__init__.py    → Minips class: loads program, drives execution loop
minips/memory.py      → Memory with integrated cache logic (modes 1-6)
minips/cache/         → L1/L2 cache implementations
minips/instruction/   → Instruction factory + R/I/J/FR/FI instruction types
minips/registers.py   → 32 GP registers + HI/LO
minips/coprocessor/   → Floating-point coprocessor registers
minips/word.py        → 32-bit Word abstraction (data field is int, not string)
helpers/              → Binary conversion utilities
examples/             → MIPS test programs (.asm source, .data/.text/.rodata binaries)
tests/                → pytest tests
test.py               → Standalone profiling script (not pytest)
```

## Key conventions & gotchas

- **`Word.data` is an integer**, never a string. A performance refactor replaced all string-based bit handling with integer bitmasks. Do not treat data as a binary string.
- **`Word.is_empty()` checks `data is None`**, but the default constructor sets `data=0`. A fresh `Word()` is NOT empty — it holds the value 0. Empty words are created via `Word(data=None)`.
- **`Memory.__init__(mem_mode, log)` requires two arguments.** The test files pass no args (`Memory()`) which is stale and would fail against current code.
- **Memory modes**: 1=no cache, 2=unified L1 random, 3=split L1, 4=split L1 LRU, 5=split L1 N-way, 6=split L1+L2 N-way. Mode 2 is the most tested.
- **`memory_controller.py`** is a dead/experimental file not wired into the main execution path. The real memory logic lives in `memory.py`.
- **Example programs** consist of `.text` (code), `.data` (data section), and `.rodata` (read-only data) binary files. The `.asm` files are source for reference. `.rodata` is optional — load silently skips missing files.
- **Program counter** value `-1` signals execution termination (syscall exit).
- **logger** writes to `./minips.trace` when trace/debug mode is active. This file is gitignored.
- **Register zero** writes are silently ignored (hardwired to 0).
- **Tests may be stale** — the test suite has not been maintained through refactors. Run with caution.
