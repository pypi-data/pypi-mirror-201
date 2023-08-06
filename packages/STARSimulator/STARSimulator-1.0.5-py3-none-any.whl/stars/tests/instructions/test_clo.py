import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestClo(unittest.TestCase):
    # Clo
    # Positive
    def test_clo_1(self):
        '''
            Test the clo instruction, counting the leading ones in the register
            containing positive number
        '''
        reg = Registers()
        reg.set_register('$t1', 200000)
        instructions.clo('$t0', '$t1', reg)
        self.assertEqual(0, reg.get_register('$t0'))

    # Negative
    def test_clo_2(self):
        '''
            Test the clo instruction, counting the leading ones in the register
            containing negitive number
        '''
        reg = Registers()
        reg.set_register('$t1', -200000)
        instructions.clo('$t0', '$t1', reg)
        self.assertEqual(14, reg.get_register('$t0'))

    # -1
    def test_clo_3(self):
        '''
            Test the clo instruction, counting the leading ones in the register
            containing -1
        '''
        reg = Registers()
        reg.set_register('$t1', -1)
        instructions.clo('$t0', '$t1', reg)
        self.assertEqual(32, reg.get_register('$t0'))