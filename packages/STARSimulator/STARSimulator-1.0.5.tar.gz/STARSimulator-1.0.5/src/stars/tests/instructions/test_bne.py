import unittest

from interpreter import instructions
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestBne(unittest.TestCase):
    
    def test_bne(self):
        '''
            Tests the beq instruction sets pc to the address of the label if
            the source and the target registers contains the same value
        '''
        mem = Memory(False)
        mem.addLabel('label', 0x12345678)
        reg = Registers()
        reg.set_register("$t0", 100)
        reg.set_register("$t1", 200)
        instructions.bne('label', "$t0", "$t1", mem, reg)
        self.assertEqual(0x12345678, reg.get_register('pc'))