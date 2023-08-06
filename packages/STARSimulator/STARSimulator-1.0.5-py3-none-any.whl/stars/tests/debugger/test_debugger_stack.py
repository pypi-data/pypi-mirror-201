import unittest
import unittest.mock as mock

from interpreter.classes import *
from interpreter.debugger import Debug
from interpreter.interpreter import Interpreter
from settings import settings

class TestDebugger(unittest.TestCase):

    def setUp(self) -> None:
        '''
            Creates an empty Debug object with an empty stack.
        '''
        super().setUp()
        settings['garbage_registers'] = True
        self.debug = Debug()
        self.inter = Interpreter([Declaration("data", ".asciiz", "'hello'"), Label('main')], [])

    def test_push_div(self):
        '''
            Tests the an instruction that modifies the hi/lo registers is properly pushed onto 
            the stack as a MChange.
        '''
        op, regs = "div", ["$t0", "$t1"]
        object = RType(op, regs)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, MChange, f"The change is not a MChange.")
    
    def test_push_move(self):
        '''
            Tests the a move instruction is properly pushed onto the stack as a
            register change.
        '''
        op, reg = "mfhi", "$t1"
        object = Move(op, reg)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, RegChange, f"The change is not a register change.")

    def test_push_loadImm(self):
        '''
            Tests the a LoadImm instruction is properly pushed onto the stack as a
            register change.
        '''
        op, reg, imm = "li", "$a0", 0
        object = LoadImm(op, reg, imm)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, RegChange, f"The change is not a register change.")

    def test_push_jType(self):
        '''
            Tests the a JType instruction is properly pushed onto the stack as a
            change.
        '''
        op, label = "j", Label("next")
        object = JType(op, label)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, Change, f"The change is not a change.")
    
    def test_push_jal(self):
        '''
            Tests the jal instruction is properly pushed onto the stack as a
            register change.
        '''
        op, label = "jal", Label("next")
        object = JType(op, label)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, RegChange, f"The change is not a reg change.")

    def test_push_loadMem_load(self):
        '''
            Tests the a LoadMem instruction is properly pushed onto the stack as a
            register change.
        '''
        op, reg, addr, imm = "lb", "$a0", "$a1", 0
        object = LoadMem(op, reg, addr, imm)
        self.inter.instr = object
        self.inter.set_register("$a1", self.inter.mem.getLabel("data"))

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, RegChange, f"The change is not a register change.")

    def test_push_loadMem_store(self):
        '''
            Tests the a LoadMem instruction that stores a value in memory is properly pushed 
            onto the stack as a mem change.
        '''
        op, reg, addr, imm = "sb", "$a0", "$a1", 0
        object = LoadMem(op, reg, addr, imm)
        self.inter.instr = object
        self.inter.set_register("$a1", self.inter.mem.getLabel("data"))

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, MemChange, f"The change is not a mem change.")

    def test_push_compare(self):
        '''
            Tests the a Compare instruction is properly pushed onto the stack as 
            a flag change.
        '''
        op, rt, rs, flag = "c.eq.d", "$f2", "$f4", 1
        object = Compare(op, rt, rs, flag)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, FlagChange, f"The change is not a flag change.")

    def test_push_convert(self):
        '''
            Tests the a Convert instruction is properly pushed onto the stack as 
            a register change.
        '''
        op, rt, rs = "cvt.d.s", "$f2", "$f1"
        object = Convert(op, rt, rs)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, RegChange, f"The change is not a reg change.")

    def test_push_moveFloat(self):
        '''
            Tests the a MoveFloat instruction is properly pushed onto the stack as 
            a register change.
        '''
        op, regs = "mfc1", ["$t1", "$f1"]
        object = MoveFloat(op, regs)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, RegChange, f"The change is not a reg change.")

        op, regs = "mtc1", ["$t1", "$f1"]
        object = MoveFloat(op, regs)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 2, f"The size of the stack is not two.")

        change = stack[1]
        self.assertIsInstance(change, RegChange, f"The change is not a reg change.")

        op, regs = "movz.d", ["$f2", "$f4", "$t3"]
        object = MoveFloat(op, regs)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 3, f"The size of the stack is not two.")

        change = stack[2]
        self.assertIsInstance(change, RegChange, f"The change is not a reg change.")

    def test_push_moveCond(self):
        '''
            Tests the a MoveCond instruction is properly pushed onto the stack as 
            a register change.
        '''
        op, rt, rs, flag = "movf.d", "$f2", "$f4", 1
        object = MoveCond(op, rt, rs, flag)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, RegChange, f"The change is not a reg change.")

    def test_push_branch(self):
        '''
            Tests the a Branch instruction is properly pushed onto the stack as 
            a change.
        '''
        op, rt, rs, label = "beq", "$a0", "$a1", Label("next")
        object = Branch(op, rt, rs, label)
        self.inter.instr = object

        self.debug.push(self.inter)

        stack = self.debug.stack
        self.assertEqual(len(stack), 1, f"The size of the stack is not one.")

        change = stack[0]
        self.assertIsInstance(change, Change, f"The change is not a change.")

    def test_reverse_regChange(self):
        '''
            Tests that a RegChange is pop and the registers are modified to be their
            previous value.
        '''
        self.inter.mem.text['4194300'] = "BLANK_FILLER"
        op, reg = "mfhi", "$t1"
        object = Move(op, reg)
        self.inter.instr = object

        original_t1 = self.inter.get_register("$t1")
        original_hi = self.inter.get_register("hi")
        self.debug.push(self.inter)

        self.inter.execute_instr(object)
        new_t1 = self.inter.get_register("$t1")

        self.assertEqual(new_t1, original_hi, f"The value of $t1 does not match the value for the hi register.")

        self.debug.reverse([], self.inter)
        reversed_t1 = self.inter.get_register("$t1")

        self.assertEqual(reversed_t1, original_t1, f"The value of $t1 does not match the original value of $t1.")

    def test_reverse_MChange(self):
        '''
            Tests that a MChange is pop and the hi/lo registers are modified to be their
            previous value.
        '''
        self.inter.mem.text['4194300'] = "BLANK_FILLER"
        op, regs = "div", ["$t0", "$t1"]
        object = RType(op, regs)
        self.inter.instr = object

        original_lo = self.inter.get_register("lo")
        original_hi = self.inter.get_register("hi")
        self.debug.push(self.inter)

        self.inter.execute_instr(object)
        self.debug.reverse([], self.inter)
        reversed_lo = self.inter.get_register("lo")
        reversed_hi = self.inter.get_register("hi")

        self.assertEqual(reversed_lo, original_lo, f"The value of lo does not match the original value of lo.")
        self.assertEqual(reversed_hi, original_hi, f"The value of hi does not match the original value of hi.")

    def test_reverse_FlagChange(self):
        '''
            Tests that a FlagChange is pop and the conditional flag is modified to be its
            previous value.
        '''
        self.inter.mem.text['4194300'] = "BLANK_FILLER"
        op, regs = "mov.d", ["$f2", "$f4"]
        object = RType(op, regs)
        self.inter.execute_instr(object) # sets f2 to f4

        op, rt, rs, flag = "c.eq.d", "$f2", "$f4", 1
        object = Compare(op, rt, rs, flag)
        self.inter.instr = object

        original_flag = self.inter.condition_flags[1]
        self.debug.push(self.inter)
        self.inter.execute_instr(object)

        new_flag = self.inter.condition_flags[1]
        self.assertTrue(new_flag, f"The new flag is not True.")
        
        self.debug.reverse([], self.inter)
        reversed_flag = self.inter.condition_flags[1]

        self.assertEqual(reversed_flag, original_flag, f"The value of flag 1 does not match the original value of flag 1.")

    def test_reverse_MemChange(self):
        '''
            Tests that a FlagChange is pop and the conditional flag is modified to be its
            previous value.
        '''
        self.inter.mem.text['4194300'] = "BLANK_FILLER"
        self.inter.set_register("$a0", 72) # H
        self.inter.set_register("$a1", self.inter.mem.getLabel("data"))
        op, reg, addr, imm = "sb", "$a0", "$a1", 0
        object = LoadMem(op, reg, addr, imm)
        self.inter.instr = object

        original_string = self.inter.mem.getString("data")
        self.debug.push(self.inter)
        self.inter.execute_instr(object)

        new_string = self.inter.mem.getString("data")
        self.assertEqual(new_string, "Hello", f"The string was not modified")
        
        self.debug.reverse([], self.inter)
        reversed_string = self.inter.mem.getString("data")

        self.assertEqual(reversed_string, original_string, f"The value of string does not match the original value of string.")