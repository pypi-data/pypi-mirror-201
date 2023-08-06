import unittest

from interpreter import instructions
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestBgezal(unittest.TestCase):

    def test_bgezal_1(self):
        '''
            Tests the bgezal instruction sets pc to the address of the label and ra to the
            current address if the source register contains the value zero
        '''
        mem = Memory(False)
        mem.addLabel('label', 0x12345678)
        reg = Registers()
        reg.set_register('pc', 0x400000)
        reg.set_register("$t0", 0)
        instructions.bgezal('label', "$t0", mem, reg)
        self.assertEqual(0x12345678, reg.get_register('pc'))
        self.assertEqual(0x400000, reg.get_register('$ra'))
        
    def test_bgezal_2(self):
        '''
            Tests the bgezal instruction sets pc to the address of the label and ra to the
            current address if the source register contains a value greater than zero
        '''
        mem = Memory(False)
        mem.addLabel('label', 0x12345678)
        reg = Registers()
        reg.set_register('pc', 0x400000)
        reg.set_register("$t0", 20)
        instructions.bgezal('label', "$t0", mem, reg)
        self.assertEqual(0x12345678, reg.get_register('pc'))
        self.assertEqual(0x400000, reg.get_register('$ra'))