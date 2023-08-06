import unittest

from interpreter import instructions
from interpreter.exceptions import MemoryAlignmentError
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestLw(unittest.TestCase):
    # Lw
    # General case
    def test_lw_1(self):
        '''
            Tests lw instruction sets the register with the provided word
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addWord(0x1234abcd, 0x10010008)
        reg.set_register("$t1", 0x10010008)
        instructions.lw('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x1234abcd, reg.get_register('$t0'))

    # Address unaligned
    def test_lw_2(self):
        '''
            Tests lw instruction raises MemoryAlignmentError when the address is not aligned
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addWord(0x1234abcd, 0x10010008)
        reg.set_register("$t1", 0x10010007)
        self.assertRaises(MemoryAlignmentError, instructions.lw, '$t0', "$t1", 0, mem, reg)

    # Nothing there
    def test_lw_3(self):
        '''
            Tests lh instruction sets the register to 0 when the provided word
            contains nothing
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addByte(0xFF, 0x10010002)
        reg.set_register("$t1", 0x10010000)
        instructions.lw('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x00FF0000, reg.get_register('$t0'))