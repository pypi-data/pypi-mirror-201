from io import StringIO
import struct
import unittest
import unittest.mock as mock

from constants import REGS
from interpreter.exceptions import WritingToZeroRegister, InvalidRegister
from interpreter.registers import Registers
from settings import settings

class TestRegisters(unittest.TestCase):

    def test_normal_initialization(self):
        '''
            Tests if the registers except ones with initial values in settings are set to 0.
        '''
        test_registers = Registers().reg
        # 35 regular registers + 32 float registers
        self.assertEqual(67 ,len(test_registers), "Not all registers are initialize.")

        for register, value in test_registers.items():
            if f'initial_{register}' in settings.keys():
                self.assertEqual(settings[f'initial_{register}'], value,
                            f"Register {register} is not set to the correct initial value")
            else:
                self.assertEqual(0, value, f"Register {register} is not set to 0.")


    def test_random_initialization(self):
        '''
            Tests if the registers except ones with initial values in settings are set to a
            random value between [0, 2**32) and float registers are 4 bytes long.
        '''
        test_registers = Registers(toggle_garbage=True).reg
        # 35 regular registers + 32 float registers
        self.assertEqual(67 ,len(test_registers), "Not all registers are initialize.")

        for register, value in test_registers.items():
            if f'initial_{register}' in settings.keys():
                self.assertEqual(settings[f'initial_{register}'], value,
                            f"Register {register} is not set to the correct initial value")
            else:
                if register[1] == "f":
                    random_check = len(struct.pack('>f', value))
                else:
                    random_check = value >= 0 and value < 2**32
                self.assertTrue(random_check, 
                    f"Register {register} {value} is not set to a random value between [0, 2**32).")

    def test_get_invalid_register(self):
        '''
            Tests that a InvalidRegister error is raised when trying to get a register that
            does not exist.
        '''
        test_register = Registers()
        self.assertRaises(InvalidRegister, test_register.get_register, "$p1")
        self.assertRaises(InvalidRegister, test_register.get_register, "$p1", double=True)
        self.assertRaises(InvalidRegister, test_register.get_register, "$34")

    def test_set_invalid_register(self):
        '''
            Tests that a InvalidRegister error is raised when trying to set a register that
            does not exist.
        '''
        test_register = Registers()
        self.assertRaises(InvalidRegister, test_register.set_register, "$p1", 1)
        self.assertRaises(InvalidRegister, test_register.set_register, "$p1", 1, double=True)
        self.assertRaises(InvalidRegister, test_register.set_register, "$34", 1)

    def test_set_zero_register(self):
        '''
            Tests that a WritingToZeroRegister Error is raise when there is an attempt to modify
            the zero register.
        '''
        zero_register_representations = ["$0", "$zero"]
        
        for zero in zero_register_representations:
            with self.subTest(zero=zero):
                test_register = Registers()
                self.assertRaises(WritingToZeroRegister, test_register.set_register, zero, 1)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_get_unitialized(self, mock_stderr: StringIO):
        '''
            Tests that a warning is printed to stderr when reading a register that have not been
            initialized when the warnings setting is True.
        '''
        settings['warnings'] = True
        test_register = Registers()

        test_register.get_register("$t0")
        settings['warnings'] = False
        self.assertEqual(mock_stderr.getvalue(), 
                "Reading from uninitialized register $t0!\n",
                "Warning should be printed to stderr.")

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_get_unitialized_no_warning(self, mock_stderr: StringIO):
        '''
            Tests that there is no warning printed to stderr when reading a constant register that 
            have not been initialized when the warnings setting is True.
        '''
        settings['warnings'] = True
        test_register = Registers()

        test_register.get_register("hi")
        settings['warnings'] = False
        self.assertEqual(mock_stderr.getvalue(), 
                "",
                "Warning should not be printed to stderr.")

    def test_get_double_from_odd(self):
        '''
            Tests that a InvalidRegister error is raised when trying to get a double register value
            from an odd float register.
        '''
        test_register = Registers()
        self.assertRaises(InvalidRegister, test_register.get_register, "$f1", double=True)

    def test_set_double_from_odd(self):
        '''
            Tests that a InvalidRegister error is raised when trying to set a double register value
            from an odd float register.
        '''
        test_register = Registers()
        self.assertRaises(InvalidRegister, test_register.set_register, "$f1", 1.0, double=True)
        
    def test_double_register(self):
        '''
            Tests that the double register is set to the correct double precision value.
        '''
        test_register = Registers()
        value = 1.0
        f_register = "$f0"

        test_register.set_register(f_register, value, double=True)
        result = test_register.get_register(f_register, double=True)

        self.assertEqual(value, result, 
                f"The expected result {result} is not the same as the initial value {value}")

    def test_word_register(self):
        '''
            Tests that a float register is set to the word fixed point value.
        '''
        test_register = Registers()
        value = 100
        f_register = "$f0"

        test_register.set_reg_word(f_register, value)
        result = test_register.get_reg_word(f_register)

        self.assertEqual(value, result, 
                f"The expected result {result} is not the same as the initial value {value}")

    def test_register_by_digit(self):
        '''
            Tests if registers can be obtained using the numerical ordering. there are 32 
            registers with numerical ordering from $0 to $31. For example, $9 is the $t0 register.
        '''
        test_register = Registers()

        for i in range(1, 32): 
            test_register.set_register(f"${i}", i)
            result = test_register.get_register(REGS[i])

            self.assertEqual(i, result,
                    f"Register ${i}/{REGS[i]} should have value {i} {test_register.reg}.")

        # test the inverse with set using canonical form
        test_register = Registers()

        for i in range(1, 32): 
            test_register.set_register(REGS[i], i)
            result = test_register.get_register(f"${i}")

            self.assertEqual(i, result,
                    f"Register ${i}/{REGS[i]} should have value {i} {test_register.reg}.")