import unittest

from interpreter import instructions
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestBltzal(unittest.TestCase):

    def test_bltzal(self):
        '''
            Tests the blezal instruction sets pc to the address of the label and ra to the
            current address if the source register contains a value less than zero
        '''
        mem = Memory(False)
        mem.addLabel('label', 0x12345678)
        reg = Registers()
        reg.set_register('pc', 0x400000)
        reg.set_register("$t0", -20)
        instructions.bltzal('label', "$t0", mem, reg)
        self.assertEqual(0x12345678, reg.get_register('pc'))
        self.assertEqual(0x400000, reg.get_register('$ra'))