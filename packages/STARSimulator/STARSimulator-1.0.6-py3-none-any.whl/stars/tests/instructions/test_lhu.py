import unittest

from interpreter import instructions
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestLhu(unittest.TestCase):
    # Lhu
    # Zero extend
    def test_lhu(self):
        '''
            Tests the lhu register sets the register with the provided halfword address
            without sign extending
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addHWord(0xFFFF, 0x10010006)
        reg.set_register("$t1", 0x10010006)
        instructions.lh('$t0', "$t1", 0, mem, reg, signed=False)
        self.assertEqual(0xFFFF, reg.get_register('$t0'))