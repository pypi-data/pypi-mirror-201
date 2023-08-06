from io import StringIO
from os import path as p
from tempfile import NamedTemporaryFile
import unittest
import unittest.mock as mock

from gui import mainwindow
from interpreter.classes import IType, Label, Syscall
import sbumips


class TestSbumips(unittest.TestCase):

    @mock.patch.object(mainwindow, "launch_gui")
    def test_no_args(self, mock_method: mock.patch.object):
        '''
            Tests the program with no arguments. The intended effect is the GUI is started with 
            a function call to launch_gui.
        '''
        sbumips.main([])
        mock_method.assert_called_once()

    @mock.patch.object(sbumips, "run_CLI")
    def test_no_gui(self, mock_method: mock.patch.object):
        '''
            Tests the program with the --noGui option. The intended effect is the program arguments
            are processed with a function call to run_CLI.
        '''
        sbumips.main(["--noGui", "testfile.asm"])
        mock_method.assert_called_once()

    def test_invalid_assemble(self):
        '''
            Tests if assemble returns FileNotFoundError if the main file is invalid.
        '''
        self.assertRaises(FileNotFoundError, sbumips.assemble,
                          f"{p.dirname(__file__)}/testfile.asm")

    def test_assemble(self):
        '''
            Tests if assemble returns the correct list of classes.
        '''
        intended_result = [
            Label("main"),
            IType("addi", ["$v0", "$0"], 1),
            IType("addi", ["$a0", "$0"], 1),
            Syscall(),
        ]

        result = sbumips.assemble(f"{p.dirname(__file__)}/test.asm")

        self.assertEqual(len(intended_result), len(result),
                         "The number of classes are not equal.")

        for expected, actual in zip(intended_result, result):
            self.assertEqual(str(expected), str(actual),
                             "The lines are not equal.")

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_assemble_only(self, mock_stdout: StringIO):
        '''
            Tests if assemble correctly prints and exits if ran the -a option"
        '''
        from settings import settings
        settings['assemble'] = True

        self.assertRaises(SystemExit, sbumips.assemble,
                          f"{p.dirname(__file__)}/test.asm")
        self.assertEqual(mock_stdout.getvalue(), "Program assembled successfully.\n",
                         "Program did not assembled successfully.")

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_run_cli(self, mock_stdout: StringIO):
        '''
            Tests the program with the --noGui and -i option. The intended effect is the program 
            is executed and the asssembly file output along with the instruction count is printed 
            out.
        '''
        sbumips.main(["--noGui", "-i", f"{p.dirname(__file__)}/test.asm"])
        program_output, instruction_count = mock_stdout.getvalue().split("\n")
        self.assertEqual(program_output, "1", "Incorrect output.")
        self.assertEqual(instruction_count, "Instruction count: 3",
                         "Incorrect Instruction count.")

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_run_cli_error(self, mock_stderr: StringIO):
        '''
            Tests the program with an invalid file without the GUI. The intended effect is the 
            program prints out a FileNotFoundError to stderr and exits.
        '''
        sbumips.main(["--noGui", "-i", f"{p.dirname(__file__)}/testfile.asm"])
        self.assertEqual(mock_stderr.getvalue(),
                         f"FileNotFoundError: [Errno 2] No such file or directory: '{p.dirname(__file__)}/testfile.asm'\n",
                         "Program did not return a print out of FileNotFoundError")

    def test_run_cli_assemble(self):
        '''
            Tests that all declarations and instructions are assemble and recognized 
            by the lexer and parser.
        '''
        arguments = ["--noGui", f"{p.dirname(__file__)}/instructions.asm"]
        args = sbumips.init_args(arguments)
        sbumips.init_settings(args)
        pArgs = args.pa if args.pa else []
        result = sbumips.assemble(args.filename)
        inter = sbumips.Interpreter(result, pArgs)
