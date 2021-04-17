from minips.registers import InvalidRegister, Register, Registers
import pytest


class TestRegisters:
    def test_get_all_valid_registers(self):
        registers = Registers()
        for x in range(32):
            register = registers.get_register(x)
            assert isinstance(register, Register)

    def test_all_registers_initialized_with_zero(self):
        registers = Registers()
        for x in range(32):
            register_value = registers.get_register_value(x)
            assert register_value == 0

    def test_get_invalid_register(self):
        registers = Registers()
        with pytest.raises(InvalidRegister):
            registers.get_register(-1)
            registers.registers(100)

    def test_modify_register_value(self):
        new_value = 42
        registers = Registers()
        #  register No 4 is register a0
        registers.set_register_value(4, new_value)
        assert new_value == registers.get_register_value(4)

    def test_register_name(self):
        register_name = "$a0"
        register_number = 4
        registers = Registers()

        assert register_name == registers.get_register_name(register_number)
