import unittest

from interpreter import instructions
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestBltz(unittest.TestCase):
    
    def test_bltz(self):
        '''
            Tests the bltz instruction sets pc to the address of the label if
            the source register contains a value less than zero
        '''
        mem = Memory(False)
        mem.addLabel('label', 0x12345678)
        reg = Registers()
        reg.set_register("$t0", -20)
        instructions.bltz('label', "$t0", mem, reg)
        self.assertEqual(0x12345678, reg.get_register('pc'))