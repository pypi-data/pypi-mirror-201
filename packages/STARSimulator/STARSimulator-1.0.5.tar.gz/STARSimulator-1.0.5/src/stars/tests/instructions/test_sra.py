import unittest

from interpreter import instructions
from interpreter.registers import Registers
from interpreter.utility import overflow_detect

class TestSra(unittest.TestCase):
    # Sra
    def test_sra(self):
        '''
            Tests the srav instruction sets the destination register to the source 
            register shifted right by the immediate amount with the signed bit
        '''
        reg = Registers()
        reg.set_register("$t0", -2 ** 31)
        instructions.sra("$t1", "$t0", 24, reg)
        ret = reg.get_register("$t1")
        ret = overflow_detect(ret)
        self.assertEqual(-128, ret)