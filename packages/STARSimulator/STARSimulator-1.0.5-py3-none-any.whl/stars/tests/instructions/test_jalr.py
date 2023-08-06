import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestJalr(unittest.TestCase):
    # jalr
    def test_jalr(self):
        '''
            Tests the jalr instruction sets pc to the address of the register and set
            $ra to the previous location
        '''
        reg = Registers()
        reg.set_register('pc', 0x400000)
        reg.set_register('$t0', 0x1234)
        instructions.jalr('pc', '$ra', '$t0', reg)
        self.assertEqual(0x400000, reg.get_register('$ra'))
        self.assertEqual(0x1234, reg.get_register('pc'))