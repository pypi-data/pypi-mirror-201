import unittest

from interpreter import instructions
from interpreter.exceptions import InvalidImmediate
from interpreter.registers import Registers
from interpreter.utility import overflow_detect

class TestLui(unittest.TestCase):
    # Lui
    # Positive
    def test_lui_1(self):
        '''
            Tests the lui instruction sets upper bits of the destination register 
            to the provided positive immediate
        '''
        reg = Registers()
        instructions.lui('$t0', 0xFFF, reg)
        self.assertEqual(0xFFF0000, reg.get_register('$t0'))

    # Negative
    def test_lui_2(self):
        '''
            Tests the lui instruction sets upper bits of the destination register 
            to the provided negitive immediate
        '''
        reg = Registers()
        instructions.lui('$t0', 0xFFFF, reg)
        self.assertEqual(-2 ** 16, overflow_detect(reg.get_register('$t0')))

    # Invalid
    def test_lui_3(self):
        '''
            Tests the lui instruction raises InvalidImmediate when setting an invalid
            immediate
        '''
        reg = Registers()
        self.assertRaises(InvalidImmediate, instructions.lui, '$t0', -1, reg)
        self.assertRaises(InvalidImmediate, instructions.lui, '$t0', 65536, reg)