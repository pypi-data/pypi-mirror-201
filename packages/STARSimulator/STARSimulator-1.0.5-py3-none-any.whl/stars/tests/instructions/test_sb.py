import unittest

from interpreter import instructions
from interpreter.exceptions import MemoryOutOfBounds
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestSb(unittest.TestCase):
    # sb
    # General case
    def test_sb_1(self):
        '''
            Tests the sb instruction stores the byte from the register into the 
            memory address
        '''
        mem = Memory(False)
        reg = Registers()
        reg.set_register("$t0", 0xF4)
        reg.set_register("$t1", 0x10010005)
        instructions.sb('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0xF4, mem.data[str(0x10010005)])

    # Address out of range
    def test_sb_2(self):
        '''
            Tests the sb instruction raises a MemoryOutOfBounds when the memory
            address is out of bound
        '''
        mem = Memory(False)
        reg = Registers()
        reg.set_register("$t0", 0xF4)
        reg.set_register("$t1", 0x1001005)
        self.assertRaises(MemoryOutOfBounds, instructions.sb, '$t0', "$t1", 0, mem, reg)

    # More than one byte
    def test_sb_3(self):
        '''
            Tests the sb instruction stores the byte from the register into the 
            memory address
        '''
        mem = Memory(False)
        reg = Registers()
        reg.set_register("$t0", 0x12345678)
        reg.set_register("$t1", 0x10010005)
        instructions.sb('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x78, mem.data[str(0x10010005)])

    # Negative address
    def test_sb_4(self):
        '''
            Tests the sb instruction stores the byte from the register into the 
            negitive memory address
        '''
        mem = Memory(False)
        reg = Registers()
        reg.set_register("$t0", 0xF4)
        reg.set_register("$t1", 0xffff0000)
        instructions.sb('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0xF4, mem.data[str(0xffff0000)])