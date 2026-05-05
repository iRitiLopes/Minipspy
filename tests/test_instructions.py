import pytest
from minips.word import Word
from minips.registers import Registers
from minips.memory import Memory
from minips.coprocessor import COProcessor
from minips.instruction.factory import InstructionFactory
from helpers.log import Log
from helpers.float2int import Float2Int


TEXT_START = 0x00400000


def _r_word(rs, rt, rd, shamt, funct):
    return (0x00 << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (shamt << 6) | funct


def _i_word(opcode, rs, rt, imm):
    return (opcode << 26) | (rs << 21) | (rt << 16) | (imm & 0xFFFF)


def _j_word(opcode, addr):
    return (opcode << 26) | (addr & 0x3FFFFFF)


def _fr_word(opcode, fmt, ft, fs, fd, funct):
    return (opcode << 26) | (fmt << 21) | (ft << 16) | (fs << 11) | (fd << 6) | funct


def _fi_word(opcode, base, ft, offset):
    return (opcode << 26) | (base << 21) | (ft << 16) | (offset & 0xFFFF)


class TestInstructions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.log = Log()
        self.memory = Memory(mem_mode=1, log=self.log)
        self.registers = Registers()
        self.coprocessor = COProcessor()
        self.factory = InstructionFactory()
        self.kwargs = {
            'coprocessor': self.coprocessor,
            'instruction_factory': self.factory,
            'logger': self.log,
        }
        self.memory.init_store(TEXT_START + 4, 0x00000000)
        self.pc = TEXT_START

    def _delayed_kwargs(self):
        k = dict(self.kwargs)
        k['coprocessor'] = self.coprocessor
        return k

    def _execute(self, word):
        instr = self.factory.factory(Word(word))
        return instr.execute(
            registers=self.registers,
            program_counter=self.pc,
            memory=self.memory,
            **self._delayed_kwargs(),
        )

    def _decode(self, word):
        instr = self.factory.factory(Word(word))
        return instr.decode(
            registers=self.registers,
            coprocessor=self.coprocessor,
        )

    # ── R-type helpers ───────────────────────────────────────────

    def _set_r(self, num, value):
        self.registers.set_register_value(num, value)

    def _get_r(self, num):
        return self.registers.get_register(num).to_signed_int()

    def _get_r_unsigned(self, num):
        return self.registers.get_register(num).to_unsigned_int()

    # ── R-type: ADD ──────────────────────────────────────────────

    def test_add_decode(self):
        w = _r_word(rs=9, rt=10, rd=8, shamt=0, funct=0x20)
        assert self._decode(w) == "ADD $t0, $t1, $t2"

    def test_add_execute(self):
        self._set_r(9, 5)
        self._set_r(10, 3)
        result = self._execute(_r_word(9, 10, 8, 0, 0x20))
        assert self._get_r(8) == 8
        assert result[1] == self.pc + 4

    def test_add_negative(self):
        self._set_r(9, -5)
        self._set_r(10, -3)
        self._execute(_r_word(9, 10, 8, 0, 0x20))
        assert self._get_r(8) == -8

    # ── R-type: ADDU ─────────────────────────────────────────────

    def test_addu_decode(self):
        w = _r_word(rs=9, rt=10, rd=8, shamt=0, funct=0x21)
        assert self._decode(w) == "ADDU $t0, $t1, $t2"

    def test_addu_execute(self):
        self._set_r(9, 100)
        self._set_r(10, 200)
        self._execute(_r_word(9, 10, 8, 0, 0x21))
        assert self._get_r(8) == 300

    # ── R-type: SUB ──────────────────────────────────────────────

    def test_sub_decode(self):
        w = _r_word(rs=9, rt=10, rd=8, shamt=0, funct=0x22)
        assert self._decode(w) == "SUB $t0, $t1, $t2"

    def test_sub_execute(self):
        self._set_r(9, 10)
        self._set_r(10, 3)
        self._execute(_r_word(9, 10, 8, 0, 0x22))
        assert self._get_r(8) == 7

    # ── R-type: SUBU ─────────────────────────────────────────────

    def test_subu_decode(self):
        w = _r_word(rs=9, rt=10, rd=8, shamt=0, funct=0x23)
        assert self._decode(w) == "SUBU $t0, $t1, $t2"

    def test_subu_execute(self):
        self._set_r(9, 50)
        self._set_r(10, 20)
        self._execute(_r_word(9, 10, 8, 0, 0x23))
        assert self._get_r(8) == 30

    # ── R-type: AND ──────────────────────────────────────────────

    def test_and_decode(self):
        w = _r_word(rs=9, rt=10, rd=8, shamt=0, funct=0x24)
        assert self._decode(w) == "AND $t0, $t1, $t2"

    def test_and_execute(self):
        self._set_r(9, 0xFF)
        self._set_r(10, 0x0F)
        self._execute(_r_word(9, 10, 8, 0, 0x24))
        assert self._get_r(8) == 0x0F

    # ── R-type: OR ───────────────────────────────────────────────

    def test_or_decode(self):
        w = _r_word(rs=9, rt=10, rd=8, shamt=0, funct=0x25)
        assert self._decode(w) == "OR $t0, $t1, $t2"

    def test_or_execute(self):
        self._set_r(9, 0xF0)
        self._set_r(10, 0x0F)
        self._execute(_r_word(9, 10, 8, 0, 0x25))
        assert self._get_r(8) == 0xFF

    # ── R-type: XOR ──────────────────────────────────────────────

    def test_xor_decode(self):
        w = _r_word(rs=9, rt=10, rd=8, shamt=0, funct=0x26)
        assert self._decode(w) == "XOR $t0, $t1, $t2"

    def test_xor_execute(self):
        self._set_r(9, 0xFF)
        self._set_r(10, 0x0F)
        self._execute(_r_word(9, 10, 8, 0, 0x26))
        assert self._get_r(8) == 0xF0

    # ── R-type: NOR ──────────────────────────────────────────────

    def test_nor_decode(self):
        w = _r_word(rs=9, rt=10, rd=8, shamt=0, funct=0x27)
        assert self._decode(w) == "NOR $t0, $t1, $t2"

    # ── R-type: SLT ──────────────────────────────────────────────

    def test_slt_decode(self):
        w = _r_word(rs=9, rt=10, rd=8, shamt=0, funct=0x2A)
        assert self._decode(w) == "SLT $t0, $t1, $t2"

    def test_slt_true(self):
        self._set_r(9, 3)
        self._set_r(10, 5)
        self._execute(_r_word(9, 10, 8, 0, 0x2A))
        assert self._get_r(8) == 1

    def test_slt_false(self):
        self._set_r(9, 5)
        self._set_r(10, 3)
        self._execute(_r_word(9, 10, 8, 0, 0x2A))
        assert self._get_r(8) == 0

    # ── R-type: SLTU ─────────────────────────────────────────────

    def test_sltu_decode(self):
        w = _r_word(rs=9, rt=10, rd=8, shamt=0, funct=0x2B)
        assert self._decode(w) == "SLTU $t0, $t1, $t2"

    def test_sltu_true(self):
        self._set_r(9, 1)
        self._set_r(10, 2)
        self._execute(_r_word(9, 10, 8, 0, 0x2B))
        assert self._get_r(8) == 1

    # ── R-type: SLL ──────────────────────────────────────────────

    def test_sll_decode(self):
        w = _r_word(rs=0, rt=9, rd=8, shamt=2, funct=0x00)
        assert self._decode(w) == "SLL $t0, $t1, 2"

    def test_sll_execute(self):
        self._set_r(9, 1)
        self._execute(_r_word(0, 9, 8, 3, 0x00))
        assert self._get_r(8) == 8

    def test_sll_nop_decode(self):
        w = _r_word(rs=0, rt=0, rd=0, shamt=0, funct=0x00)
        assert self._decode(w) == "nop"

    def test_sll_nop_execute(self):
        self._set_r(8, 42)
        result = self._execute(_r_word(0, 0, 0, 0, 0x00))
        assert result[1] == self.pc + 4

    # ── R-type: SRL ──────────────────────────────────────────────

    def test_srl_decode(self):
        w = _r_word(rs=0, rt=9, rd=8, shamt=4, funct=0x02)
        assert self._decode(w) == "SRL $t0, $t1, 4"

    def test_srl_execute(self):
        self._set_r(9, 16)
        self._execute(_r_word(0, 9, 8, 2, 0x02))
        assert self._get_r(8) == 4

    # ── R-type: SRA ──────────────────────────────────────────────

    def test_sra_decode(self):
        w = _r_word(rs=0, rt=9, rd=8, shamt=2, funct=0x03)
        assert self._decode(w) == "SRA $t0, $t1, 2"

    def test_sra_execute(self):
        self._set_r(9, -8)
        self._execute(_r_word(0, 9, 8, 1, 0x03))
        assert self._get_r(8) == -4

    # ── R-type: MULT ─────────────────────────────────────────────

    def test_mult_decode(self):
        w = _r_word(rs=9, rt=10, rd=0, shamt=0, funct=0x18)
        assert self._decode(w) == "MULT $t1, $t2"

    def test_mult_execute(self):
        self._set_r(9, 6)
        self._set_r(10, 7)
        self._execute(_r_word(9, 10, 0, 0, 0x18))
        assert self.registers.get_lo().to_signed_int() == 42
        assert self.registers.get_hi().to_signed_int() == 0

    # ── R-type: DIV ──────────────────────────────────────────────

    def test_div_decode(self):
        w = _r_word(rs=9, rt=10, rd=0, shamt=0, funct=0x1A)
        assert self._decode(w) == "DIV $t1, $t2"

    def test_div_execute(self):
        self._set_r(9, 17)
        self._set_r(10, 5)
        self._execute(_r_word(9, 10, 0, 0, 0x1A))
        assert self.registers.get_lo().to_signed_int() == 3
        assert self.registers.get_hi().to_signed_int() == 2

    # ── R-type: MFHI ─────────────────────────────────────────────

    def test_mfhi_decode(self):
        w = _r_word(rs=0, rt=0, rd=8, shamt=0, funct=0x10)
        assert self._decode(w) == "MFHI $t0"

    def test_mfhi_execute(self):
        self.registers.set_hi_value(123)
        self._execute(_r_word(0, 0, 8, 0, 0x10))
        assert self._get_r(8) == 123

    # ── R-type: MFLO ─────────────────────────────────────────────

    def test_mflo_decode(self):
        w = _r_word(rs=0, rt=0, rd=8, shamt=0, funct=0x12)
        assert self._decode(w) == "MFLO $t0"

    def test_mflo_execute(self):
        self.registers.set_lo_value(456)
        self._execute(_r_word(0, 0, 8, 0, 0x12))
        assert self._get_r(8) == 456

    # ── R-type: JR ───────────────────────────────────────────────

    def test_jr_decode(self):
        w = _r_word(rs=31, rt=0, rd=0, shamt=0, funct=0x08)
        assert self._decode(w) == "JR $ra"

    def test_jr_execute(self):
        target = TEXT_START + 0x100
        self._set_r(31, target)
        result = self._execute(_r_word(31, 0, 0, 0, 0x08))
        assert result[1] == target

    # ── R-type: JALR ─────────────────────────────────────────────

    def test_jalr_decode(self):
        w = _r_word(rs=31, rt=0, rd=8, shamt=0, funct=0x09)
        assert self._decode(w) == "JALR $ra $t0"

    def test_jalr_execute(self):
        target = TEXT_START + 0x200
        self._set_r(31, target)
        self._execute(_r_word(31, 0, 8, 0, 0x09))
        assert self._get_r(8) == self.pc + 8

    # ── R-type: SYSCALL ──────────────────────────────────────────

    def test_syscall_decode(self):
        w = _r_word(rs=0, rt=0, rd=0, shamt=0, funct=0x0C)
        assert self._decode(w) == "SYSCALL"

    def test_syscall_exit(self):
        self._set_r(2, 10)
        result = self._execute(_r_word(0, 0, 0, 0, 0x0C))
        assert result[1] == -1

    # ── R-type: NOP ──────────────────────────────────────────────

    def test_nop_decode(self):
        w = _r_word(rs=0, rt=0, rd=0, shamt=0, funct=0x0D)
        assert self._decode(w) == "nop"

    def test_nop_execute(self):
        self._set_r(8, 99)
        result = self._execute(_r_word(0, 0, 0, 0, 0x0D))
        assert result[1] == self.pc + 4

    # ── I-type: ADDI ─────────────────────────────────────────────

    def test_addi_decode(self):
        w = _i_word(opcode=0x08, rs=9, rt=8, imm=5)
        assert self._decode(w) == "ADDI $t0, $t1, 5"

    def test_addi_execute(self):
        self._set_r(9, 10)
        self._execute(_i_word(0x08, 9, 8, 5))
        assert self._get_r(8) == 15

    def test_addi_negative_immediate(self):
        self._set_r(9, 10)
        self._execute(_i_word(0x08, 9, 8, 0xFFFB))
        assert self._get_r(8) == 5

    # ── I-type: ADDIU ────────────────────────────────────────────

    def test_addiu_decode(self):
        w = _i_word(opcode=0x09, rs=9, rt=8, imm=7)
        assert self._decode(w) == "ADDIU $t0, $t1, 7"

    def test_addiu_execute(self):
        self._set_r(9, 0)
        self._execute(_i_word(0x09, 9, 8, 42))
        assert self._get_r(8) == 42

    # ── I-type: ANDI ─────────────────────────────────────────────

    def test_andi_decode(self):
        w = _i_word(opcode=0x0C, rs=9, rt=8, imm=0x00FF)
        assert self._decode(w) == "ANDI $t0, $t1, 255"

    def test_andi_execute(self):
        self._set_r(9, 0xABCD)
        self._execute(_i_word(0x0C, 9, 8, 0x00FF))
        assert self._get_r(8) == 0x00CD

    # ── I-type: ORI ──────────────────────────────────────────────

    def test_ori_decode(self):
        w = _i_word(opcode=0x0D, rs=9, rt=8, imm=0x00FF)
        assert self._decode(w) == "ORI $t0, $t1, 255"

    def test_ori_execute(self):
        self._set_r(9, 0xAB00)
        self._execute(_i_word(0x0D, 9, 8, 0x00FF))
        assert self._get_r(8) == 0xABFF

    # ── I-type: SLTI ─────────────────────────────────────────────

    def test_slti_decode(self):
        w = _i_word(opcode=0x0A, rs=9, rt=8, imm=10)
        assert self._decode(w) == "SLTI $t0, $t1, 10"

    def test_slti_true(self):
        self._set_r(9, 5)
        self._execute(_i_word(0x0A, 9, 8, 10))
        assert self._get_r(8) == 1

    def test_slti_false(self):
        self._set_r(9, 15)
        self._execute(_i_word(0x0A, 9, 8, 10))
        assert self._get_r(8) == 0

    # ── I-type: LUI ──────────────────────────────────────────────

    def test_lui_decode(self):
        w = _i_word(opcode=0x0F, rs=0, rt=8, imm=0x1234)
        assert self._decode(w) == "LUI $t0, 4660"

    def test_lui_execute(self):
        self._execute(_i_word(0x0F, 0, 8, 0xABCD))
        assert self._get_r_unsigned(8) == 0xABCD0000

    # ── I-type: LW ───────────────────────────────────────────────

    def test_lw_decode(self):
        w = _i_word(opcode=0x23, rs=9, rt=8, imm=4)
        assert self._decode(w) == "LW $t0, 4($t1)"

    def test_lw_execute(self):
        base_addr = 0x10010000
        val = 0xDEADBEEF
        self.memory.init_store(base_addr + 4, val)
        self._set_r(9, base_addr)
        self._execute(_i_word(0x23, 9, 8, 4))
        assert self._get_r_unsigned(8) == val

    def test_lw_with_negative_offset(self):
        base_addr = 0x10010010
        val = 0xCAFEBABE
        self.memory.init_store(base_addr - 4, val)
        self._set_r(9, base_addr)
        self._execute(_i_word(0x23, 9, 8, 0xFFFC))
        assert self._get_r_unsigned(8) == val

    # ── I-type: SW ───────────────────────────────────────────────

    def test_sw_decode(self):
        w = _i_word(opcode=0x2B, rs=9, rt=8, imm=8)
        assert self._decode(w) == "SW $t0, 8($t1)"

    def test_sw_execute(self):
        base_addr = 0x10010000
        self._set_r(8, 0x12345678)
        self._set_r(9, base_addr)
        self._execute(_i_word(0x2B, 9, 8, 8))
        stored = self.memory.load(base_addr + 8).data
        assert stored == 0x12345678

    # ── I-type: LB ───────────────────────────────────────────────

    def test_lb_decode(self):
        w = _i_word(opcode=0x20, rs=9, rt=8, imm=0)
        assert self._decode(w) == "LB $t0, 0($t1)"

    def test_lb_execute(self):
        base_addr = 0x10010000
        self.memory.init_store(base_addr, 0x000000AB)
        self._set_r(9, base_addr)
        self._execute(_i_word(0x20, 9, 8, 0))
        assert self._get_r(8) == 0xAB

    # ── I-type: BEQ ──────────────────────────────────────────────

    def test_beq_decode(self):
        w = _i_word(opcode=0x04, rs=9, rt=8, imm=3)
        assert self._decode(w) == "BEQ $t0, $t1, 3"

    def test_beq_taken(self):
        self._set_r(8, 5)
        self._set_r(9, 5)
        result = self._execute(_i_word(0x04, 9, 8, 2))
        assert result[1] == self.pc + 4 + (2 * 4)

    def test_beq_not_taken(self):
        self._set_r(8, 5)
        self._set_r(9, 7)
        result = self._execute(_i_word(0x04, 9, 8, 2))
        assert result[1] == self.pc + 4

    # ── I-type: BNE ──────────────────────────────────────────────

    def test_bne_decode(self):
        w = _i_word(opcode=0x05, rs=9, rt=8, imm=3)
        assert self._decode(w) == "BNE $t0, $t1, 3"

    def test_bne_taken(self):
        self._set_r(8, 5)
        self._set_r(9, 7)
        result = self._execute(_i_word(0x05, 9, 8, 2))
        assert result[1] == self.pc + 4 + (2 * 4)

    def test_bne_not_taken(self):
        self._set_r(8, 5)
        self._set_r(9, 5)
        result = self._execute(_i_word(0x05, 9, 8, 2))
        assert result[1] == self.pc + 4

    # ── I-type: BLEZ ─────────────────────────────────────────────

    def test_blez_decode(self):
        w = _i_word(opcode=0x06, rs=9, rt=8, imm=3)
        assert self._decode(w) == "BLEZ $t0, $t1, 3"

    def test_blez_taken(self):
        self._set_r(9, -1)
        self._set_r(8, 0)
        result = self._execute(_i_word(0x06, 9, 8, 2))
        assert result[1] == self.pc + 4 + (2 * 4)

    def test_blez_not_taken(self):
        self._set_r(9, 5)
        self._set_r(8, 0)
        result = self._execute(_i_word(0x06, 9, 8, 2))
        assert result[1] == self.pc + 4

    # ── I-type: BGEZ ─────────────────────────────────────────────

    def test_bgez_decode(self):
        w = _i_word(opcode=0x01, rs=9, rt=8, imm=3)
        assert self._decode(w) == "BGEZ $t0, $t1, 3"

    def test_bgez_taken(self):
        self._set_r(9, 10)
        self._set_r(8, 5)
        result = self._execute(_i_word(0x01, 9, 8, 2))
        assert result[1] == self.pc + 4 + (2 * 4)

    def test_bgez_not_taken(self):
        self._set_r(9, -1)
        self._set_r(8, 0)
        result = self._execute(_i_word(0x01, 9, 8, 2))
        assert result[1] == self.pc + 4

    # ── I-type: LH ───────────────────────────────────────────────

    def test_lh_decode(self):
        w = _i_word(opcode=0x21, rs=9, rt=8, imm=1)
        assert self._decode(w) == "LH $t0, 1($t1)"

    # ── I-type: LHU ──────────────────────────────────────────────

    def test_lhu_decode(self):
        w = _i_word(opcode=0x25, rs=9, rt=8, imm=1)
        assert self._decode(w) == "LHU $t0, 1($t1)"

    # ── J-type: J ────────────────────────────────────────────────

    def test_j_decode(self):
        w = _j_word(opcode=0x02, addr=0x400)
        assert self._decode(w) == "J 4096"

    def test_j_execute(self):
        result = self._execute(_j_word(0x02, 0x100))
        assert result[1] == 0x100 * 4

    # ── J-type: JAL ──────────────────────────────────────────────

    def test_jal_decode(self):
        w = _j_word(opcode=0x03, addr=0x400)
        assert self._decode(w) == "JAL 4096"

    def test_jal_execute(self):
        result = self._execute(_j_word(0x03, 0x200))
        assert self._get_r(31) == self.pc + 8
        assert result[1] == 0x200 * 4

    # ── Floating R-type: ADD.S ───────────────────────────────────

    def test_add_s_decode(self):
        w = _fr_word(opcode=0x11, fmt=0x10, ft=2, fs=0, fd=1, funct=0x00)
        assert self._decode(w) == "ADD.S $f1, $f0, $f2"

    def test_add_s_execute(self):
        a_i = Float2Int.convert(1.5, doubled=False)
        b_i = Float2Int.convert(2.75, doubled=False)
        expected = Float2Int.convert(4.25, doubled=False)
        self.coprocessor.registers.set_register_value(0, a_i)
        self.coprocessor.registers.set_register_value(2, b_i)
        self._execute(_fr_word(0x11, 0x10, 2, 0, 1, 0x00))
        assert self.coprocessor.registers.get_register(1).get_data() == expected

    # ── Floating R-type: SUB.S ───────────────────────────────────

    def test_sub_s_decode(self):
        w = _fr_word(opcode=0x11, fmt=0x10, ft=2, fs=0, fd=1, funct=0x01)
        assert self._decode(w) == "SUB.S $f1, $f0, $f2"

    def test_sub_s_execute(self):
        a_i = Float2Int.convert(5.0, doubled=False)
        b_i = Float2Int.convert(2.0, doubled=False)
        expected = Float2Int.convert(3.0, doubled=False)
        self.coprocessor.registers.set_register_value(0, a_i)
        self.coprocessor.registers.set_register_value(2, b_i)
        self._execute(_fr_word(0x11, 0x10, 2, 0, 1, 0x01))
        assert self.coprocessor.registers.get_register(1).get_data() == expected

    # ── Floating R-type: MUL.S ───────────────────────────────────

    def test_mul_s_decode(self):
        w = _fr_word(opcode=0x11, fmt=0x10, ft=2, fs=0, fd=1, funct=0x02)
        assert self._decode(w) == "MUL.S $f1, $f0, $f2"

    def test_mul_s_execute(self):
        a_i = Float2Int.convert(3.0, doubled=False)
        b_i = Float2Int.convert(4.0, doubled=False)
        expected = Float2Int.convert(12.0, doubled=False)
        self.coprocessor.registers.set_register_value(0, a_i)
        self.coprocessor.registers.set_register_value(2, b_i)
        self._execute(_fr_word(0x11, 0x10, 2, 0, 1, 0x02))
        assert self.coprocessor.registers.get_register(1).get_data() == expected

    # ── Floating R-type: MFC1 ────────────────────────────────────

    def test_mfc1_decode(self):
        w = _fr_word(opcode=0x11, fmt=0x00, ft=8, fs=0, fd=0, funct=0x00)
        assert self._decode(w) == "MFC1 $t0, $f0"

    def test_mfc1_execute(self):
        val = 0x40490FDB
        self.coprocessor.registers.set_register_value(0, val)
        self._execute(_fr_word(0x11, 0x00, 8, 0, 0, 0x00))
        assert self._get_r(8) == val

    # ── Floating R-type: MTC1 ────────────────────────────────────

    def test_mtc1_decode(self):
        w = _fr_word(opcode=0x11, fmt=0x04, ft=8, fs=0, fd=0, funct=0x00)
        assert self._decode(w) == "MTC1 $t0, $f0"

    def test_mtc1_execute(self):
        self._set_r(8, 0x3F800000)
        self._execute(_fr_word(0x11, 0x04, 8, 0, 0, 0x00))
        assert self.coprocessor.registers.get_register(0).get_data() == 0x3F800000

    # ── Floating R-type: MOV.S ───────────────────────────────────

    def test_mov_s_decode(self):
        w = _fr_word(opcode=0x11, fmt=0x10, ft=0, fs=2, fd=1, funct=0x06)
        assert self._decode(w) == "MOV.S $f1, $f2"

    def test_mov_s_execute(self):
        val = 0x40490FDB
        self.coprocessor.registers.set_register_value(2, val)
        self._execute(_fr_word(0x11, 0x10, 0, 2, 1, 0x06))
        assert self.coprocessor.registers.get_register(1).get_data() == val

    # ── Floating I-type: LWC1 ────────────────────────────────────

    def test_lwc1_decode(self):
        w = _fi_word(opcode=0x31, base=9, ft=2, offset=0)
        assert self._decode(w) == "LWC1 $f2, 0($t1)"

    def test_lwc1_execute(self):
        base_addr = 0x10010000
        val = 0x40490FDB
        self.memory.init_store(base_addr, val)
        self._set_r(9, base_addr)
        self._execute(_fi_word(0x31, 9, 2, 0))
        assert self.coprocessor.registers.get_register(2).get_data() == val

    # ── Floating I-type: SWC1 ────────────────────────────────────

    def test_swc1_decode(self):
        w = _fi_word(opcode=0x39, base=9, ft=2, offset=0)
        assert self._decode(w) == "SWC1 $f2, 0($f9)"

    def test_swc1_execute(self):
        base_addr = 0x10010000
        val = 0x40490FDB
        self.coprocessor.registers.set_register_value(2, val)
        self._set_r(9, base_addr)
        self._execute(_fi_word(0x39, 9, 2, 0))
        assert self.memory.load(base_addr).data == val

    # ── Register zero is immune to writes ────────────────────────

    def test_register_zero_ignored(self):
        w = _r_word(rs=9, rt=9, rd=0, shamt=0, funct=0x20)
        self._set_r(9, 42)
        self._execute(w)
        assert self._get_r(0) == 0

    # ── Branch delay slot executes ───────────────────────────────

    def test_beq_delay_slot_updates_register(self):
        self._set_r(8, 5)
        self._set_r(9, 5)
        delayed_word = _i_word(opcode=0x08, rs=0, rt=10, imm=42)
        self.memory.init_store(self.pc + 4, delayed_word)
        self._execute(_i_word(0x04, 9, 8, 2))
        assert self._get_r(10) == 42
