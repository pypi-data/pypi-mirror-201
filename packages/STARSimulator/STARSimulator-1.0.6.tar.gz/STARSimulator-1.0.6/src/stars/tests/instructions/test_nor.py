import unittest

from interpreter import instructions
from interpreter.registers import Registers
from interpreter.utility import overflow_detect

class TestNor(unittest.TestCase):

    def test_nor(self):
        '''
            Test the nor instruction setting destination register to the
            bitwise nor of the two source register 
        '''
        reg = Registers()
        reg.set_register("$t0", 0x5d9d128d)
        reg.set_register("$t1", 0x30be0a88)
        instructions.nor("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(-2109676174, overflow_detect(ret))