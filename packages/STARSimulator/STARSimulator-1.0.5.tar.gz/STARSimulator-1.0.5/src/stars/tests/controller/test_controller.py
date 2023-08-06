from threading import Event
import unittest
from unittest import mock

from controller import Controller
from interpreter.classes import Label
from interpreter.debugger import Debug
from interpreter.interpreter import Interpreter
from interpreter.memory import Memory
from interpreter.registers import Registers


class TestController(unittest.TestCase):

    def setUp(self):
        super().setUp()
        inter = Interpreter([Label('main')], [])
        self.controller = Controller(inter.debug, inter)

    def test_set_interpreter(self):
        '''
            Tests that the interpreter and debugger attributes are set properly.
        '''
        self.controller = Controller(None, None)
        inter = Interpreter([Label('main')], [])
        self.controller.set_interp(inter)

        self.assertEqual(self.controller.interp, inter,
                         f"The interpreter was not set correct.")
        self.assertEqual(self.controller.debug, inter.debug,
                         f"The debug object does not match the interpreter's debug object.")

    @mock.patch.object(Event, "clear")
    def test_set_pause_false(self, mock_method: mock.patch.object):
        '''
            Tests that calling set pause false will call Event.clear().
        '''
        self.controller.set_pause(False)
        mock_method.assert_called_once()

    @mock.patch.object(Event, "set")
    def test_set_pause_true(self, mock_method: mock.patch.object):
        '''
            Tests that calling set pause true will call Event.set().
        '''
        self.controller.set_pause(True)
        mock_method.assert_called_once()

    @mock.patch.object(Event, "set")
    def test_pause_false(self, mock_method: mock.patch.object):
        '''
            Tests that calling pause false will call Event.set().
        '''
        self.controller.pause(False)
        mock_method.assert_called_once()

    @mock.patch.object(Event, "clear")
    def test_pause_true(self, mock_method: mock.patch.object):
        '''
            Tests that calling pause true will call Event.clear().
        '''
        self.controller.pause(True)
        mock_method.assert_called_once()

    @mock.patch.object(Memory, "getByte")
    def test_get_byte(self, mock_method: mock.patch.object):
        '''
            Tests that calling getByte will call Memory.getByte().
        '''
        self.controller.get_byte(1)
        mock_method.assert_called_once()

    @mock.patch.object(Debug, "addBreakpoint")
    def test_add_breakpoint(self, mock_method: mock.patch.object):
        '''
            Tests that calling add_breakpoint will call Debug.addBreakpoint().
        '''
        self.controller.add_breakpoint(["list", "of", "strings"])
        mock_method.assert_called_once()

    @mock.patch.object(Debug, "removeBreakpoint")
    def test_remove_breakpoint(self, mock_method: mock.patch.object):
        '''
            Tests that calling remove_breakpoint will call Debug.removeBreakpoint().
        '''
        self.controller.remove_breakpoint(["list", "of", "strings"])
        mock_method.assert_called_once()

    @mock.patch.object(Debug, "reverse")
    def test_reverse(self, mock_method: mock.patch.object):
        '''
            Tests that calling reverse will call Debug.reverse().
        '''
        self.controller.reverse()
        mock_method.assert_called_once()

    def test_good(self):
        '''
            Tests that calling good will return True if interpreter is set.
        '''
        self.assertTrue(self.controller.good(),
                        "Interpreter should not be None.")
        self.controller = Controller(None, None)
        self.assertFalse(self.controller.good(), "Interpreter should be None.")

    def test_cont(self):
        '''
            Tests that calling cont will return the value of Debug's continueFlag attribute.
        '''
        self.assertEqual(self.controller.cont(), self.controller.debug.continueFlag,
                         "The return value does not match the value of Debug's continueFlag attribute.")

    def test_set_setting(self):
        '''
            Tests that setting the value of warnings from False to True modifies the settings 
            dictionary.
        '''
        from settings import settings
        self.controller.setSetting("warnings", True)
        self.assertTrue(
            settings['warnings'], "The warnings setting is not set to True from False.")
        settings["warnings"] = False

    def test_get_labels(self):
        '''
            Tests that calling get labels returns the labels of a blank interpreter. 
        '''
        labels = self.controller.get_labels()

        self.assertEqual(
            len(labels), 1, "The number of labels is not equal to 1.")
        self.assertIn('main', labels, "The only label in labels is main.")

    def test_get_instr_count(self):
        '''
            Tests that calling cont will return the value of Interpreter's instruction_count attribute.
        '''
        self.assertEqual(self.controller.get_instr_count(), self.controller.interp.instruction_count,
                         "The return value does not match the value of Interpreter's instruction_count attribute.")

    @mock.patch.object(Registers, "get_reg_word")
    def test_get_reg_word(self, mock_method: mock.patch.object):
        '''
            Tests that calling get_reg_word will call Debug.get_reg_word().
        '''
        self.controller.get_reg_word("$a0")
        mock_method.assert_called_once()
