from minips.instruction.instructions.i_instructions.slti_instruction import SLTIInstruction


class SLTIUInstruction(SLTIInstruction):
    instruction_name = 'SLTIU'
    funct_code = '001011'

    def execute(self, registers, program_counter, memory, *args, **kwargs):
        # The immediate is sign-extended first, then compared as unsigned.
        value = registers.get_register(self.rs_number).get_data_unsigned()
        registers.set_register_value(
            self.rt_number, int(value < (self.imediate & 0xffffffff)))
        return registers, program_counter + 4, memory, kwargs['coprocessor'].registers
