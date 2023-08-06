import unittest

from interpreter import instructions
from interpreter.exceptions import InvalidImmediate
from interpreter.registers import Registers

class TestSll(unittest.TestCase):
    # Shifting
    # Sll
    # General case
    def test_sll_1(self):
        '''
            Tests the sll instruction sets the destination register to the source 
            register shifted left by the immediate amount
        '''
        reg = Registers()
        reg.set_register("$t0", 1)
        instructions.sll("$t1", "$t0", 5, reg)
        ret = reg.get_register("$t1")
        self.assertEqual(2 ** 5, ret)

    # Invalid shift amount
    def test_sll_2(self):
        '''
            Tests the sll instruction raises InvalidImmediate when the immediate is
            too big
        '''
        reg = Registers()
        reg.set_register("$t0", 1)
        self.assertRaises(InvalidImmediate, instructions.sll, "$t1", "$t0", 32, reg)