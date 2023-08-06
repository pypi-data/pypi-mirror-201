import unittest

from interpreter.classes import *
from interpreter.exceptions import InvalidArgument

class TestClasses(unittest.TestCase):

    def test_declaration(self):
        '''
            Tests that a declaration object is initialize properly.
        '''
        object = Declaration('data', '.ascii', '"hello"')

        self.assertEqual(str(object), "data: .ascii", f"The string representation does not match.")

    def test_Breakpoint(self):
        '''
            Tests that a Breakpoint object is initialize properly.
        '''
        object = Breakpoint()

        self.assertEqual(str(object), "breakpoint", f"The string representation does not match.")

    def test_Nop(self):
        '''
            Tests that a Nop object is initialize properly.
        '''
        object = Nop()

        self.assertEqual(str(object), "nop", f"The string representation does not match.")

    def test_RType_jalr(self):
        '''
            Tests that a RType object with op = jalr is initialize properly.
        '''
        op, regs = "jalr", ['$ra', "$t1"]
        object = RType(op, regs)

        self.assertEqual(str(object), "jalr $t1", f"The string representation does not match.")
        self.assertEqual(object.get_dest(), regs[:1], f"The destination value does not match the pc register.")
        self.assertEqual(object.get_src(), regs[1:], f"The source value does not match the given register.")

        op, regs = "jalr", ['$t1', "$t2"]
        object = RType(op, regs)

        self.assertEqual(str(object), "jalr $t1, $t2", f"The string representation does not match.")
        self.assertEqual(object.get_dest(), regs[:1], f"The destination value does not match the pc register.")
        self.assertEqual(object.get_src(), regs[1:], f"The source value does not match the given register.")

    def test_RType_jr(self):
        '''
            Tests that a RType object with op = jr is initialize properly.
        '''
        op, regs = "jr", ['pc', "$t1"]
        object = RType(op, regs)

        self.assertEqual(str(object), "jr $t1", f"The string representation does not match.")
        self.assertEqual(object.get_dest(), regs[:1], f"The destination value does not match the pc register.")
        self.assertEqual(object.get_src(), regs[1:], f"The source value does not match the given register.")

    def test_RType(self):
        '''
            Tests that a RType object is initialize properly.
        '''
        op, regs = "add", ["$a0", "$t0", "$t1"]
        object = RType(op, regs)

        self.assertEqual(str(object), "add $a0, $t0, $t1", f"The string representation does not match.")
        self.assertEqual(object.get_dest(), regs[:1], f"The destination value does not match the first register.")
        self.assertEqual(object.get_src(), regs[1:], f"The source value does not match the second and third registers.")

    def test_Move(self):
        '''
            Tests that a Move object is initialize properly.
        '''
        op, reg = "mfhi", "$t1"
        object = Move(op, reg)

        self.assertEqual(str(object), "mfhi $t1", f"The string representation does not match.")
        self.assertEqual(object.get_dest(), [reg], f"The destination value does not match the register.")
        self.assertEqual(object.get_src(), ["hi"], f"The source value does not match the hi register.")

        op, reg = "mthi", "$t1"
        object = Move(op, reg)

        self.assertEqual(str(object), "mthi $t1", f"The string representation does not match.")
        self.assertEqual(object.get_dest(), ["hi"], f"The destination value does not match the register.")
        self.assertEqual(object.get_src(), ["$t1"], f"The source value does not match the hi register.")

    def test_MoveFloat(self):
        '''
            Tests that a MoveFloat object is initialize properly.
        '''
        op, regs = "mfc1", ["$t1", "$f1"]
        object = MoveFloat(op, regs)

        self.assertEqual(str(object), "mfc1 $t1, $f1", f"The string representation does not match.")

    def test_Compare(self):
        '''
            Tests that a Compare object is initialize properly.
        '''
        op, rt, rs, flag = "c.eq.d", "$f2", "$f4", 1
        object = Compare(op, rt, rs, flag)

        self.assertEqual(str(object), "c.eq.d $f2, $f4, 1", f"The string representation does not match.")

    def test_Compare_invalid(self):
        '''
            Tests that a Compare object with an invalid flag raises an InvalidArgument exception.
        '''
        op, rt, rs, flag = "c.eq.d", "$f2", "$f4", 10
        self.assertRaises(InvalidArgument, Compare,  op, rt, rs, flag)

    def test_Convert(self):
        '''
            Tests that a Convert object is initialize properly.
        '''
        op, rt, rs = "cvt.d.s", "$f2", "$f1"
        object = Convert(op, rt, rs)

        self.assertEqual(str(object), "cvt.d.s $f2, $f1", f"The string representation does not match.")

    def test_Branch(self):
        '''
            Tests that a Branch object is initialize properly.
        '''
        op, rt, rs, label = "beq", "$a0", "$a1", Label("next")
        object = Branch(op, rt, rs, label)

        self.assertEqual(str(object), "beq $a0, $a1, next", f"The string representation does not match.")
        self.assertEqual(object.get_src(), [rt, rs], f"The source value does not match the immediate.")
        self.assertEqual(object.get_dest(), [label.name], f"The destination value does not match the immediate.")

    def test_BranchFloat(self):
        '''
            Tests that a BranchFloat object is initialize properly.
        '''
        op, label, flag = "bc1f", Label("next"), 0
        object = BranchFloat(op, label, flag)

        self.assertEqual(str(object), "bc1f 0 next", f"The string representation does not match.")
        self.assertEqual(object.get_src(), [flag], f"The source value does not match the immediate.")

    def test_BranchFloat_invalid(self):
        '''
            Tests that a BranchFloat object with an invalid flag raises an InvalidArgument exception.
        '''
        op, label, flag = "bc1f", Label("next"), 10
        self.assertRaises(InvalidArgument, BranchFloat, op, label, flag)
    
    def test_LoadImm(self):
        '''
            Tests that a LoadImm object is initialize properly.
        '''
        op, reg, imm = "li", "$a0", 0
        object = LoadImm(op, reg, imm)

        self.assertEqual(str(object), "li $a0, 0x00000000", f"The string representation does not match.")
        self.assertEqual(object.get_src(), [imm], f"The source value does not match the immediate.")

    def test_LoadMem(self):
        '''
            Tests that a LoadMem object is initialize properly.
        '''
        op, reg, addr, imm = "lb", "$a0", "$a1", 0
        object = LoadMem(op, reg, addr, imm)

        self.assertEqual(str(object), "lb $a0, 0($a1)", f"The string representation does not match.")

    def test_JType(self):
        '''
            Tests that a JType object is initialize properly.
        '''
        op, label = "j", Label("next")
        object = JType(op, label)

        self.assertEqual(str(object), "j next", f"The string representation does not match.")

    def test_Change(self):
        '''
            Tests that a change object is initialize properly.
        '''
        pc = 4
        change = Change(pc)
        self.assertEqual(change.pc, pc, "The pc attribute does not match.")

    def test_FlagChange(self):
        '''
            Tests that a flag change object is initialize properly.
        '''
        flag, value, pc = 1, True, 4
        change = FlagChange(flag, value, pc)
        self.assertEqual(change.flag, flag, "The flag attribute does not match.")
        self.assertEqual(change.value, value, "The value attribute does not match.")
        self.assertEqual(change.pc, pc, "The pc attribute does not match.")

    def test_MChange(self):
        '''
            Tests that a move change object is initialize properly.
        '''
        hi, lo, pc = 1, 1, 4
        change = MChange(hi, lo, pc)
        self.assertEqual(change.hi, hi, "The hi attribute does not match.")
        self.assertEqual(change.lo, lo, "The lo attribute does not match.")
        self.assertEqual(change.pc, pc, "The pc attribute does not match.")

    def test_MemChange(self):
        '''
            Tests that a memory change object is initialize properly.
        '''
        addr, val, pc, type = 1, 1, 4, 'w'
        change = MemChange(addr, val, pc, type)
        self.assertEqual(change.addr, addr, "The addr attribute does not match.")
        self.assertEqual(change.val, val, "The val attribute does not match.")
        self.assertEqual(change.pc, pc, "The pc attribute does not match.")
        self.assertEqual(change.type, type, "The type attribute does not match.")

    def test_RegChange(self):
        '''
            Tests that a register change object is initialize properly.
        '''
        reg, val, pc, is_double = "$a0", 1, 4, True
        change = RegChange(reg, val, pc, is_double)
        self.assertEqual(change.reg, reg, "The reg attribute does not match.")
        self.assertEqual(change.val, val, "The val attribute does not match.")
        self.assertEqual(change.pc, pc, "The pc attribute does not match.")
        self.assertEqual(change.is_double, is_double, "The is_double attribute does not match.")