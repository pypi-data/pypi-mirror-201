import unittest

from interpreter import instructions
from interpreter.registers import Registers
from interpreter.utility import overflow_detect

class TestAddu(unittest.TestCase):
    # Addu
    # Positive Overflow
    def test_addu_1(self):
        '''
            Test the addu instruction for positive overflow
        '''
        reg = Registers()
        reg.set_register("$t0", 0x7FFFFFFF)
        reg.set_register("$t1", 0x7FFFFFFF)
        instructions.add("$t2", "$t0", "$t1", reg, signed=False)
        ret = reg.get_register("$t2")
        ret = overflow_detect(ret)
        self.assertEqual(-2, ret)

    # Negative Overflow
    def test_addu_2(self):
        '''
            Test the addu instruction for negative overflow
        '''
        reg = Registers()
        reg.set_register("$t0", 0x80000000)
        reg.set_register("$t1", 0x80000000)
        instructions.add("$t2", "$t0", "$t1", reg, signed=False)
        ret = reg.get_register("$t2")
        ret = overflow_detect(ret)
        self.assertEqual(0, ret)
