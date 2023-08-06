import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestMul(unittest.TestCase):
    # Mul
    # General case: Positive * positive
    def test_mul_1(self):
        '''
            Tests the mul instruction sets the destination register to the product of
            the two positive source registers
        '''
        reg = Registers()
        reg.set_register("$t0", 200)
        reg.set_register("$t1", 300)
        instructions.mul("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(60000, ret)

    # General case: Positive * negative
    def test_mul_2(self):
        '''
            Tests the mul instruction sets the destination register to the product of
            a positive and a negitive source registers
        '''
        reg = Registers()
        reg.set_register("$t0", 200)
        reg.set_register("$t1", -300)
        instructions.mul("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(-60000, ret)

    # General case: Negative * negative
    def test_mul_3(self):
        '''
            Tests the mul instruction sets the destination register to the product of
            the two negitive source registers
        '''
        reg = Registers()
        reg.set_register("$t0", -200)
        reg.set_register("$t1", -300)
        instructions.mul("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(60000, ret)

    # Edge case: more than 32 bits
    def test_mul_4(self):
        '''
            Tests the mul instruction sets the destination register to the product of
            the source registers when the product is more than 32 bits
        '''
        reg = Registers()
        reg.set_register("$t0", 0x7F000FFF)
        reg.set_register("$t1", 0x7F000FFF)
        instructions.mul("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(50323457, ret)
