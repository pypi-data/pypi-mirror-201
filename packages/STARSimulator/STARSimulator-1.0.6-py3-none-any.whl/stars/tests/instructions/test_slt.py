import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestSlt(unittest.TestCase):
    # Slt
    # General case 1
    def test_slt_1(self):
        '''
            Tests the slt instruction sets the destination register to 1 if the value
            stored in source register is less than target register, 0 otherwise
        '''
        reg = Registers()
        reg.set_register("$t0", -3)
        reg.set_register("$t1", 5)
        instructions.slt("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(1, ret)

    # General case 2
    def test_slt_2(self):
        '''
            Tests the slt instruction sets the destination register to 1 if the value
            stored in source register is less than target register, 0 otherwise
        '''
        reg = Registers()
        reg.set_register("$t0", 5)
        reg.set_register("$t1", -3)
        instructions.slt("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(0, ret)