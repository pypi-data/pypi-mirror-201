import unittest

from interpreter import instructions
from interpreter.exceptions import MemoryAlignmentError
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestSh(unittest.TestCase):
    # sh
    # General case
    def test_sh_1(self):
        '''
            Tests the sh instruction stores the half from the register into the 
            memory address
        '''
        mem = Memory(False)
        reg = Registers()
        reg.set_register("$t0", 0xabcd)
        reg.set_register("$t1", 0x10010006)
        instructions.sh('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0xcd, mem.data[str(0x10010006)])
        self.assertEqual(0xab, mem.data[str(0x10010007)])

    # Address unaligned
    def test_sh_2(self):
        '''
            Tests the sh instruction raises a MemoryAlignmentError when the memory
            address is not aligned
        '''
        mem = Memory(False)
        reg = Registers()
        reg.set_register("$t0", 0xabcd)
        reg.set_register("$t1", 0x10010007)
        self.assertRaises(MemoryAlignmentError, instructions.sh, '$t0', "$t1", 0, mem, reg)