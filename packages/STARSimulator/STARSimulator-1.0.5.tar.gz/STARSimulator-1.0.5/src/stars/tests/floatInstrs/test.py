from io import StringIO
import math
from os import path as p
import unittest
import unittest.mock as mock

from numpy import float32

from interpreter import instructions as instrs
from interpreter.registers import Registers
import sbumips

'''
https://github.com/sbustars/STARS

Copyright 2020 Kevin McDonnell, Jihu Mun, and Ian Peitzsch

Developed by Kevin McDonnell (ktm@cs.stonybrook.edu),
Jihu Mun (jihu1011@gmail.com),
and Ian Peitzsch (irpeitzsch@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


class FloatTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(FloatTest, self).__init__(*args, **kwargs)

    def execute_file(self, op, fd: str = "sys.stdout"):
        # Method to execute tests file by running the command line script
        with mock.patch(fd, new_callable=StringIO) as mock_stdout:
            sbumips.main(["--noGui", f'{p.dirname(__file__)}/{op}_test.asm'])
            output = mock_stdout.getvalue()
        return output

    def execute_test(self, op, expected_output):
        output = self.execute_file(op)
        self.assertEqual(expected_output, output)

    def execute_error_test(self, op, ex):
        output = self.execute_file(op, fd = "sys.stderr")
        self.assertIn(ex, output)

    # Arithmetic operations
    # Add
    # General case
    def test_add_general(self):
        reg = Registers()
        reg.set_register("$f0", float32(5.38))
        reg.set_register("$f1", float32(4.20))
        instrs.add_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertEqual(float32(9.58), ret)

    # Overflow
    def test_add_overflow(self):
        reg = Registers()
        reg.set_register("$f0", float32(3e38))
        reg.set_register("$f1", float32(3e38))
        instrs.add_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertEqual(float32('inf'), ret)

    # Nan
    def test_add_nan(self):
        reg = Registers()
        reg.set_register("$f0", float32('inf'))
        reg.set_register("$f1", float32('-inf'))
        instrs.add_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertTrue(math.isnan(ret))

    # Sub
    # General case
    def test_sub_general(self):
        reg = Registers()
        reg.set_register("$f0", float32(5.38))
        reg.set_register("$f1", float32(9.58))
        instrs.sub_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertEqual(float32(-4.20), ret)

    # Overflow
    def test_sub_overflow(self):
        reg = Registers()
        reg.set_register("$f0", float32(3e38))
        reg.set_register("$f1", float32(-3e38))
        instrs.sub_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertEqual(float32('inf'), ret)

    # Nan
    def test_sub_nan(self):
        reg = Registers()
        reg.set_register("$f0", float32('inf'))
        reg.set_register("$f1", float32('inf'))
        instrs.sub_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertTrue(math.isnan(ret))

    # Mul
    # General case
    def test_mul_general(self):
        reg = Registers()
        reg.set_register("$f0", float32(4.20))
        reg.set_register("$f1", float32(5.38))
        instrs.mul_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertEqual(float32(22.595999), ret)

    # Overflow
    def test_mul_overflow(self):
        reg = Registers()
        reg.set_register("$f0", float32(1e20))
        reg.set_register("$f1", float32(1e20))
        instrs.mul_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertEqual(float32('inf'), ret)

    # Nan
    def test_mul_nan(self):
        reg = Registers()
        reg.set_register("$f0", float32(0))
        reg.set_register("$f1", float32('inf'))
        instrs.mul_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertTrue(math.isnan(ret))

    # Div
    # Divide by 0
    def test_div_0_single(self):
        reg = Registers()
        reg.set_register("$f0", float32(4.0))
        reg.set_register("$f1", float32(0.0))
        instrs.div_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertEqual(float32('inf'), ret)

    def test_div_0_double(self):
        reg = Registers()
        reg.set_register("$f0", 4.0)
        reg.set_register("$f1", 0.0)
        instrs.div_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertEqual(float('inf'), ret)

    # 0 / 0
    def test_div_nan_single(self):
        reg = Registers()
        reg.set_register("$f0", float32(0.0))
        reg.set_register("$f1", float32(0.0))
        instrs.div_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertTrue(math.isnan(ret))

    def test_div_nan_double(self):
        reg = Registers()
        reg.set_register("$f0", 0.0)
        reg.set_register("$f1", 0.0)
        instrs.div_f("$f2", "$f0", "$f1", reg)
        ret = reg.get_register("$f2")
        self.assertTrue(math.isnan(ret))

    # Abs
    # General case
    def test_abs_general(self):
        reg = Registers()
        reg.set_register("$f0", float32(-4.20))
        instrs._abs("$f0", "$f0", reg)
        ret = reg.get_register("$f0")
        self.assertEqual(float32(4.20), ret)
        self.assertTrue(type(ret) is float32)

    # Infinity
    def test_abs_infinity(self):
        reg = Registers()
        reg.set_register("$f0", float32('-inf'))
        instrs._abs("$f0", "$f0", reg)
        ret = reg.get_register("$f0")
        self.assertEqual(float32('inf'), ret)
        self.assertTrue(type(ret) is float32)

    # Sqrt
    # General case
    def test_sqrt_general(self):
        reg = Registers()
        reg.set_register("$f0", float32(9.0))
        instrs.sqrt("$f0", "$f0", reg)
        ret = reg.get_register("$f0")
        self.assertEqual(float32(3.0), ret)
        self.assertTrue(type(ret) is float32)

    # Negative
    def test_sqrt_negative(self):
        reg = Registers()
        reg.set_register("$f0", float32(-9.0))
        instrs.sqrt("$f0", "$f0", reg)
        ret = reg.get_register("$f0")
        self.assertTrue(math.isnan(ret))
        self.assertTrue(type(ret) is float32)

    # Ceil (round, floor, trunc have pretty much the same functionality)
    def test_ceil(self):
        self.execute_test('ceil', '2 2147483647 2147483647')

    # Load single
    def test_load_single(self):
        self.execute_test('load_single', '420.42 inf nan')

    # Address not aligned
    def test_load_err_single(self):
        self.execute_error_test('load_single_error', 'MemoryAlignmentError')

    # Load double
    def test_load_double(self):
        self.execute_test('load_double', '420.42 nan')

    # Address not aligned
    def test_load_err_double(self):
        self.execute_error_test('load_double_error', 'MemoryAlignmentError')

    # Store single
    def test_store_single(self):
        self.execute_test('store_single', '420.42 nan')

    # Store double
    def test_store_double(self):
        self.execute_test('store_double', '420.42 nan')

    # Compare + Branch
    # General case
    def test_comp(self):
        self.execute_test('comp', '1')

    # Nan case
    def test_comp_nan(self):
        self.execute_test('comp_nan', '01')

    # Convert
    # To word
    def test_cvt_to_word(self):
        self.execute_test('cvt_to_word', '4 42')

    # From word
    def test_cvt_from_word(self):
        self.execute_test('cvt_from_word', '1337.0 1234567.0')

    # Move if (not) zero
    def test_move_zero(self):
        self.execute_test('move', '0.0 3.4')

    # Move conditional
    def test_move_conditional(self):
        self.execute_test('move_cond', '42 0')
