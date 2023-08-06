import unittest

from interpreter import instructions
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestLbu(unittest.TestCase):
    # Lbu
    # General case
    def test_lbu_1(self):
        '''
            Tests the lbu register sets the register with the provided byte address without
            sign extending
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addByte(0xF0, 0x10010005)
        reg.set_register("$t1", 0x10010005)
        instructions.lb('$t0', "$t1", 0, mem, reg, signed=False)
        self.assertEqual(0xF0, reg.get_register('$t0'))

    # More than one byte
    def test_lbu_2(self):
        '''
            Tests the lbu register sets the register with the provided bytes address without
            sign extending
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addByte(0xFFF0, 0x10010005)
        reg.set_register("$t1", 0x10010005)
        instructions.lb('$t0', "$t1", 0, mem, reg, signed=False)
        self.assertEqual(0xF0, reg.get_register('$t0'))