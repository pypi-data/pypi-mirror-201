import unittest

from interpreter import instructions
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestJ(unittest.TestCase):
    # Jump operations
    # j
    # Valid case
    def test_j_1(self):
        '''
            Tests the j instruction sets pc to the address of the label
        '''
        mem = Memory(False)
        mem.addLabel('label', 0x12345678)
        reg = Registers()
        instructions.j(mem.getLabel('label'), reg)
        self.assertEqual(0x12345678, reg.get_register('pc'))

    # Invalid case
    # def test_j_2(self):
    #     '''
    #         Tests the j instruction raises InvalidLabel when trying to jump to 
    #         a invalid label
    #     '''
    #     mem = Memory(False)
    #     mem.addLabel('label', 0x12345678)
    #     reg = Registers()
    #     self.assertRaises(InvalidLabel, instructions.j, reg, mem.getLabel('wack'))