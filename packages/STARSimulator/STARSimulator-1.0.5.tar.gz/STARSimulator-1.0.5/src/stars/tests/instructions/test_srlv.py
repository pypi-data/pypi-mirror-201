import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestSrl(unittest.TestCase):
    def test_srlv(self):
        '''
            Tests the srlv instruction sets the destination register to the source 
            register shifted left by the value of operand with zeros
        '''
        reg = Registers()
        reg.set_register("$t0", 2 ** 30)
        reg.set_register("$t1", 24)
        instructions.srlv("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(64, ret)

    def test_srlv_negative(self):
        '''
            Tests the srlv instruction sets the destination register to the source 
            register shifted left by the value of operand with zeros.
        '''
        reg = Registers()
        reg.set_register("$t0", -2 ** 31)
        reg.set_register("$t1", 24)
        instructions.srlv("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(128, ret)

    def test_srlv_lower(self):
        '''
            Tests the srlv instruction sets the destination register to the source 
            register shifted left by the value of the lower 5 bits of the operand with zeros.
        '''
        reg = Registers()
        reg.set_register("$t0", 2 ** 30)
        reg.set_register("$t1", 152) # 128 + 24
        instructions.srlv("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(64, ret)
