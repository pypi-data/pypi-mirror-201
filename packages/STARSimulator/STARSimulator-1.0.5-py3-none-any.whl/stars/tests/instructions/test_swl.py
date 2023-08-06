import unittest

from interpreter import instructions
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestSwl(unittest.TestCase):
    # swl
    def test_swl_0(self):
        '''
            Tests swl instruction sets the left bits of the memory address
            with the word in target register
        '''
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg = Registers()
        reg.set_register("$t0", 0x2468abcd)
        reg.set_register("$t1", 0x10010000)
        instructions.swl('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x24, mem.data[str(0x10010000)])
        self.assertEqual(0x56, mem.data[str(0x10010001)])
        self.assertEqual(0x34, mem.data[str(0x10010002)])
        self.assertEqual(0x12, mem.data[str(0x10010003)])

    def test_swl_1(self):
        '''
            Tests swl instruction sets the left bits of the memory address
            with the word in target register
        '''
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg = Registers()
        reg.set_register("$t0", 0x2468abcd)
        reg.set_register("$t1", 0x10010001)
        instructions.swl('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0x68, mem.data[str(0x10010000)])
        self.assertEqual(0x24, mem.data[str(0x10010001)])
        self.assertEqual(0x34, mem.data[str(0x10010002)])
        self.assertEqual(0x12, mem.data[str(0x10010003)])

    def test_swl_2(self):
        '''
            Tests swl instruction sets the left bits of the memory address
            with the word in target register
        '''
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg = Registers()
        reg.set_register("$t0", 0x2468abcd)
        reg.set_register("$t1", 0x10010002)
        instructions.swl('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0xab, mem.data[str(0x10010000)])
        self.assertEqual(0x68, mem.data[str(0x10010001)])
        self.assertEqual(0x24, mem.data[str(0x10010002)])
        self.assertEqual(0x12, mem.data[str(0x10010003)])

    def test_swl_3(self):
        '''
            Tests swl instruction sets the left bits of the memory address
            with the word in target register
        '''
        mem = Memory(False)
        mem.addWord(0x12345678, 0x10010000)
        reg = Registers()
        reg.set_register("$t0", 0x2468abcd)
        reg.set_register("$t1", 0x10010003)
        instructions.swl('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0xcd, mem.data[str(0x10010000)])
        self.assertEqual(0xab, mem.data[str(0x10010001)])
        self.assertEqual(0x68, mem.data[str(0x10010002)])
        self.assertEqual(0x24, mem.data[str(0x10010003)])