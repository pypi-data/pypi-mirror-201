import unittest

from interpreter import instructions
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestLwl(unittest.TestCase):
    # Lwl
    # Test with different alignment
    def test_lwl_0(self):
        '''
            Tests lwl instruction sets the left bits of the register with the provided word
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg.set_register('$t0', 0x2468abcd)
        reg.set_register("$t1", 0x10010000)
        instructions.lwl('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x7868abcd, reg.get_register('$t0'))

    def test_lwl_1(self):
        '''
            Tests lwl instruction sets the left bits of the register with the provided word
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg.set_register('$t0', 0x2468abcd)
        reg.set_register("$t1", 0x10010001)
        instructions.lwl('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x5678abcd, reg.get_register('$t0'))

    def test_lwl_2(self):
        '''
            Tests lwl instruction sets the left bits of the register with the provided word
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg.set_register('$t0', 0x2468abcd)
        reg.set_register("$t1", 0x10010002)
        instructions.lwl('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x345678cd, reg.get_register('$t0'))

    def test_lwl_3(self):
        '''
            Tests lwl instruction sets the left bits of the register with the provided word
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg.set_register('$t0', 0x2468abcd)
        reg.set_register("$t1", 0x10010003)
        instructions.lwl('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x12345678, reg.get_register('$t0'))