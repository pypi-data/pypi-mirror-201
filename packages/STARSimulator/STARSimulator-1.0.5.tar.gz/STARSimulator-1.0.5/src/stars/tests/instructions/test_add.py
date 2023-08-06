import unittest

from interpreter import instructions
from interpreter.exceptions import ArithmeticOverflow
from interpreter.registers import Registers

class TestAdd(unittest.TestCase):

    def test_add(self):
        '''
            Tests the add instruction sets the destination register to the sum of the 
            two source registers.
        '''
        reg = Registers()
        reg.set_register("$t0", 2113)
        reg.set_register("$t1", 420)
        instructions.add("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(2113 + 420, ret)

    def test_positive_overflow(self):
        '''
            Tests that an ArithmeticOverflow error is raised adding two large positive 
            numbers (2^31-1: maximum) together.
        '''
        reg = Registers()
        reg.set_register("$t0", 0x7FFFFFFF)
        reg.set_register("$t1", 0x7FFFFFFF)
        self.assertRaises(ArithmeticOverflow, instructions.add, "$t2", "$t0", "$t1", reg)

    def test_negative_overflow(self):
        '''
            Tests that an ArithmeticOverflow error is raised adding two large negative 
            numbers (-2^31: minimum) together.
        '''
        reg = Registers()
        reg.set_register("$t0", 0x80000000)
        reg.set_register("$t1", 0x80000000)
        self.assertRaises(ArithmeticOverflow, instructions.add, "$t2", "$t0", "$t1", reg)
    