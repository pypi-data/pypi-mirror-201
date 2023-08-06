import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestXor(unittest.TestCase):

    def test_xor(self):
        '''
            Test the xor instruction setting destination register to the
            bitwise xor of the two source register 
        '''
        reg = Registers()
        reg.set_register("$t0", 0x5d9d128d)
        reg.set_register("$t1", 0x30be0a88)
        instructions.xor("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(0x6d231805, ret)