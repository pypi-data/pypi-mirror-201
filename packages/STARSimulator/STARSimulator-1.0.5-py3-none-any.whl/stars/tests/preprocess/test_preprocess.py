from os import path as p
from pathlib import Path
import unittest

from preprocess import *

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


class TestPreprocess(unittest.TestCase):

    def test_walk_include_success(self):
        path = Path(f"{p.dirname(__file__)}/includeSuccess.asm")
        path.resolve()

        files = []
        eqv_dict = {}
        abs_to_rel = {}
        walk(path, files, eqv_dict, abs_to_rel, path.parent)
        res = [f.name for f in files]
        self.assertEqual(res, ['includeSuccess.asm', 'toInclude.asm'],
                         msg='Failed test_walk_include_success.')

    def test_walk_include_already_included(self):
        path = Path(f"{p.dirname(__file__)}/alreadyIncluded.asm")
        path.resolve()

        files = []
        eqv_dict = {}
        abs_to_rel = {}
        self.assertRaises(FileAlreadyIncluded, walk, path,
                          files, eqv_dict, abs_to_rel, path.parent)

    def test_walk_include_file_dne(self):
        path = Path(f"{p.dirname(__file__)}/invalidFile.asm")
        path.resolve()

        files = []
        eqv_dict = {}
        abs_to_rel = {}
        self.assertRaises(FileNotFoundError, walk, path,
                          files, eqv_dict, abs_to_rel, path.parent)

    def test_walk_eqv_success(self):
        path = Path(f"{p.dirname(__file__)}/eqvTest.asm")
        path.resolve()

        files = []
        eqv_dict = {}
        abs_to_rel = {}
        walk(path, files, eqv_dict, abs_to_rel, path.parent)
        expected = {r'\bword\b': '"hello"'}
        self.assertEqual(eqv_dict, expected,
                         msg='Failed test_walk_eqv_success.')

    def test_eqv_restricted_token(self):
        path = Path(f"{p.dirname(__file__)}/eqvRestricted.asm")
        path.resolve()

        files = []
        eqv_dict = {}
        abs_to_rel = {}
        self.assertRaises(InvalidEQV, walk, path, files,
                          eqv_dict, abs_to_rel, path.parent)

    def test_preprocess_eqv_success(self):
        path = Path(f"{p.dirname(__file__)}/eqvTest.asm")
        path.resolve()

        files = []
        eqv_dict = {}
        abs_to_rel = {}
        walk(path, files, eqv_dict, abs_to_rel, path.parent)
        file = files[0]
        contents = ''
        with file.open() as f:
            s = f.readlines()
            contents = ''.join(s)
        data = preprocess(contents, file, eqv_dict)

        self.assertEqual(data, f'''.data  "{p.dirname(__file__)}/eqvTest.asm" 1
.eqv "hello" "hello"  "{p.dirname(__file__)}/eqvTest.asm" 2
.asciiz "hello"  "{p.dirname(__file__)}/eqvTest.asm" 3
.asciiz " word " # word  "{p.dirname(__file__)}/eqvTest.asm" 4

.text  "{p.dirname(__file__)}/eqvTest.asm" 6

main:  "{p.dirname(__file__)}/eqvTest.asm" 8
li $t0, 0  "{p.dirname(__file__)}/eqvTest.asm" 9

li $v0, 30  "{p.dirname(__file__)}/eqvTest.asm" 11
li $a0, 0x10010000  "{p.dirname(__file__)}/eqvTest.asm" 12
li $a1, 0x10010010  "{p.dirname(__file__)}/eqvTest.asm" 13
syscall  "{p.dirname(__file__)}/eqvTest.asm" 14
''', msg='Failed test_preprocess_eqv_success.')

    def test_preprocess_include_success(self):
        path = Path(f"{p.dirname(__file__)}/includeSuccess.asm")
        path.resolve()

        files = []
        eqv_dict = {}
        abs_to_rel = {}
        walk(path, files, eqv_dict, abs_to_rel, path.parent)
        expected = {files[0].as_posix(): f'''.include "toInclude.asm"  "{p.dirname(__file__)}/includeSuccess.asm" 1
.text  "{p.dirname(__file__)}/includeSuccess.asm" 2
li $a0, 24  "{p.dirname(__file__)}/includeSuccess.asm" 3
li $v0, 4  "{p.dirname(__file__)}/includeSuccess.asm" 4
syscall  "{p.dirname(__file__)}/includeSuccess.asm" 5
li $v0, 10  "{p.dirname(__file__)}/includeSuccess.asm" 6
syscall  "{p.dirname(__file__)}/includeSuccess.asm" 7

.data  "{p.dirname(__file__)}/includeSuccess.asm" 9
UvU: .asciiz "owo what's this?"  "{p.dirname(__file__)}/includeSuccess.asm" 10
''',
                    files[1].as_posix(): f'''.text  "{p.dirname(__file__)}/toInclude.asm" 1
li $v0, 10  "{p.dirname(__file__)}/toInclude.asm" 2
syscall  "{p.dirname(__file__)}/toInclude.asm" 3

.data  "{p.dirname(__file__)}/toInclude.asm" 5
jello: .word 4  "{p.dirname(__file__)}/toInclude.asm" 6
'''}
        contents = {}
        processed = {}
        for file in files:
            with file.open() as f:
                contents[file.as_posix()] = ''.join(f.readlines())
                processed[file.as_posix()] = preprocess(
                    contents[file.as_posix()], file, eqv_dict)
            self.assertEqual(processed[file.as_posix()], expected[file.as_posix(
            )], msg=f"Failed test_preprocess_include_success on file {file.name}.")

        (og_text, text, _) = link(files, contents, processed, abs_to_rel)
        self.assertEqual(text, f'''.text  "{p.dirname(__file__)}/toInclude.asm" 1
li $v0, 10  "{p.dirname(__file__)}/toInclude.asm" 2
syscall  "{p.dirname(__file__)}/toInclude.asm" 3

.data  "{p.dirname(__file__)}/toInclude.asm" 5
jello: .word 4  "{p.dirname(__file__)}/toInclude.asm" 6
.text  "{p.dirname(__file__)}/includeSuccess.asm" 2
li $a0, 24  "{p.dirname(__file__)}/includeSuccess.asm" 3
li $v0, 4  "{p.dirname(__file__)}/includeSuccess.asm" 4
syscall  "{p.dirname(__file__)}/includeSuccess.asm" 5
li $v0, 10  "{p.dirname(__file__)}/includeSuccess.asm" 6
syscall  "{p.dirname(__file__)}/includeSuccess.asm" 7

.data  "{p.dirname(__file__)}/includeSuccess.asm" 9
UvU: .asciiz "owo what's this?"  "{p.dirname(__file__)}/includeSuccess.asm" 10
''', msg="Failed test_preprocess_include_success on linking preprocessed text.")
        self.assertEqual(og_text, '''.text
li $v0, 10
syscall

.data
jello: .word 4.text
li $a0, 24
li $v0, 4
syscall
li $v0, 10
syscall

.data
UvU: .asciiz "owo what's this?"''', msg="Failed test_preprocess_include_success on linking original text.")
