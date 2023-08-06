import unittest

from interpreter import instructions
from interpreter.exceptions import DivisionByZero
from interpreter.registers import Registers
from interpreter.utility import overflow_detect

class TestDiv(unittest.TestCase):
    # Div
    # General case: pos / pos
    def test_div_1(self):
        '''
            Tests the div instruction sets the destination register to the quotion of
            the two positive source registers
        '''
        reg = Registers()
        reg.set_register('$t0', 30000)
        reg.set_register('$t1', 59)
        instructions.div('$t0', '$t1', reg)
        low = overflow_detect(reg.get_register('lo'))
        high = overflow_detect(reg.get_register('hi'))
        self.assertEqual((508, 28), (low, high))

    # General case: pos / neg
    def test_div_2(self):
        '''
            Tests the div instruction sets the destination register to the quotion of
            the positive divide by negitive source registers
        '''
        reg = Registers()
        reg.set_register('$t0', 30000)
        reg.set_register('$t1', -59)
        instructions.div('$t0', '$t1', reg)
        low = overflow_detect(reg.get_register('lo'))
        high = overflow_detect(reg.get_register('hi'))
        self.assertEqual((-508, 28), (low, high))

    # General case: neg / pos
    def test_div_3(self):
        '''
            Tests the div instruction sets the destination register to the quotion of
            the negitive divide by positive source registers
        '''
        reg = Registers()
        reg.set_register('$t0', -30000)
        reg.set_register('$t1', 59)
        instructions.div('$t0', '$t1', reg)
        low = overflow_detect(reg.get_register('lo'))
        high = overflow_detect(reg.get_register('hi'))
        self.assertEqual((-508, -28), (low, high))

    # General case: neg / neg
    def test_div_4(self):
        '''
            Tests the div instruction sets the destination register to the quotion of
            the two negitive source registers
        '''
        reg = Registers()
        reg.set_register('$t0', -30000)
        reg.set_register('$t1', -59)
        instructions.div('$t0', '$t1', reg)
        low = overflow_detect(reg.get_register('lo'))
        high = overflow_detect(reg.get_register('hi'))
        self.assertEqual((508, -28), (low, high))

    # Division by 0
    def test_div_5(self):
        '''
            Tests the div instruction raises a DivisionByZero error when dividing by zero
        '''
        reg = Registers()
        reg.set_register('$t0', 5)
        reg.set_register('$t1', 0)
        self.assertRaises(DivisionByZero, instructions.div, '$t0', '$t1', reg)
