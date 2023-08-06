import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestSrl(unittest.TestCase):
    # Srl
    # positive
    def test_srl_1(self):
        '''
            Tests the srl instruction sets the destination register to the source 
            register shifted left by the immediate amount with zeros
        '''
        reg = Registers()
        reg.set_register("$t0", 2 ** 30)
        instructions.srl("$t1", "$t0", 24, reg)
        ret = reg.get_register("$t1")
        self.assertEqual(64, ret)

    # Negative
    def test_srl_2(self):
        '''
            Tests the srl instruction sets the destination register to the source 
            register shifted left by the immediate amount with zeros
        '''
        reg = Registers()
        reg.set_register("$t0", -2 ** 31)
        instructions.srl("$t1", "$t0", 24, reg)
        ret = reg.get_register("$t1")
        self.assertEqual(128, ret)