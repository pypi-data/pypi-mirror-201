import unittest

from interpreter import instructions
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestLwr(unittest.TestCase):
    # Lwr
    # Test with different alignment
    def test_lwr_0(self):
        '''
            Tests lwl instruction sets the right bits of the register with the provided word
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg.set_register('$t0', 0x2468abcd)
        reg.set_register("$t1", 0x10010000)
        instructions.lwr('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x12345678, reg.get_register('$t0'))

    def test_lwr_1(self):
        '''
            Tests lwl instruction sets the right bits of the register with the provided word
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg.set_register('$t0', 0x2468abcd)
        reg.set_register("$t1", 0x10010001)
        instructions.lwr('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x24123456, reg.get_register('$t0'))

    def test_lwr_2(self):
        '''
            Tests lwl instruction sets the right bits of the register with the provided word
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg.set_register('$t0', 0x2468abcd)
        reg.set_register("$t1", 0x10010002)
        instructions.lwr('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x24681234, reg.get_register('$t0'))

    def test_lwr_3(self):
        '''
            Tests lwl instruction sets the right bits of the register with the provided word
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg.set_register('$t0', 0x2468abcd)
        reg.set_register("$t1", 0x10010003)
        instructions.lwr('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x2468ab12, reg.get_register('$t0'))