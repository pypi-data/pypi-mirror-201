import struct
import unittest
import unittest.mock as mock
from io import StringIO
from tempfile import NamedTemporaryFile

from numpy import float32
from constants import WORD_SIZE

from interpreter import exceptions as ex
from interpreter import syscalls
from interpreter.classes import Label, Syscall
from interpreter.interpreter import Interpreter
from interpreter.memory import Memory
from interpreter.utility import align_address
from settings import settings

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

class TestSyscalls(unittest.TestCase):
    def setUp(self):
        ''' Creates an empty interpreter object. '''
        super().setUp()
        self.inter = Interpreter([Label('main')], [])

    # syscall 1 
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printInt(self, mock_stdout):
        syscall, input, output = 1, 0, str(0)

        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printNegInt(self, mock_stdout):
        syscall, input, output = 1, -1, str(-1)

        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printLargeInt(self, mock_stdout):
        syscall, input, output = 1, 0x7FFFFFFF, str(2147483647)

        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printLargeNegInt(self, mock_stdout):
        syscall, input, output = 1, 0x80000000, str(-2147483648)
        
        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    # syscall 2
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printFloat(self, mock_stdout):
        syscall, input, output = 2, float32(420.42), '420.42'
        
        self.inter.set_register("$f12", input)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printFloatBig(self, mock_stdout):
        syscall, input, output = 2, float32(42.0E17), '4.2e+18'
        
        self.inter.set_register("$f12", input)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printFloatInf(self, mock_stdout):
        syscall, input, output = 2, float32('inf'), 'inf'
        
        self.inter.set_register("$f12", input)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    # syscall 3
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printDouble(self, mock_stdout):
        syscall, input_one, input_two, output = 3, float32(1.26443839488E11), float32(3.9105663299560546875E0), '420.42'
        
        self.inter.set_register("$f12", input_one)
        self.inter.set_register("$f13", input_two)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printDoubleBig(self, mock_stdout):
        syscall, input_one, input_two, output = 3, float32(-2.4833974245227757568E19), float32(4.1028668212890625E2), '4.2e+18'
        
        self.inter.set_register("$f12", input_one)
        self.inter.set_register("$f13", input_two)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printDoubleInf(self, mock_stdout):
        syscall, input_one, input_two, output = 3, float32(0), struct.unpack('>f', struct.pack('>i', 0x7FF00000))[0], 'inf'
        
        self.inter.set_register("$f12", input_one)
        self.inter.set_register("$f13", input_two)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    # syscall 4
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printString(self, mock_stdout):
        syscall, input, output = 4, self.inter.mem.dataPtr, 'words'
        
        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        self.inter.mem.addAsciiz('words', input)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printInvalidString(self, mock_stdout):
        syscall, input = 4, self.inter.mem.dataPtr
        
        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)

        self.inter.mem.addAscii('words', input)
        self.inter.mem.dataPtr += 5
        self.inter.mem.addByte(255, self.inter.mem.dataPtr)
        self.inter.mem.dataPtr += 1
        self.inter.mem.addAsciiz('words', self.inter.mem.dataPtr)
        self.assertRaises(ex.InvalidCharacter, self.inter.execute_instr, Syscall())

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printInvalidString2(self, mock_stdout):
        syscall, input = 4, self.inter.mem.dataPtr
        
        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)

        self.inter.mem.addAscii('words', input)
        self.inter.mem.dataPtr += 5
        self.inter.mem.addByte(8, self.inter.mem.dataPtr)
        self.inter.mem.dataPtr += 1
        self.inter.mem.addAsciiz('words', self.inter.mem.dataPtr)
        self.assertRaises(ex.InvalidCharacter, self.inter.execute_instr, Syscall())


    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printEmptyString(self, mock_stdout):
        syscall, input, output = 4, self.inter.mem.dataPtr, ''
        
        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        self.inter.mem.addByte(0, input)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    # sycall 5
    @mock.patch('builtins.input', side_effect=['0'])
    def test_readInt(self, input):
        syscall, output = 5, 0
        
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(self.inter.get_register('$v0'), output)

    @mock.patch('builtins.input', side_effect=['-1'])
    def test_readNegInt(self, input):
        syscall, output = 5, -1
        
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(self.inter.get_register('$v0'), output)

    @mock.patch('builtins.input', side_effect=['A'])
    def test_readInvalidInt(self, input):
        syscall = 5
        
        self.inter.set_register("$v0", syscall)
        self.assertRaises(ex.InvalidInput, self.inter.execute_instr, Syscall())

    # syscall 6
    def test_atoi(self):
        syscall, input, output = 6, '02113', 2113

        self.inter.set_register('$a0', self.inter.mem.dataPtr)
        self.inter.set_register("$v0", syscall)
        self.inter.mem.addAsciiz(input, self.inter.mem.dataPtr)
        self.inter.execute_instr(Syscall())
        self.assertEqual(self.inter.reg.get_register('$v0'), output)

    def test_atoi_zero(self):
        syscall, input, output = 6, '0', 0

        self.inter.set_register('$a0', self.inter.mem.dataPtr)
        self.inter.set_register("$v0", syscall)
        self.inter.mem.addAsciiz(input, self.inter.mem.dataPtr)
        self.inter.execute_instr(Syscall())
        self.assertEqual(self.inter.reg.get_register('$v0'), output)

    def test_atoi_neg(self):
        syscall, input, output = 6, '-12345', -12345

        self.inter.set_register('$a0', self.inter.mem.dataPtr)
        self.inter.set_register("$v0", syscall)
        self.inter.mem.addAsciiz(input, self.inter.mem.dataPtr)
        self.inter.execute_instr(Syscall())
        self.assertEqual(self.inter.reg.get_register('$v0'), output)
        
    def test_atoi_bad1(self):
        syscall, input = 6, '--12345'

        self.inter.set_register('$a0', self.inter.mem.dataPtr)
        self.inter.set_register("$v0", syscall)
        self.inter.mem.addAsciiz(input, self.inter.mem.dataPtr)
        self.assertRaises(ex.InvalidCharacter, self.inter.execute_instr, Syscall())

    def test_atoi_bad2(self):
        syscall, input = 6, '123e45'

        self.inter.set_register('$a0', self.inter.mem.dataPtr)
        self.inter.set_register("$v0", syscall)
        self.inter.mem.addAsciiz(input, self.inter.mem.dataPtr)
        self.assertRaises(ex.InvalidCharacter, self.inter.execute_instr, Syscall())

    def test_atoi_bad_empty(self):
        syscall, input = 6, ''

        self.inter.set_register('$a0', self.inter.mem.dataPtr)
        self.inter.set_register("$v0", syscall)
        self.inter.mem.addAsciiz(input, self.inter.mem.dataPtr)
        self.assertRaises(ex.InvalidCharacter, self.inter.execute_instr, Syscall())

    # syscall 8
    @mock.patch('builtins.input', side_effect=['uwu'])
    def test_readString(self, input):
        syscall, length, output = 8, 3, 'uwu'
        
        self.inter.set_register("$a0", self.inter.mem.dataPtr)
        self.inter.set_register("$a1", length)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        string = syscalls.getString(self.inter.mem.dataPtr, self.inter.mem, num_chars=length)
        self.assertEqual(string, output)

    @mock.patch('builtins.input', side_effect=['uwu uwu'])
    def test_underReadString(self, input):
        syscall, length, output = 8, 3, 'uwu'
        
        self.inter.set_register("$a0", self.inter.mem.dataPtr)
        self.inter.set_register("$a1", length)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        string = syscalls.getString(self.inter.mem.dataPtr, self.inter.mem, num_chars=length)
        self.assertEqual(string, output)

    @mock.patch('builtins.input', side_effect=['uwu uwu'])
    def test_overReadString(self, input):
        syscall, length, output = 8, 9, 'uwu uwu'
        
        self.inter.set_register("$a0", self.inter.mem.dataPtr)
        self.inter.set_register("$a1", length)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        string = syscalls.getString(self.inter.mem.dataPtr, self.inter.mem, num_chars=length)
        self.assertEqual(string, output)

    @mock.patch('builtins.input', side_effect=[str(chr(0xFF))])
    def test_readWeirdString(self, input):
        syscall, length, output = 8, 9, str(chr(0xFF))
        
        self.inter.set_register("$a0", self.inter.mem.dataPtr)
        self.inter.set_register("$a1", length)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        string = self.inter.mem.getByte(self.inter.mem.dataPtr, signed=False)
        self.assertEqual(str(chr(string)), output)

    # syscall 9
    def test_sbrk(self):
        syscall, input = 9, 5
        
        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        out = self.inter.mem.heapPtr
        self.inter.execute_instr(Syscall())
        self.assertEqual(self.inter.get_register('$v0'), out)
        self.assertEqual(self.inter.mem.heapPtr, align_address(out+input, 4))

    def test_Negsbrk(self):
        syscall, input = 9, -1
        
        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        self.assertRaises(ex.InvalidArgument, self.inter.execute_instr, Syscall())

    def test_Negsbrk2(self):
        syscall, input = 9, 0xFFFFFFFF
        
        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        self.assertRaises(ex.InvalidArgument, self.inter.execute_instr, Syscall())

    def test_0sbrk(self):
        syscall, input = 9, 0
        
        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        out = self.inter.mem.heapPtr
        self.inter.execute_instr(Syscall())
        self.assertEqual(self.inter.get_register('$v0'), out)
        self.assertEqual(self.inter.mem.heapPtr, align_address(out+input, 4))

    def test_Maxsbrk(self):
        syscall, input = 9, settings['initial_$sp'] - self.inter.mem.heapPtr
        
        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        out = self.inter.mem.heapPtr
        self.inter.execute_instr(Syscall())
        self.assertEqual(self.inter.get_register('$v0'), out)
        self.assertEqual(self.inter.mem.heapPtr, align_address(out+input, 4))

    def test_MaxsbrkExceeded(self):
        syscall, input = 9, settings['initial_$sp'] - self.inter.mem.heapPtr 
        
        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        out = self.inter.mem.heapPtr
        self.inter.execute_instr(Syscall())
        self.assertEqual(self.inter.get_register('$v0'), out)
        self.assertEqual(self.inter.mem.heapPtr, align_address(out+input, 4))

        self.inter.set_register("$a0", 4)
        self.inter.set_register("$v0", syscall)
        self.assertRaises(ex.MemoryOutOfBounds, self.inter.execute_instr, Syscall())

    # syscall 10/17 
    def test_exit(self):
        syscall_values = [10, 17] 

        for syscall in syscall_values:
            self.inter.set_register("$v0", syscall)
            self.assertRaises(SystemExit, self.inter.execute_instr, Syscall())

    def test_exit_instruction(self):
        settings['disp_instr_count'] = True
        syscall_values = [10, 17] 

        for syscall in syscall_values:
            with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with self.subTest(syscall=syscall, mock_stdout=mock_stdout):
                    self.inter.set_register("$v0", syscall)
                    self.assertRaises(SystemExit, self.inter.execute_instr, Syscall())
                    self.assertIn("\nInstruction count: ", mock_stdout.getvalue())

        settings['disp_instr_count'] = False

    # syscall 11
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printChar(self, mock_stdout):
        syscall, input, output = 11, ord('A'), 'A'

        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        self.assertEqual(mock_stdout.getvalue(), output)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printInvalidChar(self, mock_stdout):
        syscall, input = 11, 8

        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        self.assertRaises(ex.InvalidCharacter, self.inter.execute_instr, Syscall())

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printInvalidChar2(self, mock_stdout):
        syscall, input = 11, 255

        self.inter.set_register("$a0", input)
        self.inter.set_register("$v0", syscall)
        self.assertRaises(ex.InvalidCharacter, self.inter.execute_instr, Syscall())

    # syscall 30
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_dumpMem(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.mem.addAsciiz('uwu hewwo worwd >.<', inter.mem.dataPtr)
        inter.reg.reg = {'$a0': inter.mem.dataPtr, '$a1': inter.mem.dataPtr + 12}
        syscalls.memDump(inter)
        self.assertEqual('''addr        hex             ascii       
0x10010000  20  75  77  75     u  w  u  
0x10010004  77  77  65  68  w  w  e  h  
0x10010008  6f  77  20  6f  o  w     o  
''', mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_dumpMemBadChar(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.mem.addAsciiz('uwu hew' + str(chr(255)) + 'o worwd >.<', inter.mem.dataPtr)
        inter.reg.reg = {'$a0': inter.mem.dataPtr, '$a1': inter.mem.dataPtr + 12}
        syscalls.memDump(inter)
        self.assertEqual('''addr        hex             ascii       
0x10010000  20  75  77  75     u  w  u  
0x10010004  ff  77  65  68  .  w  e  h  
0x10010008  6f  77  20  6f  o  w     o  
''', mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_dumpMemBadChar2(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.mem.addAsciiz('uwu hew' + str(chr(20)) + 'o worwd >.<', inter.mem.dataPtr)
        inter.reg.reg = {'$a0': inter.mem.dataPtr, '$a1': inter.mem.dataPtr + 12}
        syscalls.memDump(inter)
        self.assertEqual('''addr        hex             ascii       
0x10010000  20  75  77  75     u  w  u  
0x10010004  14  77  65  68  .  w  e  h  
0x10010008  6f  77  20  6f  o  w     o  
''', mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_dumpMemNull(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.mem.addAsciiz('uwu hew' + str(chr(0)) + 'o worwd >.<', inter.mem.dataPtr)
        inter.reg.reg = {'$a0': inter.mem.dataPtr, '$a1': inter.mem.dataPtr + 12}
        syscalls.memDump(inter)
        self.assertEqual('''addr        hex             ascii       
0x10010000  20  75  77  75     u  w  u  
0x10010004  00  77  65  68  \\0 w  e  h  
0x10010008  6f  77  20  6f  o  w     o  
''', mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_dumpMemTab(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.mem.addAsciiz('uwu hew' + str(chr(9)) + 'o worwd >.<', inter.mem.dataPtr)
        inter.reg.reg = {'$a0': inter.mem.dataPtr, '$a1': inter.mem.dataPtr + 12}
        syscalls.memDump(inter)
        self.assertEqual('''addr        hex             ascii       
0x10010000  20  75  77  75     u  w  u  
0x10010004  09  77  65  68  \\t w  e  h  
0x10010008  6f  77  20  6f  o  w     o  
''', mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_dumpMemNewline(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.mem.addAsciiz('uwu hew' + str(chr(10)) + 'o worwd >.<', inter.mem.dataPtr)
        inter.reg.reg = {'$a0': inter.mem.dataPtr, '$a1': inter.mem.dataPtr + 12}
        syscalls.memDump(inter)
        self.assertEqual('''addr        hex             ascii       
0x10010000  20  75  77  75     u  w  u  
0x10010004  0a  77  65  68  \\n w  e  h  
0x10010008  6f  77  20  6f  o  w     o  
''', mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_dumpMemRound(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.mem.addAsciiz('uwu hewwo worwd >.<', inter.mem.dataPtr)
        inter.reg.reg = {'$a0': inter.mem.dataPtr, '$a1': inter.mem.dataPtr + 10}
        syscalls.memDump(inter)
        self.assertEqual('''addr        hex             ascii       
0x10010000  20  75  77  75     u  w  u  
0x10010004  77  77  65  68  w  w  e  h  
0x10010008  6f  77  20  6f  o  w     o  
''', mock_stdout.getvalue())

    # syscall 31
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_dumpReg(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': 0}
        syscalls.regDump(inter)
        self.assertEqual('''reg  hex        dec
$a0  0x00000000 0
''', mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_dumpRegNeg(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': 0x80000000}
        syscalls.regDump(inter)
        self.assertEqual('''reg  hex        dec
$a0  0x80000000 -2147483648
''', mock_stdout.getvalue())

    # syscall 32
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_dumpFiles(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg = {}
        with NamedTemporaryFile(delete=True) as f:
            name = f.name
            inter.mem.fileTable[3] = f
            syscalls.dumpFiles(inter)
        self.assertEqual(f'''0	stdin
1	stdinter.out
2	stderr
3	{name}
''', mock_stdout.getvalue())

    # syscall 34
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printHex(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': 0}
        syscalls.printHex(inter)
        self.assertEqual(mock_stdout.getvalue(), '0x00000000')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printNegHex(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': -1}
        syscalls.printHex(inter)
        self.assertEqual(mock_stdout.getvalue(), '0xffffffff')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printLargeHex(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': 0x7FFFFFFF}
        syscalls.printHex(inter)
        self.assertEqual(mock_stdout.getvalue(), '0x7fffffff')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printLargeNegHex(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': -2147483648}
        syscalls.printHex(inter)
        self.assertEqual(mock_stdout.getvalue(), '0x80000000')

    # syscall 35
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printBin(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': 0}
        syscalls.printBin(inter)
        self.assertEqual(mock_stdout.getvalue(), '0b00000000000000000000000000000000')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printNegBin(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': -1}
        syscalls.printBin(inter)
        self.assertEqual(mock_stdout.getvalue(), '0b11111111111111111111111111111111')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printLargeBin(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': 0x7FFFFFFF}
        syscalls.printBin(inter)
        self.assertEqual(mock_stdout.getvalue(), '0b01111111111111111111111111111111')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printLargeNegBin(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': -2147483648}
        syscalls.printBin(inter)
        self.assertEqual(mock_stdout.getvalue(), '0b10000000000000000000000000000000')

    # syscall 36
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printUInt(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': 0}
        syscalls.printUnsignedInt(inter)
        self.assertEqual(mock_stdout.getvalue(), str(0))

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printNegval(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': -1}
        syscalls.printUnsignedInt(inter)
        self.assertEqual(mock_stdout.getvalue(), str(0xffffffff))

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printLargeUInt(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': 0x7FFFFFFF}
        syscalls.printUnsignedInt(inter)
        self.assertEqual(mock_stdout.getvalue(), str(0x7fffffff))

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_printLargeNegUInt(self, mock_stdout):
        inter = Interpreter([Label('main')], [])
        inter.mem = Memory()
        inter.reg.reg = {'$a0': -2147483648}
        syscalls.printUnsignedInt(inter)
        self.assertEqual(mock_stdout.getvalue(), str(0x80000000))

    # syscall 40/41/42
    def test_randInt(self):
        '''
            Tests that the random integer returned by syscall 41 is an 8 byte integer.
        '''
        self.inter.set_register("$v0", 41)
        self.inter.execute_instr(Syscall())
        value = self.inter.get_register("$v0")
        
        self.assertTrue(value >= -WORD_SIZE/2 and value < WORD_SIZE/2, f"Random int {value} is not within the bounds [2**31, 2**32).")

    def test_seed(self):
        '''
            Tests that the seed is set appropriate when syscall 40 is set. The int requested immediately after setting
            seed will always be the same.
        '''
        seed = 1
        self.inter.set_register("$a0", seed)
        self.inter.set_register("$v0", 40)
        self.inter.execute_instr(Syscall()) # set seed

        self.inter.set_register("$v0", 41)
        self.inter.execute_instr(Syscall())
        first = self.inter.get_register("$v0") # get int returned 

        self.inter.set_register("$a0", seed)
        self.inter.set_register("$v0", 40)
        self.inter.execute_instr(Syscall()) # reset seed

        self.inter.set_register("$v0", 41)
        self.inter.execute_instr(Syscall())
        second = self.inter.get_register("$v0") # get int returned (should be equal to first)      

        self.assertEqual(first, second, 
            f"The seed was not set properly. The first value ({first}) is not equal to the second value ({second}).")

    def test_random_int_range(self):
        '''
            Tests that the value return by random int range is within the range [0, 10] when 
            the upper bound is set to 10.
        '''
        self.inter.set_register("$a1", 10)
        self.inter.set_register("$v0", 42)
        self.inter.execute_instr(Syscall())
        value = self.inter.get_register("$v0") 
        
        self.assertTrue(value >= 0 and value <= 10, f"The value ({value}) returned is not in the range [0, 10]")

    def test_random_int_range_negative(self):
        '''
            Tests that an InvalidArgument exception is raised when the upper bound is a negative number.
        '''
        self.inter.set_register("$a1", -10)
        self.inter.set_register("$v0", 42)
        self.assertRaises(ex.InvalidArgument, self.inter.execute_instr, Syscall())