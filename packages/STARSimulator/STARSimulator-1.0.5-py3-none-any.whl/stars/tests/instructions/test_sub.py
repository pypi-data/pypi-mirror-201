import unittest

from interpreter import instructions
from interpreter.registers import Registers

class TestSub(unittest.TestCase):
    
    def test_sub(self):
        '''
            Tests the sub instruction sets the destination register to the difference of the 
            two source registers.
        '''
        reg = Registers()
        reg.set_register("$t0", 2113)
        reg.set_register("$t1", 420)
        instructions.sub("$t2", "$t0", "$t1", reg)
        ret = reg.get_register("$t2")
        self.assertEqual(2113 - 420, ret)