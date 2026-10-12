"""CPU and input behavior needed by the uncompiled C++ MD5 example."""
import pytest

from minips import Minips
from minips.word import Word


def execute(emulator, word):
    emulator.factory.factory(Word(word)).execute(
        registers=emulator.registers, program_counter=0x00400000,
        memory=emulator.memory, coprocessor=emulator.coprocessor,
        instruction_factory=emulator.factory, logger=emulator.log)


def read_character(emulator):
    emulator.registers.set_register_value(2, 12)
    execute(emulator, 0x0000000c)
    return emulator.registers.get_register(2).get_data()


@pytest.mark.parametrize('line', ['', 'abc def', 'ação'])
def test_read_character_returns_utf8_bytes_and_enter(monkeypatch, line):
    lines = iter([line, 'next'])
    monkeypatch.setattr('builtins.input', lambda: next(lines))
    emulator = Minips(1)
    for byte in (line + '\n').encode('utf-8'):
        assert read_character(emulator) == byte
    assert read_character(emulator) == ord('n')


def test_read_character_returns_minus_one_at_eof(monkeypatch):
    def eof():
        raise EOFError
    monkeypatch.setattr('builtins.input', eof)
    assert read_character(Minips(1)) == -1


def test_read_character_buffer_is_not_shared(monkeypatch):
    lines = iter(['abc', 'xyz'])
    monkeypatch.setattr('builtins.input', lambda: next(lines))
    first, second = Minips(1), Minips(1)
    assert read_character(first) == ord('a')
    assert read_character(second) == ord('x')
    assert read_character(first) == ord('b')


def test_srl_zero_fills_sign_bit():
    emulator = Minips(1)
    emulator.registers.set_register_value(9, 0x80000001)
    execute(emulator, (9 << 16) | (8 << 11) | (1 << 6) | 0x02)
    assert emulator.registers.get_register(8).get_data_unsigned() == 0x40000000


def test_nor_produces_integer_bits():
    emulator = Minips(1)
    emulator.registers.set_register_value(9, 0x12345678)
    execute(emulator, (9 << 21) | (8 << 11) | 0x27)
    value = emulator.registers.get_register_value(8).data
    assert isinstance(value, int)
    assert value == 0xedcba987


@pytest.mark.parametrize('left,right,expected', [
    (0xffffffff, 1, 0), (0x80000000, 0x80000000, 0),
    (0x7fffffff, 1, 0x80000000),
])
def test_addu_wraps_at_32_bits(left, right, expected):
    emulator = Minips(1)
    emulator.registers.set_register_value(9, left)
    emulator.registers.set_register_value(10, right)
    execute(emulator, (9 << 21) | (10 << 16) | (8 << 11) | 0x21)
    assert emulator.registers.get_register_value(8).data == expected


@pytest.mark.parametrize('value,immediate,expected', [
    (9, 10, 1), (10, 10, 0), (0x80000000, 1, 0),
    (0xfffffffe, -1, 1), (0xffffffff, -1, 0),
])
def test_sltiu_unsigned_comparison_and_sign_extension(value, immediate, expected):
    emulator = Minips(1)
    emulator.registers.set_register_value(9, value)
    execute(emulator, (0xb << 26) | (9 << 21) | (8 << 16) | (immediate & 0xffff))
    assert emulator.registers.get_register(8).get_data() == expected
