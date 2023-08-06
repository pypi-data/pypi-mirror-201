import unittest

from interpreter import instructions
from interpreter.exceptions import MemoryAlignmentError
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestSw(unittest.TestCase):
    # sw
    # General case
    def test_sw_1(self):
        '''
            Tests the sb instruction stores the word from the register into the 
            memory address
        '''
        mem = Memory(False)
        reg = Registers()
        reg.set_register("$t0", 0x1234abcd)
        reg.set_register("$t1", 0x10010004)
        instructions.sw('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0xcd, mem.data[str(0x10010004)])
        self.assertEqual(0xab, mem.data[str(0x10010005)])
        self.assertEqual(0x34, mem.data[str(0x10010006)])
        self.assertEqual(0x12, mem.data[str(0x10010007)])

    # Address unaligned
    def test_sw_2(self):
        '''
            Tests the sw instruction raises a MemoryAlignmentError when the memory
            address is not aligned
        '''
        mem = Memory(False)
        reg = Registers()
        reg.set_register("$t0", 0x1234abcd)
        reg.set_register("$t1", 0x10010006)
        self.assertRaises(MemoryAlignmentError, instructions.sw, '$t0', "$t1", 0, mem, reg)