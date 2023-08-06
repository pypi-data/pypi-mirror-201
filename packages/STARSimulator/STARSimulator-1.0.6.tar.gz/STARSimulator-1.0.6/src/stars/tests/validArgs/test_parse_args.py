from io import StringIO
import unittest
import unittest.mock as mock

from sbumips import init_args, init_settings
from settings import settings

class TestParseArgs(unittest.TestCase):

    def test_no_arg(self):
        '''
            Tests the program with no arguments. The intended effect is the GUI is started with 
            the debug setting set True and all other settings to False. The argument parser should 
            have all boolean values be False.
        '''
        arguments = []
        args = init_args(arguments)

        values = [args.assemble, args.debug, args.garbage, args.disp_instr_count, args.warnings, args.noGui]
        for i, value in enumerate(values):
            self.assertFalse(value, f"All arguments should be False by default.")

        init_settings(args)
        CL_settings = ["assemble", "garbage_memory", "garbage_registers", "disp_instr_count", "warnings"]

        for value in CL_settings:
            self.assertFalse(settings[value], f"Setting {value} should be False by default.")

        CL_settings_modified = ["debug", "gui"]
        for value in CL_settings_modified:
            self.assertTrue(settings[value], f"Setting {value} should be True by default.")

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_invalid_arg(self, mock_stderr: StringIO):
        '''
            Tests the argument parser with an invalid long argument. The intended effect is the 
            program exits and an error message is outputted to stderr.
        '''
        arguments = ["-e", "testfile.asm"]
        self.assertRaises(SystemExit, init_args, arguments)
        self.assertIn("error: unrecognized arguments: -e", 
                mock_stderr.getvalue(), "Incorrect Error Message from argparse")
            
    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_invalid_arg(self, mock_stderr: StringIO):
        '''
            Tests the argument parser with an invalid long argument. The intended effect is the 
            program exits and an error message is outputted to stderr.
        '''
        arguments = ["--e", "testfile.asm"]
        self.assertRaises(SystemExit, init_args, arguments)
        self.assertIn("error: unrecognized arguments: --e", 
                mock_stderr.getvalue(), "Incorrect Error Message from argparse")

    def test_one_arg(self):
        '''
           Tests the argument parser with one argument. The argument parser reads the argument
           as the filename.
        '''
        arguments = ["testfile.asm"]
        args = init_args(arguments)

        self.assertEqual(args.filename, arguments[0], "Filename does not match.")

    def test_boolean_short_args(self):
        '''
           Tests the argument parser with all the boolean short argument options. The argument 
           parser sets all boolean arguments as True. The command line settings corresponding to
           these arguments are set to True. 
        '''
        arguments = ["-a", "-d", "-g", "-i", "-w", "testfile.asm"]
        args = init_args(arguments)
        
        self.assertEqual(args.filename, arguments[-1], "Filename does not match.")

        values = [args.assemble, args.debug, args.garbage, args.disp_instr_count, args.warnings]
        for i, value in enumerate(values):
            self.assertTrue(value, f"Argument {arguments[i]} is not recognized.")

        init_settings(args)
        CL_settings = ["assemble", "debug", ("garbage_memory", "garbage_registers"), "disp_instr_count", "warnings"]

        for value in CL_settings:
            if len(value) == 2:
                self.assertTrue(settings[value[0]], f"Argument {value[0]} should be set True.")
                value = value[1]
            self.assertTrue(settings[value], f"Argument {value} should be set True.")

    def test_boolean_long_args(self):
        '''
           Tests the argument parser with all the boolean long argument options except --noGui. 
           The argument parser sets all boolean arguments as True. The command line settings corresponding to
           these arguments are set to True. 
        '''
        arguments = ["--assemble", "--debug", "--garbage", "--disp_instr_count", "--warnings", "testfile.asm"]
        args = init_args(arguments)
        
        self.assertEqual(args.filename, arguments[-1], "Filename does not match.")

        values = [args.assemble, args.debug, args.garbage, args.disp_instr_count, args.warnings]
        for i, value in enumerate(values):
            self.assertTrue(value, f"Argument {arguments[i]} is not recognized.")

        init_settings(args)
        CL_settings = ["assemble", "debug", ("garbage_memory", "garbage_registers"), "disp_instr_count", "warnings"]

        for value in CL_settings:
            if len(value) == 2:
                self.assertTrue(settings[value[0]], f"Argument {value[0]} should be set True.")
                value = value[1]
            self.assertTrue(settings[value], f"Argument {value} should be set True.")

    def test_mix_args(self):
        '''
           Tests the argument parser with a short option (-d) and a long option (--assemble). 
           The argument parser sets assemble and debug to True. The command line settings 
           corresponding tothese arguments are set to True. The rest of the command line 
           arguments are False.
        '''
        arguments = ["--assemble", "-d", "testfile.asm"]
        args = init_args(arguments)
        
        self.assertEqual(args.filename, arguments[-1], "Filename does not match.")

        values = [args.assemble, args.debug]
        for i, value in enumerate(values):
                self.assertTrue(value, f"Argument {arguments[i]} is not recognized.")

        init_settings(args)
        CL_settings = ["assemble", "debug", "garbage_memory", "garbage_registers", "disp_instr_count", "warnings"]

        for i, value in enumerate(CL_settings):
            if i < len(arguments)-1:
                self.assertTrue(settings[value], f"Setting {value} is not recognized.")
            else:
                self.assertFalse(settings[value], f"Setting {value} is modified.")

    def test_required_filename(self):
        '''
            Tests the argument parser with one of the following: --noGui, -a/--asssemble, 
            -d/--debug. The argument parser requires a filename.
        '''
        options = ["--noGui", "-a", "--assemble", "-d", "--debug"]

        for option in options:
            with mock.patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with self.subTest(option=option):                
                    self.assertRaises(SystemExit, init_args, [option])
                    self.assertIn("error: the following arguments are required: filename", 
                            mock_stderr.getvalue(), "Incorrect Error Message from argparse")

    def test_max_instructions(self):
        '''
            Tests the argument parser with -n/--max_instructions. The argument parser 
            reads next argument as a integer input and sets the max_instructions setting to be
            the read input.
        '''
        options = ["-n", "--max_instructions"]

        for option in options:
            with self.subTest(option=option):     
                args = init_args([option, "10000", "filename.asm"])
                init_settings(args)

                self.assertEqual(args.max_instructions, 10000, 
                        "Argument parser set to the incorrect max instruction.")
                self.assertEqual(settings['max_instructions'], 10000, 
                        "Max instruction setting set to the incorrect max instruction.")
