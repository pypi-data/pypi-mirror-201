import unittest

from numpy import float32

from interpreter.classes import Declaration, Label
from interpreter.exceptions import InvalidImmediate
from interpreter.interpreter import Interpreter
from interpreter.utility import align_address
from settings import settings

class TestSetData(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.inter = Interpreter([Label('main')], [])


    def test_ascii(self):
        '''
            Tests that an ascii declaration is properly added to the data section.
        '''
        name, data_type, data = "data", ".ascii", "AscII"
        starting_adress = self.inter.mem.dataPtr
        data_length = len(data)

        declaration = Declaration(name, data_type, f'"{data}"') # pad with quotation marks
        self.inter.set_data(declaration)

        data_pointer = self.inter.mem.dataPtr

        self.assertEqual(data_pointer, starting_adress+data_length, f"The data point was not incremented properly by {data_length}.")
        self.assertIn(name, self.inter.mem.labels, f"The label {name} was not all to the dictionary of labels.")
        self.assertEqual(self.inter.mem.getLabel(name), starting_adress, f"The label {name} does not contain the correct address.")
        self.assertEqual(self.inter.mem.getString(name, data_length), data, f"The value at the label {name} does not contain the correct data.")

        for i in range(data_length): # checks the characters byte by byte
            self.assertEqual(chr(self.inter.mem.getByte(starting_adress+i)), data[i], 
                f"The {i}-th character does not match the byte at address {starting_adress+i}.")

    def test_asciiz(self):
        '''
            Tests that an asciiz declaration is properly added to the data section.
        '''
        name, data_type, data = "data", ".asciiz", "AscIIz"
        starting_adress = self.inter.mem.dataPtr
        data_length = len(data)

        declaration = Declaration(name, data_type, f'"{data}"') # pad with quotation marks
        self.inter.set_data(declaration)

        data_pointer = self.inter.mem.dataPtr

        self.assertEqual(data_pointer, starting_adress+data_length+1, f"The data point was not incremented properly by {data_length}.")
        self.assertIn(name, self.inter.mem.labels, f"The label {name} was not all to the dictionary of labels.")
        self.assertEqual(self.inter.mem.getLabel(name), starting_adress, f"The label {name} does not contain the correct address.")
        self.assertEqual(self.inter.mem.getString(name), data, f"The value at the label {name} does not contain the correct data.")

        for i in range(data_length): # checks the characters byte by byte
            self.assertEqual(chr(self.inter.mem.getByte(starting_adress+i)), data[i], 
                f"The {i}-th character does not match the byte at address {starting_adress+i}.")

        self.assertEqual(self.inter.mem.getByte(starting_adress+data_length), 0, f"The string in memory is not null terminated.")

    def test_byte(self):
        '''
            Tests that a byte declaration is properly added to the data section.
        '''
        name, data_type, data = "data", ".byte", [1, ord('a'), 0xff, 0x3ff, 0x1]
        starting_adress = self.inter.mem.dataPtr
        data_length = len(data)

        declaration = Declaration(name, data_type, data) 
        self.inter.set_data(declaration)

        data_pointer = self.inter.mem.dataPtr

        self.assertEqual(data_pointer, starting_adress+data_length, f"The data point was not incremented properly by {data_length}.")
        self.assertIn(name, self.inter.mem.labels, f"The label {name} was not all to the dictionary of labels.")
        self.assertEqual(self.inter.mem.getLabel(name), starting_adress, f"The label {name} does not contain the correct address.")

        for i in range(data_length): # checks the characters byte by byte
            self.assertEqual(self.inter.mem.getByte(starting_adress+i, signed= False), data[i] & 0xff, 
                f"The {i}-th character does not match the byte at address {starting_adress+i}.")

    def test_double(self):
        '''
            Tests that a double declaration is properly added to the data section.
        '''
        name, data_type, data = "data", ".double", [420.42, 1.8733, -1.0]
        starting_adress = self.inter.mem.dataPtr
        data_length = len(data)

        declaration = Declaration(name, data_type, data) 
        self.inter.set_data(declaration)

        data_pointer = self.inter.mem.dataPtr

        self.assertEqual(data_pointer, starting_adress+data_length*8, f"The data point was not incremented properly by {data_length}.")
        self.assertIn(name, self.inter.mem.labels, f"The label {name} was not all to the dictionary of labels.")
        self.assertEqual(self.inter.mem.getLabel(name), starting_adress, f"The label {name} does not contain the correct address.")

        for i in range(data_length): # checks the characters byte by byte
            self.assertEqual(self.inter.mem.getDouble(starting_adress+i*8), data[i], 
                f"The {i}-th character does not match the byte at address {starting_adress+i}.")

    def test_float(self):
        '''
            Tests that a float declaration is properly added to the data section.
        '''
        name, data_type, data = "data", ".float", [420.42, 1.8733, -1.0]
        starting_adress = self.inter.mem.dataPtr
        data_length = len(data)

        declaration = Declaration(name, data_type, data) 
        self.inter.set_data(declaration)

        data_pointer = self.inter.mem.dataPtr

        self.assertEqual(data_pointer, starting_adress+data_length*4, f"The data point was not incremented properly by {data_length}.")
        self.assertIn(name, self.inter.mem.labels, f"The label {name} was not all to the dictionary of labels.")
        self.assertEqual(self.inter.mem.getLabel(name), starting_adress, f"The label {name} does not contain the correct address.")

        for i in range(data_length): # checks the characters byte by byte
            self.assertEqual(self.inter.mem.getFloat(starting_adress+i*4), float32(data[i]), 
                f"The {i}-th character does not match the byte at address {starting_adress+i}.")

    def test_half(self):
        '''
            Tests that a half declaration is properly added to the data section.
        '''
        name, data_type, data = "data", ".half", [1, ord('a'), 0xff, 0x3ff]
        starting_adress = self.inter.mem.dataPtr
        data_length = len(data)

        declaration = Declaration(name, data_type, data) 
        self.inter.set_data(declaration)

        data_pointer = self.inter.mem.dataPtr

        self.assertEqual(data_pointer, starting_adress+data_length*2, f"The data point was not incremented properly by {data_length}.")
        self.assertIn(name, self.inter.mem.labels, f"The label {name} was not all to the dictionary of labels.")
        self.assertEqual(self.inter.mem.getLabel(name), starting_adress, f"The label {name} does not contain the correct address.")

        for i in range(data_length): # checks the characters byte by byte
            self.assertEqual(self.inter.mem.getHWord(starting_adress+i*2, signed= False), data[i] & 0xFFFF, 
                f"The {i}-th character does not match the byte at address {starting_adress+i}.")

    def test_space(self):
        '''
            Tests that a space declaration is properly added to the data section.
        '''
        name, data_type, data = "data", ".space", 7
        starting_adress = self.inter.mem.dataPtr
        data_length = data

        declaration = Declaration(name, data_type, data) 
        self.inter.set_data(declaration)

        data_pointer = self.inter.mem.dataPtr

        self.assertEqual(data_pointer, starting_adress+data_length, f"The data point was not incremented properly by {data_length}.")
        self.assertIn(name, self.inter.mem.labels, f"The label {name} was not all to the dictionary of labels.")
        self.assertEqual(self.inter.mem.getLabel(name), starting_adress, f"The label {name} does not contain the correct address.")

        for i in range(data_length): # checks the characters byte by byte
            self.assertEqual(self.inter.mem.getByte(starting_adress+i, signed= False), 0, 
                f"The {i}-th character is not 0.")

        settings['garbage_memory'] = True
        name = "data2"
        starting_adress = data_pointer

        declaration = Declaration(name, data_type, data) 
        self.inter.set_data(declaration)

        data_pointer = self.inter.mem.dataPtr

        self.assertEqual(data_pointer, starting_adress+data_length, f"The data point was not incremented properly by {data_length}.")
        self.assertIn(name, self.inter.mem.labels, f"The label {name} was not all to the dictionary of labels.")
        self.assertEqual(self.inter.mem.getLabel(name), starting_adress, f"The label {name} does not contain the correct address.")

        for i in range(data_length): # checks the characters byte by byte
            value = self.inter.mem.getByte(starting_adress+i, signed= False)
            self.assertTrue(value >= 0 and value <= 0xFF, 
                f"The {i}-th character is not within the range [0, 0xFF].")

        settings['garbage_memory'] = False

    def test_word(self):
        '''
            Tests that a word declaration is properly added to the data section.
        '''
        name, data_type, data = "data", ".word", [1, 2, 3, 0xff]
        starting_adress = self.inter.mem.dataPtr
        data_length = len(data)

        declaration = Declaration(name, data_type, data) 
        self.inter.set_data(declaration)

        data_pointer = self.inter.mem.dataPtr

        self.assertEqual(data_pointer, starting_adress+data_length*4, f"The data point was not incremented properly by {data_length}.")
        self.assertIn(name, self.inter.mem.labels, f"The label {name} was not all to the dictionary of labels.")
        self.assertEqual(self.inter.mem.getLabel(name), starting_adress, f"The label {name} does not contain the correct address.")

        for i in range(data_length): # checks the characters byte by byte
            self.assertEqual(self.inter.mem.getWord(starting_adress+i*4), data[i] & 0xff, 
                f"The {i}-th character does not match the byte at address {starting_adress+i}.")


    def test_align(self):
        '''
            Tests that a align declaration with integers from 0 to 3, inclusive, is properly added to the data section.
        '''
        for i, alignment in enumerate([1, 2, 4, 8]):
            name, data_type, data = f"data{i}", ".align", i
            starting_adress = self.inter.mem.dataPtr

            declaration = Declaration(name, data_type, data) 
            self.inter.set_data(declaration)

            data_pointer = self.inter.mem.dataPtr

            self.assertEqual(data_pointer, align_address(starting_adress, alignment), f"The data point was not align at a {alignment} boundary.")
            self.assertIn(name, self.inter.mem.labels, f"The label {name} was not all to the dictionary of labels.")
            self.assertEqual(self.inter.mem.getLabel(name), starting_adress, f"The label {name} does not contain the correct address.")

    def test_align_invalid(self):
        '''
            Tests that a align declaration with an invalid argument raises and InvalidImmediate exception.
        '''
        invalid_values = [-1, 10]
        for i in invalid_values:
            name, data_type, data = f"data{i}", ".align", i

            declaration = Declaration(name, data_type, data) 
            self.assertRaises(InvalidImmediate, self.inter.set_data, declaration)

    def test_no_label(self):
        '''
            Tests that a declaration with no labels will not modify the dictionary of labels.
        '''
        data_type, data = ".ascii", "AscII"
        starting_adress = self.inter.mem.dataPtr
        data_length = len(data)
        number_of_labels = len(self.inter.mem.labels)

        declaration = Declaration(None, data_type, f'"{data}"') # pad with quotation marks
        self.inter.set_data(declaration)

        data_pointer = self.inter.mem.dataPtr

        self.assertEqual(data_pointer, starting_adress+data_length, f"The data point was not incremented properly by {data_length}.")
        self.assertEqual(len(self.inter.mem.labels), number_of_labels, f"The dictionary of labels was modified.")

        for i in range(data_length): # checks the characters byte by byte
            self.assertEqual(chr(self.inter.mem.getByte(starting_adress+i)), data[i], 
                f"The {i}-th character does not match the byte at address {starting_adress+i}.")

    def test_invalid_type(self):
        '''
            Tests that the memory is not modified if the data type is invalid.
        '''
        name, data_type, data = "data", ".string", "AscII"
        starting_adress = self.inter.mem.dataPtr
        number_of_labels = len(self.inter.mem.labels)

        declaration = Declaration(None, data_type, f'"{data}"') # pad with quotation marks
        self.inter.set_data(declaration)

        data_pointer = self.inter.mem.dataPtr

        self.assertEqual(data_pointer, starting_adress, f"The data point should not have been incremented.")
        self.assertEqual(len(self.inter.mem.labels), number_of_labels, f"The dictionary of labels was modified.")
    