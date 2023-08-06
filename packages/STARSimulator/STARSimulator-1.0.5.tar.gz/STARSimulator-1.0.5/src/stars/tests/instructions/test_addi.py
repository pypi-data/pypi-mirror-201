import unittest

from interpreter import instructions
from interpreter.exceptions import InvalidImmediate
from interpreter.registers import Registers

class TestAddi(unittest.TestCase):
    # Addi
    # General case
    def test_addi_1(self):
        '''
            Tests the addi instruction sets the destination register to the sum of the 
            two immediate.
        '''
        reg = Registers()
        reg.set_register("$t0", 30000)
        instructions.addi("$t1", "$t0", 420, reg)
        ret = reg.get_register("$t1")
        self.assertEqual(30420, ret)

    # Invalid immediate value
    def test_addi_2(self):
        '''
            Tests InvalidImmediate is raised when one of the registers is empty
        '''
        reg = Registers()
        reg.set_register("$t0", 30000)
        self.assertRaises(InvalidImmediate, instructions.addi, "$t1", "$t0", 60000, reg)