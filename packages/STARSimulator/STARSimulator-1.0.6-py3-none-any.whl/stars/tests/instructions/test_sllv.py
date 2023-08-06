import unittest

from interpreter import instructions
from interpreter.registers import Registers
from interpreter.utility import overflow_detect

class TestSllv(unittest.TestCase):
    # Sllv
    # shamt out of range 0-31
    def test_sllv(self):
        '''
            Tests the sll instruction sets the destination register to the source 
            register shifted left by the amount in the target register
        '''
        reg = Registers()
        reg.set_register("$t0", 1)
        reg.set_register("$t1", -1)
        instructions.sllv("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        ret = overflow_detect(ret)
        self.assertEqual(-2 ** 31, ret)