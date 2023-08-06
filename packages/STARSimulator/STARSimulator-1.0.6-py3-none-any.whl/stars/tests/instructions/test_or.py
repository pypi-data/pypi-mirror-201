import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestOr(unittest.TestCase):

    def test_or(self):
        '''
            Test the or instruction setting destination register to the
            bitwise or of the two source register 
        '''
        reg = Registers()
        reg.set_register("$t0", 0x5d9d128d)
        reg.set_register("$t1", 0x30be0a88)
        instructions._or("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(0x7dbf1a8d, ret)