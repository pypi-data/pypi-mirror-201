import unittest

from interpreter import instructions
from interpreter.exceptions import InvalidImmediate
from interpreter.registers import Registers

class TestSltiu(unittest.TestCase):
    # Sltiu
    # Invalid immediate
    def test_sltiu(self):
        '''
            Tests the sltiu instruction raises InvalidImmediate if the immediate is invalid
        '''
        reg = Registers()
        reg.set_register("$t0", 3)
        self.assertRaises(InvalidImmediate, instructions.slti, "$t1", "$t0", -60000, reg, signed=True)