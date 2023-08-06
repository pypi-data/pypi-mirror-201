from io import StringIO
from os import path as p
import unittest
import unittest.mock as mock

from interpreter import debugger
import sbumips

class TestDebugger(unittest.TestCase):
    
    @mock.patch('builtins.input', side_effect=['q'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_quit(self, mock_stdout: StringIO, mock_input):
        '''
            Tests that the debugger quits successfully.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")

    @mock.patch('builtins.input', side_effect=['quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_quit_full(self, mock_stdout: StringIO, mock_input):
        '''
            Tests that the debugger quits successfully.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")

    @mock.patch('builtins.input', side_effect=['uwu', 'q'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch.object(debugger, 'print_usage_text')
    def test_invalid_command(self, mock_method: mock.patch.object, mock_stdout: StringIO, mock_input):
        '''
            Tests that the help instructions are printed when an invalid command is inputted.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])
        mock_method.assert_called_once()      

    @mock.patch('builtins.input', side_effect=['help', 'q'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_help(self, mock_stdout: StringIO, mock_input):
        '''
            Tests that the help instructions are printed when help is inputted.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])
        
        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
USAGE:  
[b]reak <filename> <line_no>
[d]elete: Clear all breakpoints
[n]ext: Step to the next instruction
[c]ontinue: Run until the next breakpoint
[i]nfo b: Print information about the breakpoints
[p]rint <flag>
[p]rint <reg> <format>
[p]rint <label> <data_type> <length> <format>
[q]uit: Terminate the program
[h]elp: Print this usage text
[r]everse: Step back to the previous instruction
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")      


    @mock.patch('builtins.input', side_effect=['next', 'quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_next(self, mock_stdout: StringIO, mock_input):
        '''
            Tests that the debugger executes the current instruction and steps to the 
            next instruction when next is input.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
li $a0 10 (ori $a0, $0, 0x0000000a)
 "{p.dirname(__file__)}/test.asm", 15
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")

    @mock.patch('builtins.input', side_effect=['break tests/debugger/test.asm 15', 'info', 'delete', 'info', 'break tests/debugger/test.asm 15', 'info', 'quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_addBreakpoint(self, mock_stdout: StringIO, mock_input):
        '''
            Tests that a breakpoint is added, removed, and readded to the 
            set of breakpoints successfully.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
1 "tests/debugger/test.asm" 15
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
1 "tests/debugger/test.asm" 15
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_addBreakpoint_invalid(self, mock_stdout: StringIO):
        '''
            Tests that the help instructions are printed when an invalid break command is inputted.
        '''
        invalid_break_commands = ['break tests/debugger/test.asm 0xff', 'break tests/debugger/test.asm 15 10', 'break tests/debugger/test.asm']

        for invalid in invalid_break_commands:
            with mock.patch('builtins.input', side_effect=[invalid, 'quit']) as mock_input:
                with mock.patch.object(debugger, 'print_usage_text') as mock_method:
                    with self.subTest(mock_method=mock_method):
                        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])
                        mock_method.assert_called_once()

    @mock.patch('builtins.input', side_effect=['delete 10', 'quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch.object(debugger, 'print_usage_text')
    def test_deleteBreakpoint_invalid(self, mock_method: mock.patch.object, mock_stdout: StringIO, mock_input):
        '''
            Tests that the help instructions are printed when an invalid delete command is inputted.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])
        mock_method.assert_called_once()

    @mock.patch('builtins.input', side_effect=['continue', 'quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_cont(self, mock_stdout: StringIO, mock_input):
        '''
            Tests that if there are no breakpoints inputting continue will execute 
            the program to completion.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
10"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")

    @mock.patch('builtins.input', side_effect=[f'break {p.dirname(__file__)}/test.asm 17','continue', 'quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_cont_breakpoint(self, mock_stdout: StringIO, mock_input):
        '''
            Tests that if there is a breakpoint when inputting continue will execute 
            the program until it reaches the breakpoint.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
syscall 
 "{p.dirname(__file__)}/test.asm", 17
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")

    @mock.patch('builtins.input', side_effect=[f'print','quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch.object(debugger, 'print_usage_text')
    def test_print_invalid(self, mock_method: mock.patch.object, mock_stdout: StringIO, mock_input):
        '''
            Tests an error message along with the help instructions are printed when there is an invalid flag.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
Invalid usage of print.
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")
        mock_method.assert_called_once()

    @mock.patch('builtins.input', side_effect=[f'print 0','quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_print_flag(self, mock_stdout: StringIO, mock_input):
        '''
            Tests that the value of the flag is printed properly.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
The value of flag 0 is False
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")

    @mock.patch('builtins.input', side_effect=[f'print x','quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch.object(debugger, 'print_usage_text')
    def test_print_flag_invalid(self, mock_method: mock.patch.object, mock_stdout: StringIO, mock_input):
        '''
            Tests an error message along with the help instructions are printed when there is an invalid flag.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
x is not a valid flag.
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")
        mock_method.assert_called_once()

    @mock.patch('builtins.input', side_effect=[f'print 10','quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch.object(debugger, 'print_usage_text')
    def test_print_flag_invalid_integer(self, mock_method: mock.patch.object, mock_stdout: StringIO, mock_input):
        '''
            Tests an error message along with the help instructions are printed when there is an invalid flag.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
10 is not a valid flag.
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")
        mock_method.assert_called_once()

    @mock.patch('builtins.input', side_effect=['next', 'next', 'print $a0 i', 'print $a0 u', 'print $a0 x', 'print $a0 b', 'print $f1 f', 'print $f1 d', 'print $f2 d', 'quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_print_register(self, mock_stdout: StringIO, mock_input):
        '''
            Tests that print register prints the register value in the specified representation. In addition,
            checks that an error message is printed when trying to print a double from a non-even f-register.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
li $a0 10 (ori $a0, $0, 0x0000000a)
 "{p.dirname(__file__)}/test.asm", 15
li $v0 1 (ori $v0, $0, 0x00000001)
 "{p.dirname(__file__)}/test.asm", 16
$a0 10
li $v0 1 (ori $v0, $0, 0x00000001)
 "{p.dirname(__file__)}/test.asm", 16
$a0 10
li $v0 1 (ori $v0, $0, 0x00000001)
 "{p.dirname(__file__)}/test.asm", 16
$a0 0x0000000a
li $v0 1 (ori $v0, $0, 0x00000001)
 "{p.dirname(__file__)}/test.asm", 16
$a0 0b00000000000000000000000000001010
li $v0 1 (ori $v0, $0, 0x00000001)
 "{p.dirname(__file__)}/test.asm", 16
$f1 0.0
li $v0 1 (ori $v0, $0, 0x00000001)
 "{p.dirname(__file__)}/test.asm", 16
Not an even numbered register
li $v0 1 (ori $v0, $0, 0x00000001)
 "{p.dirname(__file__)}/test.asm", 16
$f2 0.0
li $v0 1 (ori $v0, $0, 0x00000001)
 "{p.dirname(__file__)}/test.asm", 16
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")

    @mock.patch('builtins.input', side_effect=['print string s', 'print array w 4 i', 'print array w 4 o', 'print half h 2 i', 'print byte b 1 i', 'print double d 1', 'print float f 1', 'print string c 2','quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch.object(debugger, 'print_usage_text')
    def test_print_memory(self, mock_method: mock.patch.object, mock_stdout: StringIO, mock_input):
        '''
            Tests that print memory prints the memory value the specified number of bytes in the specified 
            representation. In addition, check that the proper error message is printed when there are 
            invalid command is inputted.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
string hello
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
1
4
7
10
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
o is not a valid base.
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
-1
1
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
5
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
420.0
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
18.0
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
string
	h
	e
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")

    @mock.patch('builtins.input', side_effect=['print array w 0 i', 'print array w -2 i', 'print array u 4 i', 'print array w 4', 'print', 'print bad_label w 4 i','quit'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch.object(debugger, 'print_usage_text')
    def test_print_invalid(self, mock_method: mock.patch.object, mock_stdout: StringIO, mock_input):
        '''
            Tests the proper error message is printed when an invalid print command is inputted.
        '''
        self.assertRaises(SystemExit, sbumips.main, ["-d", f"{p.dirname(__file__)}/test.asm"])

        expected_output = f"""mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
0 is not a valid length.
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
-2 is not a valid length.
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
u is not a valid data type.
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
Invalid usage of print.
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
Invalid usage of print.
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
Invalid usage of print.
mul $t2, $t0, $t1 
 "{p.dirname(__file__)}/test.asm", 13
"""
        self.assertEqual(mock_stdout.getvalue(), expected_output, f"The expected output does not match.\n{mock_stdout.getvalue()}\n{expected_output}")