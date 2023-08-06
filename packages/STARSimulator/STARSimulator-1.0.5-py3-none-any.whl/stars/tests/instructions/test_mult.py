import unittest

from interpreter import instructions
from interpreter.registers import Registers
from interpreter.utility import overflow_detect

class TestMult(unittest.TestCase):
    # Mult
    # General case: positive
    def test_mult_1(self):
        '''
            Tests the mult instruction sets the lo and hi register to the product of
            the two positive source registers
        '''
        reg = Registers()
        reg.set_register("$t0", 0x7F000FFF)
        reg.set_register("$t1", 0x7F000FFF)
        instructions.mult("$t0", "$t1", reg)
        ret = reg.get_register("lo"), reg.get_register("hi")
        self.assertEqual((50323457, 1057034207), ret)

    # General case: negative
    def test_mult_2(self):
        '''
            Tests the mult instruction sets the lo and hi register to the product of
            a positive and a negitive source registers
        '''
        reg = Registers()
        reg.set_register("$t0", 0x7F000FFF)
        reg.set_register("$t1", -200)
        instructions.mult("$t0", "$t1", reg)
        low, high = reg.get_register("lo"), reg.get_register("hi")
        low = overflow_detect(low)
        high = overflow_detect(high)
        self.assertEqual((-940343096, -100), (low, high))