import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestClz(unittest.TestCase):
    # Clz
    # Positive
    def test_clz_1(self):
        '''
            Test the clz instruction, counting the leading ones in the register
            containing positive number
        '''
        reg = Registers()
        reg.set_register('$t1', 200000)
        instructions.clz('$t0', '$t1', reg)
        self.assertEqual(14, reg.get_register('$t0'))

    # Negative
    def test_clz_2(self):
        '''
            Test the clz instruction, counting the leading ones in the register
            containing negitive number
        '''
        reg = Registers()
        reg.set_register('$t1', -200000)
        instructions.clz('$t0', '$t1', reg)
        self.assertEqual(0, reg.get_register('$t0'))

    # 0
    def test_clz_3(self):
        '''
            Test the clz instruction, counting the leading ones in the register
            containing 0
        '''
        reg = Registers()
        reg.set_register('$t1', 0)
        instructions.clz('$t0', '$t1', reg)
        self.assertEqual(32, reg.get_register('$t0'))