import unittest

from interpreter import instructions
from interpreter.exceptions import MemoryOutOfBounds
from interpreter.memory import Memory
from interpreter.registers import Registers

class TestLb(unittest.TestCase):
    # Load operations
    # Lb
    # Positive
    def test_lb_1(self):
        '''
            Tests lb instruction sets the register with the provided byte address
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addByte(30, 0x10010005)
        reg.set_register("$t1", 0x10010005)
        instructions.lb('$t0', "$t1", 0, mem, reg)
        self.assertEqual(30, reg.get_register('$t0'))

    # Sign extend
    def test_lb_2(self):
        '''
            Tests lb instruction sets the register with the provided sign extended
            byte address
        '''
        reg = Registers(False)
        mem = Memory(False)
        mem.addByte(0xF0, 0x10010005)
        reg.set_register("$t1", 0x10010005)
        instructions.lb('$t0', "$t1", 0, mem, reg)
        self.assertEqual(-16, reg.get_register('$t0'))

    # Address out of range
    def test_lb_3(self):
        '''
            Tests lb instruction raises MemoryOutOfBounds when trying to load
            from invalid address
        '''
        reg = Registers(False)
        mem = Memory(False)
        reg.set_register("$t1", 0x10000005)
        self.assertRaises(MemoryOutOfBounds, instructions.lb, '$t0', "$t1", 0, mem, reg)

    # Nothing there
    def test_lb_4(self):
        '''
            Tests lb instruction sets the register to 0 when the provided byte
            is contains nothing
        '''
        reg = Registers(False)
        mem = Memory(False)
        reg.set_register("$t1", 0x10010002)
        instructions.lb('$t0', "$t1", 0, mem, reg)
        self.assertEqual(0, reg.get_register('$t0'))