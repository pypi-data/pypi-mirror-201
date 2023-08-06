import unittest

from interpreter import instructions
from interpreter.registers import Registers
from interpreter.utility import overflow_detect

class TestSra(unittest.TestCase):
    def test_srav(self):
        '''
            Tests the srav instruction sets the destination register to the source 
            register shifted right by the value of operand with the signed bit
        '''
        reg = Registers()
        reg.set_register("$t0", -2 ** 31)
        reg.set_register("$t1", 24)
        instructions.srav("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        ret = overflow_detect(ret)
        self.assertEqual(-128, ret)

    def test_srav_lower(self):
        '''
            Tests the srav instruction sets the destination register to the source 
            register shifted right by the value of of the lower 5 bits of the 
            operand with the signed bit.
        '''
        reg = Registers()
        reg.set_register("$t0", -2 ** 31)
        reg.set_register("$t1", 152) # 128 + 24
        instructions.srav("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        ret = overflow_detect(ret)
        self.assertEqual(-128, ret)