import unittest

from interpreter import instructions
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestJal(unittest.TestCase):
    # jal
    # Valid case
    def test_jal_1(self):
        '''
            Tests the jal instruction sets pc to the address of the label and set
            $ra to the previous location
        '''
        mem = Memory(False)
        mem.addLabel('label', 0x12345678)
        reg = Registers()
        reg.set_register('pc', 0x400000)
        instructions.jal(mem.getLabel('label'), reg)
        self.assertEqual(0x12345678, reg.get_register('pc'))
        self.assertEqual(0x400000, reg.get_register('$ra'))

    # Invalid case
    # def test_jal_2(self):
    #     '''
    #         Tests the jal instruction raises InvalidLabel when trying to jump to 
    #         a invalid label
    #     '''
    #     mem = Memory(False)
    #     mem.addLabel('label', 0x12345678)
    #     reg = Registers()
    #     reg.reg = {'pc': 0x400000}
    #     self.assertRaises(InvalidLabel, instructions.jal, reg, mem.getLabel('wack'))