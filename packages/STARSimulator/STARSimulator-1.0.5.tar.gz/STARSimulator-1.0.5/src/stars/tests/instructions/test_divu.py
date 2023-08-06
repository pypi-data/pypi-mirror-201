import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestDivu(unittest.TestCase):
    # Divu
    def test_divu(self):
        '''
            Tests the divu instruction sets the destination register to the quotion of
            the the two unsigned source registers
        '''
        reg = Registers()
        reg.set_register('$t0', -30000)
        reg.set_register('$t1', 59)
        instructions.div('$t0', '$t1', reg, signed=False)
        low = reg.get_register('lo')
        high = reg.get_register('hi')
        self.assertEqual((72795547, 23), (low, high))