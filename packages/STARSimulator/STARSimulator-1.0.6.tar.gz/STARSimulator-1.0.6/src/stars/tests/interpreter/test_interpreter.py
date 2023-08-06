from io import StringIO
import unittest
from unittest import mock

from interpreter.classes import Declaration, IType, Label, LoadImm, PseudoInstr
from interpreter.exceptions import NoMainLabel
from interpreter.interpreter import Interpreter
from interpreter.memory import Memory
from interpreter.registers import Registers
from interpreter.syscalls import getString
from settings import settings

class TestInterpreter(unittest.TestCase):

    def test_handle_args(self):
        '''
            Tests the handle_args properly adds the program arguments to the stack and returns the number of 
            arguments in $a0 and the address of an array of address containing the arguments in $a1.
        '''

        arguments = ['a', 'b', 'c', 'hello', 'world!']

        for i in range(len(arguments)):
            program_arguments = arguments[:i+1]
            number_of_arguments = len(program_arguments)
            inital_sp = settings['initial_$sp']
            expected_array_addr = inital_sp-4*(number_of_arguments)
            new_sp = inital_sp-4*(number_of_arguments+1)
            inter = Interpreter([Label('main')], program_arguments)

            
            self.assertEqual(inter.get_register("$a0"), number_of_arguments,
                    f"The number of arguments added to the stack is not {number_of_arguments}.")
            self.assertEqual(inter.get_register("$sp"), new_sp,
                    f"The value of $sp is incorrect. It should be {new_sp:08x}")
            array = inter.get_register("$a1")
            self.assertEqual(array, expected_array_addr,
                    f"The address of the array is incorrect. It should be {expected_array_addr:08x}")

            for increment in range(i):
                addr = inter.mem.getWord(array+increment*4)
                value = getString(addr, inter.mem)
                self.assertEqual(value, program_arguments[increment],
                        f"The {increment}-th value does not match the value at address {addr}.")


    def test_no_main_label(self):
        '''
            Tests that if the list of instruction does not contain a main Label then a NoMainLabel 
            exeception is raised.
        '''
        self.assertRaises(NoMainLabel, Interpreter, [], [])

    def test_single_label(self):
        '''
            Tests that if the list of instruction contains a Label it is added to the dictionary
            of labels.
        '''
        list_of_labels = ['main', 'first']
        inter = Interpreter([Label(l) for l in list_of_labels], [])

        labels_dict = inter.mem.labels

        for label in list_of_labels:
            self.assertIn(label, labels_dict, f"The label ({label}) not in the dictionary of labels.")
        
        self.assertEqual(len(labels_dict), len(list_of_labels), 
                    f"The size of the labels dictionary is not equal to the number of labels {len(list_of_labels)}.")

    @mock.patch.object(Interpreter, 'set_data')
    def test_initialize_declaration(self, mock_method: mock.patch.object):
        '''
            Tests that set_data is called when initializing a Declaration object.
        '''
        Interpreter([Declaration(None, ".ascii", "'hello'"), Label('main')], [])
        mock_method.assert_called_once()

    def test_psuedo_instruction_load(self):
        '''
            Tests that add the individual instruction making up the pseudoInstruction is added to the text
            section and labels are replaced with the actual instruction. 
        '''
        instrs = [LoadImm('lui', '$at', 0), IType('ori', ["$a0", '$at'], 0)]
        pseudoInstr = PseudoInstr('la $a0 data', instrs)
        pseudoInstr.label = Label("data")

        list_of_instructions = [
            Declaration("data", ".ascii", "'hello'"), 
            Label('main'),
            pseudoInstr
        ]

        inter = Interpreter(list_of_instructions, [])

        instructions = inter.mem.text.values()
        self.assertEqual(len(instructions), 3, 
            "There should be three instructions. The two instructions for the psuedo_instrction and the terminate execution instruction")
        for instruction in instrs:
            self.assertIn(instruction, instructions, f"The instruction ({instruction}) is not in the text section of memory.")
        
        addr = inter.mem.getLabel("data")
        left, right = (addr >> 16) & 0xFFFF, addr & 0xFFFF
        self.assertEqual(instrs[0].imm, left, f"The label is not replaced with the actual address in {instruction}.")
        self.assertEqual(instrs[1].imm, right, f"The label is not replaced with the actual address in {instruction}.")

    
    def test_register_functions(self):
        '''
            Tests that the Registers object equivalent of get and set registers are called when Interpreter get/set
            operations are called.
        '''
        functions = ["get_register", "set_register", "get_reg_word", "set_reg_word"]
        inter = Interpreter([Label('main')], [])

        for function in functions:
            with mock.patch.object(Registers, function) as mock_method:
                with self.subTest(function=function):
                    arguments = ("$a0",) if "get" in function else ("$a0", 0)
                    getattr(inter, function)(*arguments)

                    mock_method.assert_called_once()

    def test_dump(self):
        '''
            Tests that the dump method calls the register and memory dump methods.
        '''
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with mock.patch.object(Registers, "dump") as register_method:
                with mock.patch.object(Memory, "dump") as memory_method:
                    inter = Interpreter([Label('main')], [])
                    inter.dump()
                    register_method.assert_called_once()
                    memory_method.assert_called_once()

                    output = mock_stdout.getvalue()
                    self.assertIn("Registers:\n", output, "Registers were not dump.")
                    self.assertIn("Memory:\n", output, "Memory was not dump.")
                
    def test_reset(self):
        '''
            Tests that the program counter returns to its original value.
        '''
        inter = Interpreter([Label('main')], [])
        initial_pc = inter.get_register("pc")
        inter.set_register("pc", initial_pc+0x100)
        inter.reset()
        self.assertEqual(inter.get_register("pc"), initial_pc, f"The program counter register was not reset.")