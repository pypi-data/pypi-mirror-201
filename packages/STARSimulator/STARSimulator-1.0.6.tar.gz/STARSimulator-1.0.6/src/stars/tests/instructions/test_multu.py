import unittest

from interpreter import instructions
from interpreter.registers import Registers
from interpreter.utility import overflow_detect

class TestMultu(unittest.TestCase):
    # Multu
    # General case
    def test_multu(self):
        '''
            Tests the multu instruction sets the lo and hi register to the product of
            a positive and a negitive source registers without sign extending
        '''
        reg = Registers()
        reg.set_register("$t0", 300)
        reg.set_register("$t1", -200)
        instructions.mult("$t0", "$t1", reg, signed=False)
        low, high = reg.get_register("lo"), reg.get_register("hi")
        low = overflow_detect(low)
        high = overflow_detect(high)
        self.assertEqual((-60000, 299), (low, high))