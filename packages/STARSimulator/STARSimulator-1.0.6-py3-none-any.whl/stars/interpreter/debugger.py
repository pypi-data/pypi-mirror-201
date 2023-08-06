import re

import constants as const
from interpreter.classes import *
from interpreter.exceptions import InvalidRegister
from interpreter.utility import to_ascii
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


def next(cmd, interp) -> bool:
    '''
        Returns False to break out of the listen
        loop for user input.
    '''
    return False


def quit(cmd, interp) -> None:
    '''
        Exits the program.
    '''
    exit()


def print_usage_text() -> None:
    help_message = [
        "USAGE:  ",
        "[b]reak <filename> <line_no>",
        "[d]elete: Clear all breakpoints",
        "[n]ext: Step to the next instruction",
        "[c]ontinue: Run until the next breakpoint",
        "[i]nfo b: Print information about the breakpoints",
        "[p]rint <flag>",
        "[p]rint <reg> <format>",
        "[p]rint <label> <data_type> <length> <format>",
        "[q]uit: Terminate the program",
        "[h]elp: Print this usage text",
        "[r]everse: Step back to the previous instruction",
    ]
    print("\n".join(help_message))


def _print(cmd, interp):  # cmd = ['p', value, opts...]
    def str_value(val, base, bytes):
        # Return a string representation of a number as decimal, unsigned decimal, hex or binary
        # bytes: number of bytes to print (for hex, bin)
        representation_dictionary = {
            'i': str(val),
            'u': str(val if val >= 0 else val + const.WORD_SIZE),
            'x': f'0x{val & 0xFFFFFFFF:0{2 * bytes}x}',
            'b': f'0b{val & 0xFFFFFFFF:0{8 * bytes}b}',
        }
        return representation_dictionary[base]

    if len(cmd) == 2:  # Print condition flag
        try:
            flag = int(cmd[1])
            if 0 <= flag <= 7:
                print(
                    f"The value of flag {flag} is {interp.condition_flags[flag]}")
            else:
                raise ValueError
        except ValueError:
            print(f"{cmd[1]} is not a valid flag.")
            print_usage_text()
        return True

    elif len(cmd) < 3:  # Invalid form of input
        print("Invalid usage of print.")
        print_usage_text()
        return True

    elif cmd[1] in const.REGS and cmd[2] in ['i', 'u', 'x', 'b']:  # Print contents of a register
        reg, base = cmd[1], cmd[2]
        value = interp.get_register(reg)
        print(f'{reg} {str_value(value, base, 4)}')
        return True

    # Print contents of a floating point register
    elif cmd[1] in const.F_REGS and cmd[2] in ['f', 'd']:
        reg, base = cmd[1], cmd[2]
        try:
            print(f'{reg} {interp.get_register(reg, double=base=="d")}')
        except InvalidRegister:
            print('Not an even numbered register')
        return True

    # Data section
    # Print memory contents at a label
    elif len(cmd) >= 3 and cmd[1] in interp.mem.labels:
        label, data_type = cmd[1], cmd[2]

        if data_type == 's':  # print as string
            print(f'{label} {interp.mem.getString(label)}')
            return True

        try:  # Get the number of words/halfwords/bytes/floats/doubles/characters to print
            length = int(cmd[3])
            if length < 1:
                raise ValueError
        except ValueError:
            print(f"{cmd[3]} is not a valid length.")
            print_usage_text()
            return True
        addr = interp.mem.getLabel(label)
        memory_print = {
            'w': (4, interp.mem.getWord),
            'h': (2, interp.mem.getHWord),
            'b': (1, interp.mem.getByte),
            'f': (4, interp.mem.getFloat),
            'd': (8, interp.mem.getDouble),
        }
        if len(cmd) == 5 and data_type in ['w', 'h', 'b']:
            base = cmd[4]
            if base not in ['i', 'u', 'x', 'b']:
                print(f"{cmd[4]} is not a valid base.")
                print_usage_text()
                return True
            bytes, memory_function = memory_print[data_type]
            for i in range(length):
                print(f'{str_value(memory_function(addr+bytes*i), base, bytes)}')
            return True

        elif len(cmd) >= 4 and data_type in ['f', 'd']:
            bytes, memory_function = memory_print[data_type]
            for i in range(length):
                print(memory_function(addr+bytes*i))
            return True

        elif len(cmd) >= 4 and data_type == 'c':  # Print as character
            print(f'{label}')
            for i in range(length):
                print(f'\t{to_ascii(interp.mem.getByte(addr+i))}')
            return True

        else:
            if data_type not in ['w', 'h', 'b', 'f', 'd', 'c']:
                print(f"{data_type} is not a valid data type.")
            else:
                print("Invalid usage of print.")
            print_usage_text()
            return True

    print("Invalid usage of print.")
    print_usage_text()
    return True


class Debug:
    def __init__(self):
        self.stack = []
        self.continueFlag = False
        self.breakpoints = set()
        self.handle = {'b': self.addBreakpoint,
                       'break': self.addBreakpoint,
                       'n': next,
                       'next': next,
                       'c': self.cont,
                       'continue': self.cont,
                       'i': self.printBreakpoints,
                       'info': self.printBreakpoints,
                       'd': self.clearBreakpoints,
                       'delete': self.clearBreakpoints,
                       'p': _print,
                       'print': _print,
                       'q': quit,
                       'quit': quit,
                       'r': self.reverse,
                       'reverse': self.reverse}

    def listen(self, interp):
        '''
            Waits for user input on the current instruction and pushes
            the instruction onto the stack.
        '''
        loop = True
        while loop and not settings['gui']:
            if type(interp.instr) is not str:
                instr_text = interp.instr.original_text.strip()
                marker_idx = instr_text.find('\x81')
                if marker_idx >= 0:
                    instr_text = instr_text[:marker_idx]

                print(
                    f'{instr_text} {f"({interp.instr})" if interp.instr.is_from_pseudoinstr else ""}')
                print(f' {interp.instr.filetag}')

            try:
                cmd = input('>')
            except EOFError:
                exit()
            cmd = re.findall(r'\S+', cmd)

            if len(cmd) > 0 and cmd[0] in self.handle.keys():
                loop = self.handle[cmd[0]](cmd, interp)
            else:
                print_usage_text()

        if settings['gui']:
            interp.pause_lock.wait()
            if not self.continueFlag:
                interp.pause_lock.clear()

        self.push(interp)

    def debug(self, instr) -> bool:
        '''
            Checks whether to break execution and ask for user input.
            If the continueFlag is true, then don't break execution.
        '''
        current = instr.filetag.file_name, str(instr.filetag.line_no)

        if settings['debug'] and current in self.breakpoints:
            self.continueFlag = False
            return True

        if not self.continueFlag:
            return settings['debug']

    def push(self, interp) -> None:
        '''
            Pushes the changes to the Registers and Memory objects for the 
            current instruction to the stack.
        '''
        def is_float_double(x):
            return '.d' in x

        instr = interp.instr
        prev_pc = interp.get_register('pc') - 4
        op = instr.operation

        if type(instr) in {RType, IType}:
            if op in {'mult', 'multu', 'madd', 'maddu', 'msub', 'msubu', 'div', 'divu'}:
                prev = MChange(interp.get_register('hi'),
                               interp.get_register('lo'), prev_pc)
            else:
                dest_reg = instr.rd if type(instr) is RType else instr.rt
                prev = RegChange(dest_reg, interp.get_register(
                    dest_reg), prev_pc, is_double=is_float_double(op))

        elif type(instr) is Move:
            reg = instr.rd if 'f' in instr.operation else instr.rs
            prev = RegChange(reg, interp.get_register(reg), prev_pc)

        elif type(instr) is LoadImm:
            prev = RegChange(instr.rt, interp.get_register(instr.rt), prev_pc)

        elif type(instr) is JType:
            if 'l' in op:  # jal
                prev = RegChange('$ra', interp.get_register('$ra'), prev_pc)
            else:
                prev = Change(prev_pc)

        elif type(instr) is LoadMem:
            if op[0] == 'l':  # Loads
                prev = RegChange(instr.rt, interp.get_register(
                    instr.rt), prev_pc, is_double=is_float_double(op))
            else:  # Stores
                addr = interp.get_register(instr.rs) + instr.imm
                mem_function = {
                    's': interp.mem.getFloat,
                    'd': interp.mem.getDouble,
                    'w': interp.mem.getWord,
                    'h': interp.mem.getHWord,
                }
                prev = MemChange(addr, mem_function.get(
                    op[-1], interp.mem.getByte)(addr), prev_pc, op[-1])

        elif type(instr) is Compare:
            prev = FlagChange(
                instr.imm, interp.condition_flags[instr.imm], prev_pc)

        elif type(instr) is Convert:
            prev = RegChange(instr.rs, interp.get_register(
                instr.rs), prev_pc, is_double=op[-3] == 'd')

        elif type(instr) is MoveFloat:
            if op == 'mtc1':
                prev = RegChange(
                    instr.rt, interp.get_register(instr.rt), prev_pc)
            elif op == 'mfc1':
                prev = RegChange(
                    instr.rs, interp.get_register(instr.rs), prev_pc)
            else:
                prev = RegChange(instr.rd, interp.get_register(
                    instr.rd), prev_pc, is_double=is_float_double(op))

        elif type(instr) is MoveCond:
            prev = RegChange(instr.rt, interp.get_register(
                instr.rt), prev_pc, is_double=is_float_double(op))

        else:  # branches, nops, jr, j
            prev = Change(prev_pc)

        self.stack.append(prev)

    def reverse(self, cmd, interp) -> bool:
        '''
            Pops the last change from the stack of instructions executed and
            reverses the changes and request for the next user input for the 
            previous instruction.
        '''
        if len(self.stack) > 0:
            prev = self.stack.pop()

            if type(prev) is RegChange:
                interp.set_register(prev.reg, prev.val, double=prev.is_double)

            elif type(prev) is MemChange:
                mem_function = {
                    's': interp.mem.addFloat,
                    'd': interp.mem.addDouble,
                    'w': interp.mem.addWord,
                    'h': interp.mem.addHWord,
                }
                mem_function.get(prev.type, interp.mem.addByte)(
                    prev.val, prev.addr)

            elif type(prev) is MChange:
                interp.set_register('hi', prev.hi)
                interp.set_register('lo', prev.lo)

            elif type(prev) is FlagChange:
                interp.condition_flags[prev.flag] = prev.value

            interp.set_register('pc', prev.pc + 4)
            interp.instr = interp.mem.text[str(prev.pc)]

        if settings['gui']:
            print(interp.reg.reg['pc'])
            if prev != None:
                interp.step.emit(prev.pc)
            else:
                interp.step.emit(settings['initial_pc'])

        return True

    # cmd = ['b', filename, lineno]
    def addBreakpoint(self, cmd: List[str], interp) -> bool:
        '''
            Adds the given breakpoint to the set of breakpoints.
        '''
        if len(cmd) == 3 and str(cmd[2]).isdecimal():
            self.breakpoints.add((f'"{cmd[1]}"', cmd[2]))  # filename, lineno
            return True
        else:
            print_usage_text()
        return True

    def cont(self, cmd, interp) -> bool:
        '''
            Sets the continueFlag to True which executes all
            commands until termination or a breakpoint.
        '''
        self.continueFlag = True
        return False

    def printBreakpoints(self, cmd, interp) -> bool:
        '''
            Prints the set of breakpoints and request for 
            the next user input for the current instruction.
        '''
        for i, b in enumerate(self.breakpoints):
            print(f'{i+1} {b[0]} {b[1]}')
        return True

    def clearBreakpoints(self, cmd: List[str], interp) -> bool:
        '''
            Resets the set of breakpoints and request for 
            the next user input for the current instruction.
        '''
        if len(cmd) == 1:
            self.breakpoints = set()
        else:
            print_usage_text()
        return True

    def removeBreakpoint(self, cmd: List[str], interp) -> None:
        '''
            Removes the given breakpoint from the set of breakpoints.
            This function is used by the controller to remove breakpoints 
            from the GUI.
        '''
        self.breakpoints.remove((cmd[0], cmd[1]))
