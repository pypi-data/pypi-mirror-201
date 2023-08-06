import os
import random
import re
import struct
import sys
from collections import OrderedDict
from threading import Event, Lock

from PySide6.QtCore import *
from PySide6 import QtWidgets
from numpy import float32

import constants as const
from interpreter import exceptions as ex, instructions as instrs
from interpreter.classes import *
from interpreter.debugger import Debug
from interpreter.memory import Memory
from interpreter.registers import Registers
from interpreter.syscalls import syscalls
from interpreter.compiled_tester import check_function_uninit
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


class Interpreter(QtWidgets.QWidget):
    step = Signal(int)  # use to signal program counter increment
    end = Signal(bool)  # use to signal program termination
    console_out = Signal(str)  # use by out for printing to console
    user_input = Signal(int)  # use by input/set_input for user input syscalls

    def __init__(self, code: List[Instruction], args: List[str]) -> None:
        if settings['gui']:
            super().__init__()
        # For user input syscalls
        self.pause_lock = Event()
        self.input_lock = Event()
        self.lock_input = Lock()
        self.input_str = None
        # Registers
        self.reg = Registers(settings['garbage_registers'])
        self.condition_flags = [False] * 8
        # Memory and program arguments
        self.mem = Memory(settings['garbage_memory'])
        self.handleArgs(args)
        self.initialize_memory(code)
        # For error messages
        self.line_info = ''
        self.debug = Debug()
        self.instruction_count = 0
        self.instr = None
        self.warnings = []
        self.checkWarnings()

    def initialize_memory(self, code: List[Instruction]) -> None:
        '''Initialize memory by adding instructions to the data/text section
        and then replacing the labels with the correct address'''
        # Function control variables
        has_main = False
        comp = re.compile(r'(lb[u]?|lh[u]?|lw[lr]|lw|la|s[bhw]|sw[lr])')
        for line in code:  # Go through the source code line by line, adding declarations first
            if type(line) is Declaration:
                self.set_data(line)
            elif type(line) is Label:
                if line.name == 'main':
                    has_main = True,
                    self.set_register("pc", self.mem.textPtr)
                self.mem.addLabel(line.name, self.mem.textPtr)
            elif type(line) is PseudoInstr:
                for instr in line.instrs:
                    self.mem.addText(instr)
            else:
                self.mem.addText(line)
        if not has_main:
            raise ex.NoMainLabel('Could not find main label')
        self.orig_pc = self.reg.get_register('pc')
        for line in code:  # Replace the labels in load/store instructions by the actual address
            if type(line) is PseudoInstr and comp.match(line.operation):
                addr = self.mem.getLabel(line.label.name)
                line.instrs[0].imm = (addr >> 16) & 0xFFFF
                line.instrs[1].imm = addr & 0xFFFF

        # Special instruction to terminate execution after every instruction has been executed
        self.mem.addText('TERMINATE_EXECUTION')

    def handleArgs(self, args: List[str]) -> None:
        '''Add program arguments to the run time stack.'''
        if len(args) > 0:
            saveAddr = settings['data_max'] - 3
            temp = settings['initial_$sp'] - 4 - (4 * len(args))
            # args.reverse()
            stack = temp
            self.mem.addWord(len(args), stack)
            stack += 4
            for arg in args:
                saveAddr -= (len(arg) + 1)
                self.mem.addAsciiz(arg, saveAddr)
                self.mem.addWord(saveAddr, stack)
                stack += 4

            self.reg.set_register('$sp', temp)
            self.reg.set_register('$a0', len(args))
            self.reg.set_register('$a1', temp + 4)

    def set_data(self, line: Declaration) -> None:
        '''Add the declaration into the data section'''
        INSERT_MEMORY_FUNCTIONS = {
            'byte': self.mem.addByte,
            'half': self.mem.addHWord,
            'word': self.mem.addWord,
            'float': self.mem.addFloat,
            'double': self.mem.addDouble,
            'space': self.mem.addByte
        }
        # Data declaration
        data_type, data = line.type, line.data
        # Special formatting for data
        if data_type == 'float':
            data = [utility.create_float32(d) for d in data]
        elif data_type == 'space':
            data = [random.randint(0, 0xFF) if settings['garbage_memory'] else 0
                    for i in range(data)]
        # If a label is specified, add the label to memory
        if line.name:
            self.mem.addLabel(line.name, self.mem.dataPtr)
        # Align the dataPtr to the proper alignment
        if data_type in const.ALIGNMENT_CONVERSION:
            self.mem.dataPtr = utility.align_address(
                self.mem.dataPtr, const.ALIGNMENT_CONVERSION[data_type])

        if 'ascii' in data_type:  # ascii/asciiz
            # There could be multiple strings separated by commas
            # Add the string to memory and increment address in memory
            s = line.data[1: -1]  # Remove quotation marks
            s = utility.handle_escapes(s)
            null_terminate = 'z' in data_type
            self.mem.addAscii(s, self.mem.dataPtr,
                              null_terminate=null_terminate)
            self.mem.dataPtr += len(s) + int(null_terminate)  # T/F -> 1/0

        elif data_type in INSERT_MEMORY_FUNCTIONS:
            for info in data:
                INSERT_MEMORY_FUNCTIONS[data_type](info, self.mem.dataPtr)
                self.mem.dataPtr += const.ALIGNMENT_CONVERSION.get(
                    data_type, 1)

        elif data_type == 'align':
            if not 0 <= line.data <= 3:
                raise ex.InvalidImmediate(
                    f'Value({line.data}) for .align is invalid')
            self.mem.dataPtr = utility.align_address(
                self.mem.dataPtr, 2 ** line.data)

    def get_register(self, reg: str, double: bool = False) -> Union[int, float32, float]:
        return self.reg.get_register(reg, double=double)

    def set_register(self, reg: str, data: Union[int, float32, float], double: bool = False) -> None:
        self.reg.set_register(reg, data, double=double)

    def get_reg_word(self, reg: str) -> int:
        return self.reg.get_reg_word(reg)

    def set_reg_word(self, reg: str, data: int) -> None:
        self.reg.set_reg_word(reg, data)

    def execute_instr(self, instr) -> None:
        '''Execute the given MIPS instruction object.'''
        # Function control variables
        op = instr.operation
        # instruction hooks before executing the instruction
        if op in settings["function_hooks"]["previous"]:
            settings["function_hooks"]["previous"][op](self, instr)
        # j type instructions (Label/Return) # b, j, jal, jalr, jr
        if type(instr) is JType:
            target = self.mem.getLabel(instr.label.name)
            instrs.get_instr(op)(target, self.reg)

        # syscall
        elif type(instr) is Syscall:
            code = self.get_register('$v0')
            if code in syscalls and code in settings['enabled_syscalls']:
                syscalls[code](self)
            else:
                raise ex.InvalidSyscall('Not a valid syscall code:')

        elif type(instr) is Breakpoint:
            raise ex.BreakpointException(f'code = {instr.code}')

        else:
            additional_args = {}
            additional_args['reg'] = self.reg
            if type(instr) in [Compare, BranchFloat, MoveCond]:
                additional_args['flags'] = self.condition_flags
            if type(instr) in [Branch, BranchFloat, LoadMem]:
                additional_args['mem'] = self.mem
            if op[-1] == 'u':
                op = op[:-1]
                additional_args['signed'] = False
            if op.split('.')[-1] == 'd' and op.split('.')[0] != 'cvt':
                # convert .d to .s with double=True
                op = '.'.join(op.split('.')[:-1]+['s'])
                additional_args['double'] = True

            instrs.get_instr(op)(*instr.get_dest(), *
                                 instr.get_src(), **additional_args)

        if op in settings["function_hooks"]["after"]:  # instruction hooks at the end
            settings["function_hooks"]["after"][op](self, instr)

    def interpret(self) -> None:
        '''Goes through the text segment and executes each instruction.'''
        debug = self.debug
        try:
            while True:  # Get the next instruction and increment pc
                pc = self.get_register('pc')
                if str(pc) not in self.mem.text:
                    raise ex.MemoryOutOfBounds(f'{pc} is not a valid address')
                if self.instruction_count > settings['max_instructions']:
                    raise ex.InstrCountExceed(
                        f'Exceeded maximum instruction count: {settings["max_instructions"]}')
                self.instr = self.mem.text[str(pc)]
                if self.instr == 'TERMINATE_EXECUTION':
                    if settings['gui']:
                        self.end.emit(False)
                    break
                self.set_register('pc', self.get_register('pc')+4)
                self.instruction_count += 1
                self.line_info = str(self.instr.filetag)
                if settings['gui']:
                    self.step.emit(pc)

                if debug.debug(self.instr):
                    if not debug.continueFlag:
                        self.pause_lock.clear()
                    if settings['gui']:
                        debug.listen(self)
                    elif not settings['gui'] and settings['debug']:
                        debug.listen(self)
                elif settings['gui'] and type(self.instr) is Syscall and self.get_register('$v0') in [10, 17]:
                    if settings['disp_instr_count']:
                        self.out(
                            f'\nInstruction count: {self.instruction_count}')
                    self.end.emit(False)
                    break

                if settings['gui']:
                    debug.push(self)
                self.execute_instr(self.instr)  # execute
        except Exception as e:
            if hasattr(e, 'message'):
                e.message += f' {self.line_info}'
            if settings['gui']:
                self.end.emit(False)
                self.out(e, "\n")
            else:
                raise e

    def dump(self) -> None:
        '''Dump the contents in registers and memory.'''
        self.out(f"Registers:\n{self.reg.dump()}", end="\n")
        self.out('Memory:', end="\n")
        self.mem.dump()

    def out(self, s: str, end='') -> None:
        '''Prints to terminal or the console in the GUI'''
        if settings['gui']:
            print(s)
            self.console_out.emit(f'{s}{end}')
        else:
            print(s, end=end)

    def get_input(self, input_type: str) -> str:
        '''Prompts the user for an input value.'''
        if settings['gui']:
            self.input_lock.clear()
            self.user_input.emit(const.USER_INPUT_TYPE.index(input_type))
            self.input_lock.wait()
            return self.input_str
        else:
            return input()

    def set_input(self, string: str) -> None:
        '''Set input string to the provided string'''
        self.lock_input.acquire()
        if not self.input_lock.isSet():
            self.input_str = string
            self.input_lock.set()
        self.lock_input.release()

    def reset(self) -> bool:
        '''Resets the program counter.'''
        if hasattr(self, 'orig_pc'):
            self.reg.set_register('pc', self.orig_pc)
            return True
        return False

    def checkWarnings(self) -> None:
        '''Statically checks all warnings for unitialized variables and hard coding register convention'''
        func_code = []
        label_name = "Unlabeled"
        # print(self.mem.text)
        for pc in self.mem.text:
            if self.mem.text[pc] == "TERMINATE_EXECUTION":
                warning_list = check_function_uninit(label_name, func_code)
                if warning_list:
                    self.warnings.extend(warning_list)
                break
            line = self.mem.text[pc]
            # print(line)
            if self.mem.getLabelAtAddr(int(pc)):
                warning_list = check_function_uninit(label_name, func_code)
                if warning_list:
                    self.warnings.extend(warning_list)
                label_name = self.mem.getLabelAtAddr(int(pc))
                func_code = [line]
            else:
                func_code.append(line)

    def printWarnings(self) -> None:
        '''Prints the list of warnings to the user'''
        for warning in self.warnings:
            self.out("WARNING: " + warning, end='\n')
