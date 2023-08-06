import unittest

from interpreter import instructions
from interpreter.exceptions import MemoryAlignmentError
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestLh(unittest.TestCase):
    # Lh
    # General case
    def test_lh_1(self):
        '''
            Tests lh instruction sets the register with the provided half word
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addHWord(3000, 0x10010006)
        reg.set_register("$t1", 0x10010006)
        instructions.lh('$t0', "$t1", 0, mem, reg)
        self.assertEqual(3000, reg.get_register('$t0'))

    # Sign extend
    def test_lh_2(self):
        '''
            Tests lh instruction sets the register with the provided sign extended 
            half word
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addHWord(0xFFFF, 0x10010006)
        reg.set_register("$t1", 0x10010006)
        instructions.lh('$t0', "$t1", 0, mem, reg)
        self.assertEqual(-1, reg.get_register('$t0'))

    # Address unaligned
    def test_lh_3(self):
        '''
            Tests lh instruction raises MemoryAlignmentError when the address is not aligned
        '''
        reg = Registers(False)
        mem = Memory(False)
        reg.set_register("$t1", 0x10010005)
        self.assertRaises(MemoryAlignmentError, instructions.lh, '$t0', "$t1", 0, mem, reg)

    # Nothing there
    def test_lh_4(self):
        '''
            Tests lh instruction sets the register to 0 when the provided halfword
            contains nothing
        '''
        reg = Registers(False)
        mem = Memory(False)
        reg.set_register("$t1", 0x10010002)
        instructions.lh('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0, reg.get_register('$t0'))

    # More than one byte
    def test_lh_5(self):
        '''
            Tests lh instruction sets the register with the provided half word address
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addHWord(0x7F000F, 0x10010006)
        reg.set_register("$t1", 0x10010006)
        instructions.lh('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0xF, reg.get_register('$t0'))
