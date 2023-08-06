import unittest

from interpreter import instructions
from interpreter.exceptions import InvalidImmediate
from interpreter.registers import Registers

class TestSlti(unittest.TestCase):
    # Slti
    # Invalid immediate
    def test_slti(self):
        '''
            Tests the slti instruction sets the target register to 1 if the value
            stored in source register is less than the immediate, 0 otherwise
        '''
        reg = Registers()
        reg.set_register("$t0", 3)
        self.assertRaises(InvalidImmediate, instructions.slti, "$t1", "$t0", 60000, reg)