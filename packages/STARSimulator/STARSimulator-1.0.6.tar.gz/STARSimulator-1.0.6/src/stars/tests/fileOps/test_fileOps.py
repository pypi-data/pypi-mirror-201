import unittest
from os import path as p

from interpreter.classes import Label, Syscall
from interpreter.interpreter import Interpreter
from interpreter.syscalls import getString

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


class TestFileOps(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.file = p.abspath(f"{p.dirname(__file__)}/fileToOpen.txt")
        self.out_file = p.abspath(f"{p.dirname(__file__)}/fileToWrite.txt")

    def setUp(self):
        super().setUp()
        self.inter = Interpreter([Label('main')], [])

    # file operations
    def test_file_open_success(self):
        '''
            Tests that a file was open sucessfully with the fd returned in $v0 being 3 and the number of file descriptors 
            in the file table being 4.
        '''
        addr = self.inter.mem.dataPtr
        syscall, mode = 13, 0
        output, fileTable_length = 3, 4 

        self.inter.mem.addAsciiz(self.file, addr)
        self.inter.set_register("$a0", addr)
        self.inter.set_register("$a1", mode)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        fd = self.inter.get_register("$v0")
        fileTable = self.inter.mem.fileTable

        self.assertEqual(fd, output, "Valid file was not opened.")
        self.assertEqual(len(fileTable), fileTable_length, f"The opened file descriptor ({fd}) was not added to the file table.")
        fileTable[3].close()

    def test_file_open_nonexistent(self):
        '''
            Tests that opening an invalid filename in read mode returns a file descriptor of -1 in $v0 and the size of the
            file table remaining the same (3).
        '''
        addr = self.inter.mem.dataPtr
        syscall, mode, invalid_file = 13, 0, 'file2Open.txt'
        output, fileTable_length = -1, 3 

        self.inter.mem.addAsciiz(invalid_file, addr)
        self.inter.set_register("$a0", addr)
        self.inter.set_register("$a1", mode)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        fd = self.inter.get_register("$v0")
        fileTable = self.inter.mem.fileTable

        self.assertEqual(fd, output, "The invalid file was opened.")
        self.assertEqual(len(fileTable), fileTable_length, "The opened invalid file was added to the file table.")

    def test_file_open_invalid_char(self):
        '''
            Tests that opening an invalid filename in write mode returns a file descriptor of -1 in $v0 and the size of the
            file table remaining the same (3).
        '''
        addr = self.inter.mem.dataPtr
        syscall, mode, invalid_file = 13, 1, f'file{chr(127)}Open.txt'
        output, fileTable_length = -1, 3 

        self.inter.mem.addAsciiz(invalid_file, addr)
        self.inter.set_register("$a0", addr)
        self.inter.set_register("$a1", mode)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        fd = self.inter.get_register("$v0")
        fileTable = self.inter.mem.fileTable

        self.assertEqual(fd, output, "A file with an invalid filename was created.")
        self.assertEqual(len(fileTable), fileTable_length, "The opened invalid file was added to the file table.")

    def test_open_file_invalid_mode(self):
        '''
            Tests that opening a file with invalid mode returns a file descriptor of -1 in $v0 and the size of the
            file table remaining the same (3).
        '''
        addr = self.inter.mem.dataPtr
        syscall, mode = 13, 2
        output, fileTable_length = -1, 3 

        self.inter.mem.addAsciiz(self.file, addr)
        self.inter.set_register("$a0", addr)
        self.inter.set_register("$a1", mode)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        fd = self.inter.get_register("$v0")
        fileTable = self.inter.mem.fileTable

        self.assertEqual(fd, output, "The file was opened with an invalid mode.")
        self.assertEqual(len(fileTable), fileTable_length, "The opened file was added to the file table.")

    def test_file_read_success(self):
        '''
            Tests that exactly 5 characters are read from the file with more than 5 characters.
        '''
        addr = self.inter.mem.dataPtr
        syscall, characters, expected_read = 14, 5, 5

        fd = open(self.file)
        fileTable = self.inter.mem.fileTable
        fileTable[3] = fd

        self.inter.set_register("$a0", 3)
        self.inter.set_register("$a1", addr)
        self.inter.set_register("$a2", characters)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        characters_read = self.inter.get_register("$v0")
        read_string = getString(addr, self.inter.mem, characters_read)

        self.assertEqual(characters_read, expected_read, f'The number of characters read ({characters_read}) is incorrect.')
        self.assertEqual(read_string, 'hello', 'The string read is incorrect.')

        fd.close()

    def test_file_read_overread(self):
        '''
            Tests that the number of characters read is at most the number of characters left if the we are trying to read more than
            the amount of characters left to read.
        '''
        addr = self.inter.mem.dataPtr
        syscall, characters, expected_read = 14, 20, 12

        fd = open(self.file)
        fileTable = self.inter.mem.fileTable
        fileTable[3] = fd

        self.inter.set_register("$a0", 3)
        self.inter.set_register("$a1", addr)
        self.inter.set_register("$a2", characters)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        characters_read = self.inter.get_register("$v0")
        read_string = getString(addr, self.inter.mem, characters_read)

        self.assertEqual(characters_read, expected_read, f'The number of characters read ({characters_read}) is incorrect.')
        self.assertEqual(read_string, 'hello world!', 'The string read is incorrect.')

        fd.close()

    def test_file_read_invalid_fd(self):
        '''
            Tests reading from an invalid file descriptor returns -1 in $v0 and the array buffer remains unchanged.
        '''
        addr = self.inter.mem.dataPtr
        syscall, characters, expected_read = 14, 20, -1
        invalid_fd = 3

        self.inter.set_register("$a0", invalid_fd)
        self.inter.set_register("$a1", addr)
        self.inter.set_register("$a2", characters)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        characters_read = self.inter.get_register("$v0")
        read_string = getString(addr, self.inter.mem, characters)

        self.assertEqual(characters_read, expected_read, f'Characters read from an invalid file descriptor.')
        self.assertEqual(read_string, '', 'The array buffer was modified.')

    def test_file_read_closed_fd(self):
        '''
            Tests reading from a closed file descriptor returns -1 in $v0 and the array buffer remains unchanged.
        '''
        addr = self.inter.mem.dataPtr
        syscall, characters, expected_read = 14, 20, -1
        
        fd = open(self.file)
        fileTable = self.inter.mem.fileTable
        fileTable[3] = fd
        fd.close()

        self.inter.set_register("$a0", 3)
        self.inter.set_register("$a1", addr)
        self.inter.set_register("$a2", characters)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        characters_read = self.inter.get_register("$v0")
        read_string = getString(addr, self.inter.mem, characters)

        self.assertEqual(characters_read, expected_read, f'Characters read from a closed file descriptor.')
        self.assertEqual(read_string, '', 'The array buffer was modified.')

    def test_file_write_success(self):
        '''
            Tests that exactly 4 characters are written to the file from an output buffer with more than 4 characters.
        '''
        addr = self.inter.mem.dataPtr
        syscall, characters, expected_write = 15, 4, 4

        fd = open(self.out_file, 'w')
        fileTable = self.inter.mem.fileTable
        fileTable[3] = fd

        self.inter.mem.addAsciiz("Good morning!", addr)
        self.inter.set_register("$a0", 3)
        self.inter.set_register("$a1", addr)
        self.inter.set_register("$a2", characters)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        fd.close()

        characters_written = self.inter.get_register("$v0")
        with open(self.out_file, 'r') as f:
            written_string = f.read()

        self.assertEqual(characters_written, expected_write, f'The number of characters written ({characters_written}) is incorrect.')
        self.assertEqual(written_string, 'Good', 'The string written is incorrect.')

        open(self.out_file, 'w').close() # reset outfile

    def test_file_write_overwrite(self):

        '''
            Tests that the number of characters written is at most the number of characters in the buffer if we are trying to 
            write more than the amount of characters in the buffer.
        '''
        addr = self.inter.mem.dataPtr
        syscall, characters, expected_write = 15, 20, 13

        fd = open(self.out_file, 'w')
        fileTable = self.inter.mem.fileTable
        fileTable[3] = fd

        self.inter.mem.addAsciiz("Good morning!", addr)
        self.inter.set_register("$a0", 3)
        self.inter.set_register("$a1", addr)
        self.inter.set_register("$a2", characters)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())
        fd.close()

        characters_written = self.inter.get_register("$v0")
        with open(self.out_file, 'r') as f:
            written_string = f.read()

        self.assertEqual(characters_written, expected_write, f'The number of characters written ({characters_written}) is incorrect.')
        self.assertEqual(written_string, 'Good morning!', 'The string written is incorrect.')

        open(self.out_file, 'w').close() # reset outfile

    def test_file_write_invalid_fd(self):
        '''
            Tests reading from an invalid file descriptor returns -1 in $v0 and the array buffer remains unchanged.
        '''
        addr = self.inter.mem.dataPtr
        syscall, characters, expected_write = 15, 20, -1

        self.inter.mem.addAsciiz("Good morning!", addr)
        self.inter.set_register("$a0", 3)
        self.inter.set_register("$a1", addr)
        self.inter.set_register("$a2", characters)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        characters_written = self.inter.get_register("$v0")

        self.assertEqual(characters_written, expected_write, f'The number of characters written ({characters_written}) is incorrect.')

    def test_file_write_closed_fd(self):
        '''
            Tests reading from a closed file descriptor returns -1 in $v0 and the array buffer remains unchanged.
        '''
        addr = self.inter.mem.dataPtr
        syscall, characters, expected_write = 15, 20, -1

        fd = open(self.out_file, 'w')
        fileTable = self.inter.mem.fileTable
        fileTable[3] = fd
        fd.close()

        self.inter.mem.addAsciiz("Good morning!", addr)
        self.inter.set_register("$a0", 3)
        self.inter.set_register("$a1", addr)
        self.inter.set_register("$a2", characters)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        characters_written = self.inter.get_register("$v0")
        with open(self.out_file, 'r') as f:
            written_string = f.read()

        self.assertEqual(characters_written, expected_write, f'The number of characters written ({characters_written}) is incorrect.')
        self.assertEqual(written_string, '', 'The closed file was written to.')

        open(self.out_file, 'w').close() # reset outfile

    def test_file_close_success(self):
        '''
            Tests that a valid file descriptor is closed properly.
        '''
        syscall, fd_num = 16, 3

        fd = open(self.file)
        fileTable = self.inter.mem.fileTable
        fileTable[fd_num] = fd

        self.inter.set_register("$a0", fd_num)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        self.assertTrue(fd.closed, f"The file descriptor ({fd_num}) was not closed.")
        self.assertEqual(len(fileTable), 3, f"The closed file descriptor ({fd_num}) was not removed from the file table.")
        self.assertNotIn(fd_num, fileTable, f"The incorrect file descriptor ({fd_num}) was removed from the file table.")


    def test_file_close_no_file(self):
        '''
            Tests that there are no changes when closing an invalid file descriptor not in the file table
        '''
        syscall, fd_num = 16, 3
        fileTable = self.inter.mem.fileTable

        self.inter.set_register("$a0", fd_num)
        self.inter.set_register("$v0", syscall)
        self.inter.execute_instr(Syscall())

        self.assertEqual(len(fileTable), 3, f"The file table was modified.")
