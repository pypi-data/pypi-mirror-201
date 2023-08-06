from typing import List, Union

from interpreter import exceptions as ex
from interpreter import utility

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


class Label:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Declaration(Label):
    def __init__(self, name: str, type: str, data: Union[int, List[int], str, List[str]]):
        super().__init__(name)
        self.type = type[1:]
        self.data = data

    def __str__(self):
        return f"{super().__str__()}: .{self.type}"


class FileTag:
    def __init__(self, file_name: str, line_no: int):
        self.file_name = file_name
        self.line_no = line_no

    def __str__(self):
        return f"{self.file_name}, {self.line_no}"


class Instruction:
    def __init__(self, op):
        self.operation = op

    def __str__(self):
        return f"{self.operation}"


class Breakpoint(Instruction):
    def __init__(self, code: int = 0):
        super().__init__("breakpoint")
        self.code = code


class Nop(Instruction):
    def __init__(self):
        super().__init__("nop")


class Syscall(Instruction):
    def __init__(self):
        super().__init__("syscall")

# RType Instructions


class RType(Instruction):
    # Two or Three registers
    def __init__(self, op: str, regs: List[str]):
        super().__init__(op)
        if len(regs) == 2:
            if op in ["jr", "jalr"]:
                self.rd, self.rs = regs
                self.rt = None
            else:
                self.rs, self.rt = regs
        else:
            self.rd, self.rs, self.rt = regs

    def __str__(self) -> str:
        if self.operation in ["jr", "jalr"]:
            if self.operation == "jr":
                return f"{super().__str__()} {self.rs}"
            return f"{super().__str__()} {self.rd}, {self.rs}" if self.rd != "$ra" else f"{super().__str__()} {self.rs}"
        return f"{super().__str__()} {f'{self.rd}, ' if hasattr(self, 'rd') else ''}{self.rs}, {self.rt}"

    def get_dest(self) -> List[str]:
        return [self.rd] if hasattr(self, 'rd') else []

    def get_src(self) -> List[str]:
        return [reg for reg in [self.rs, self.rt] if reg]


class Move(Instruction):
    def __init__(self, op: str, reg: str):
        super().__init__(op)
        if 'f' in op:
            self.rs, self.rd = op[2:], reg
        else:
            self.rs, self.rd = reg, op[2:]

    def __str__(self) -> str:
        return f"{super().__str__()} {self.rd if 'f' in self.operation else self.rs}"

    def get_dest(self) -> List[str]:
        return [self.rd]

    def get_src(self) -> List[str]:
        return [self.rs]


class MoveFloat(RType):
    def __init__(self, op: str, regs: List[str]):
        super().__init__(op, regs)

# IType Instructions


class IType(Instruction):
    # Two registers and an immediate
    def __init__(self, op: str, regs: List[str], imm: int):
        super().__init__(op)
        self.rt, self.rs = regs
        if imm is not None:
            self.imm = imm

    def __str__(self) -> str:
        if self.operation in ['or', 'ori', 'and', 'andi', 'xor', 'xori']:
            imm = f", {utility.format_hex(self.imm)}"
        else:
            imm = f", {self.imm}" if hasattr(self, 'imm') else ""
        return f"{super().__str__()} {self.rt}, {self.rs}{imm}"

    def get_dest(self) -> List[str]:
        return [self.rt]

    def get_src(self) -> List[str]:
        return [self.rs, self.imm] if hasattr(self, 'imm') else [self.rs]


class Compare(IType):  # c.{eq|le|lt}.{s|d}
    def __init__(self, op: str, rt: str, rs: str, flag: int):
        if not 0 <= flag <= 7:
            raise ex.InvalidArgument(
                'Condition flag number must be between 0 - 7')
        super().__init__(op, [rt, rs], flag)


class Convert(IType):
    def __init__(self, op: str, rt: str, rs: str):
        super().__init__(op, [rt, rs], None)


class Branch(IType):
    def __init__(self, op: str, rs: str, rt: str, label: Label):
        super().__init__(op, [rt, rs], None)
        self.label = label

    def __str__(self) -> str:
        return f"{super(IType, self).__str__()} {self.rs}, {self.rt}, {self.label.name}"

    def get_dest(self) -> List[str]:
        return [self.label.name]

    def get_src(self) -> List[str]:
        return [self.rs] if 'z' in self.operation else [self.rs, self.rt]


class BranchFloat(Branch):  # bc1{f|t}
    def __init__(self, op: str, label: Label, flag: int):
        if not 0 <= flag <= 7:
            raise ex.InvalidArgument(
                'Condition flag number must be between 0 - 7')
        super().__init__(op, None, None, label)
        self.flag = flag

    def __str__(self) -> str:
        return f"{super(IType, self).__str__()} {self.flag} {self.label.name}"

    def get_src(self) -> List[str]:
        return [self.flag]


class LoadImm(IType):
    def __init__(self, op: str, reg: str, imm: int):
        super().__init__(op, [reg, None], imm)

    def __str__(self) -> str:
        imm_hex = utility.format_hex(self.imm)
        return f"{super(IType, self).__str__()} {self.rt}, {imm_hex}"

    def get_src(self):
        return [self.imm]


class LoadMem(IType):
    def __init__(self, op: str, reg: str, addr: str, imm: int):
        super().__init__(op, [reg, addr], imm)

    def __str__(self) -> str:
        return f"{super(IType, self).__str__()} {self.rt}, {self.imm}({self.rs})"


class MoveCond(Compare):  # mov{f|t}, mov{f|t}.{s|d}
    pass

# JType Instructions


class JType(Instruction):
    # A label or a register as a target
    def __init__(self, op: str, label: Label):
        super().__init__(op)
        self.label = label

    def __str__(self):
        return f"{super().__str__()} {self.label}"


class PseudoInstr(Instruction):
    def __init__(self, op: str, instrs: List):
        super().__init__(op)
        self.instrs = instrs

# Change classes for putting instructions on the stack


class Change:
    def __init__(self, pc: int):
        self.pc = pc


class FlagChange:
    def __init__(self, flag: int, value: bool, pc: int):
        self.flag = flag
        self.value = value
        self.pc = pc


class MChange:
    def __init__(self, hi: int, lo: int, pc: int):
        self.pc = pc
        self.hi = hi
        self.lo = lo

# type can be 'w', 'h', or 'b' to indicate word, halfword, and byte respectively


class MemChange:
    def __init__(self, addr: int, val: int, pc: int, type: str):
        self.addr = addr
        self.val = val
        self.pc = pc
        self.type = type


class RegChange:
    def __init__(self, reg: str, val: int, pc: int, is_double: bool = False):
        self.reg = reg
        self.val = val
        self.pc = pc
        self.is_double = is_double
