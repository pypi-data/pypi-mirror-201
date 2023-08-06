import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestJr(unittest.TestCase):
    
    def test_jr(self):
        '''
            Tests the jr instruction sets pc to the address of the register
        '''
        reg = Registers()
        reg.set_register('$t0', 0x1234)
        instructions.jr('pc', '$t0', reg)
        self.assertEqual(0x1234, reg.get_register('pc'))