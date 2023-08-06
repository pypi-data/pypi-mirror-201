import math
import warnings
import struct
from typing import Callable, Union, Tuple, Dict, List

from numpy import float32

from constants import WORD_SIZE, HALF_SIZE, WORD_MASK, WORD_MAX, WORD_MIN
from interpreter import exceptions as ex
from interpreter.memory import Memory
from interpreter.registers import Registers
from interpreter.utility import overflow_detect

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


# Regular instructions
# Check if a 16-bit immediate is valid.
def valid_immed(n: int) -> bool:
    return -HALF_SIZE // 2 <= n < HALF_SIZE // 2

# Check if an unsigned 16-bit immediate is valid.


def valid_immed_unsigned(n: int) -> bool:
    return 0 <= n < HALF_SIZE

# Check if a shift amount is valid.


def valid_shamt(n: int) -> bool:
    return 0 <= n < 32

# Convert a signed 32-bit integer to an unsigned one.


def to_unsigned(n: int) -> int:
    return n if n >= 0 else n + WORD_SIZE

# Helper method for float -> int conversion instructions


def nan_or_inf(a: Union[float32, float]) -> bool:
    return math.isnan(a) or math.isinf(a)


def convert_to_int(a: Union[float32, float], func) -> int:
    if nan_or_inf(a):
        return WORD_MAX

    result = func(a)
    return result if WORD_MIN <= result <= WORD_MAX else WORD_MAX

# helper for ceil, floor, round, trunc


def interpret_as_float(x: int) -> float32:
    x_bytes = struct.pack('>i', x)
    return struct.unpack('>f', x_bytes)[0]

# helper for {m}add{u}/{m}sub{u} instructions


def add_helper(a: int, b: int, signed: bool = True) -> int:
    # Add two 32-bit two's complement numbers
    if signed:
        if not -WORD_SIZE // 2 <= a + b < WORD_SIZE // 2:
            raise ex.ArithmeticOverflow("Overflow while adding")

    return a + b

# helper for mul, mult{u}, madd{u}, msub{u}


def mul_helper(a: int, b: int, thirty_two_bits: bool = True, signed: bool = True) -> Union[int, Tuple[int, int]]:
    # Multiply two 32-bit numbers
    # The result is a 64-bit number. (Unless 32 bits are specified)
    if thirty_two_bits:  # mul lower 32 bits only
        return overflow_detect(a*b)
    if signed:  # mult (64 bits, signed)
        result = a * b
    else:  # multu (64 bits, unsigned)
        result = to_unsigned(a) * to_unsigned(b)

    return result & WORD_MASK, (result >> 32) & WORD_MASK

# RTYPE 3 registers
# FLOAT RTYPES 3


def add_f(dest: str, src: str, operand: str, reg: Registers, double: bool = False) -> None:
    a, b = reg.get_register(src, double=double), reg.get_register(
        operand, double=double)
    if type(a) is float32:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = float32(a + b)
    else:
        result = a + b
    reg.set_register(dest, result, double=double)


def div_f(dest: str, src: str, operand: str, reg: Registers, double: bool = False) -> None:
    a, b = reg.get_register(src, double=double), reg.get_register(
        operand, double=double)
    if type(a) is float32:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = float32(a / b)
    else:
        try:
            result = a / b
        except ZeroDivisionError:
            if a > 0:
                result = float('inf')
            elif a < 0:
                result = float('-inf')
            else:
                result = float('nan')
    reg.set_register(dest, result, double=double)


def mul_f(dest: str, src: str, operand: str, reg: Registers, double: bool = False) -> None:
    a, b = reg.get_register(src, double=double), reg.get_register(
        operand, double=double)
    if type(a) is float32:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = float32(a * b)
    else:
        result = a * b
    reg.set_register(dest, result, double=double)


def sub_f(dest: str, src: str, operand: str, reg: Registers, double: bool = False) -> None:
    a, b = reg.get_register(src, double=double), reg.get_register(
        operand, double=double)
    if type(a) is float32:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = float32(a - b)
    else:
        result = a - b
    reg.set_register(dest, result, double=double)

# Standard RTYPES 3


def add(dest: str, src: str, operand: str, reg: Registers, signed: bool = True) -> None:
    a, b = reg.get_register(src), reg.get_register(operand)
    result = add_helper(a, b, signed=signed)
    reg.set_register(dest, result)


def sub(dest: str, src: str, operand: str, reg: Registers, signed: bool = True) -> None:
    # Subtract two 32-bit two's complement numbers
    a, b = reg.get_register(src), reg.get_register(operand)
    result = add_helper(a, -b, signed=signed)
    reg.set_register(dest, result)


# Set on less than.
def slt(dest: str, src: str, operand: str, reg: Registers, signed: bool = True) -> None:
    a, b = reg.get_register(src), reg.get_register(operand)
    result = a < b if signed else a & 0xFFFFFFFF < b & 0xFFFFFFFF
    reg.set_register(dest, int(result))  # 1 if True else 0


# Bitwise AND of two 32-bit numbers.
def _and(dest: str, src: str, operand: str, reg: Registers) -> None:
    a, b = reg.get_register(src), reg.get_register(operand)
    reg.set_register(dest, a & b)


def mul(dest: str, src: str, operand: str, reg: Registers) -> None:
    a, b = reg.get_register(src), reg.get_register(operand)
    result = mul_helper(a, b)
    reg.set_register(dest, result)


# Bitwise NOR of two 32-bit numbers.
def nor(dest: str, src: str, operand: str, reg: Registers) -> None:
    a, b = reg.get_register(src), reg.get_register(operand)
    reg.set_register(dest, ~(a | b))


# Bitwise OR of two 32-bit numbers.
def _or(dest: str, src: str, operand: str, reg: Registers) -> None:
    a, b = reg.get_register(src), reg.get_register(operand)
    reg.set_register(dest, a | b)


# Shift left of a 32-bit number.
def sllv(dest: str, src: str, operand: str, reg: Registers) -> None:
    a, b = reg.get_register(src), reg.get_register(operand)
    b %= 32
    reg.set_register(dest, (a << b) & WORD_MASK)


# Shift right of a 32-bit number.
def srav(dest: str, src: str, operand: str, reg: Registers) -> None:
    a, b = reg.get_register(src), reg.get_register(operand)
    b %= 32
    reg.set_register(dest, a >> b)


def srlv(dest: str, src: str, operand: str, reg: Registers) -> None:
    a, b = reg.get_register(src), reg.get_register(operand)
    b %= 32
    reg.set_register(dest, a >> b if a >= 0 else (a + 0x100000000) >> b)


# Bitwise XOR of two 32-bit numbers.
def xor(dest: str, src: str, operand: str, reg: Registers) -> None:
    a, b = reg.get_register(src), reg.get_register(operand)
    reg.set_register(dest, a ^ b)

# RTYPE 2 registers


def _abs(dest: str, src: str, reg: Registers, double: bool = False) -> None:
    a = reg.get_register(src, double=double)
    reg.set_register(dest, abs(a), double=double)


def ceil(dest: str, src: str, reg: Registers, double: bool = False) -> None:
    a = reg.get_register(src, double=double)
    value = convert_to_int(a, math.ceil)
    reg.set_register(dest, interpret_as_float(value), double=double)


def clo(dest: str, src: str, reg: Registers, is_zeroes: bool = False) -> None:
    src = to_unsigned(reg.get_register(src))
    # False -> 0 -> search for first 0
    temp = f"{src:032b}".find(str(int(is_zeroes)))
    if temp == -1:
        temp = 32
    reg.set_register(dest, temp)


def clz(dest: str, src: str, reg: Registers) -> None:
    return clo(dest, src, reg, is_zeroes=True)


def div(src: str, operand: str, reg: Registers, signed: bool = True) -> None:
    def sign(n: int) -> int:
        return -1 if n < 0 else 1

    a, b = reg.get_register(src), reg.get_register(operand)
    # Divide two 32-bit numbers
    if b == 0:
        raise ex.DivisionByZero(" ")
    elif signed:  # div
        result, remainder = int(a / b), abs(a) % abs(b) * sign(a)
    else:  # divu
        a_unsigned, b_unsigned = to_unsigned(a), to_unsigned(b)
        result, remainder = a_unsigned // b_unsigned, a_unsigned % b_unsigned

    reg.set_register('lo', result)
    reg.set_register('hi', remainder)


def floor(dest: str, src: str, reg: Registers, double: bool = False) -> None:
    a = reg.get_register(src, double=double)
    value = convert_to_int(a, math.floor)
    reg.set_register(dest, interpret_as_float(value), double=double)


def madd(src: str, operand: str, reg: Registers, signed: bool = True) -> None:
    hi, lo = reg.get_register('hi'), reg.get_register('lo')
    a, b = reg.get_register(src), reg.get_register(operand)
    low, high = mul_helper(a, b, thirty_two_bits=False, signed=signed)
    low, high = add_helper(lo, low, signed=signed), add_helper(
        hi, high, signed=signed)
    reg.set_register('lo', low)
    reg.set_register('hi', high)


def msub(src: str, operand: str, reg: Registers, signed: bool = True) -> None:
    hi, lo = reg.get_register('hi'), reg.get_register('lo')
    a, b = reg.get_register(src), reg.get_register(operand)
    low, high = mul_helper(a, b, thirty_two_bits=False, signed=signed)
    low, high = add_helper(
        lo, -low, signed=signed), add_helper(hi, -high, signed=signed)
    reg.set_register('lo', low)
    reg.set_register('hi', high)


def mult(src: str, operand: str, reg: Registers, signed: bool = True) -> None:
    a, b = reg.get_register(src), reg.get_register(operand)
    low, high = mul_helper(a, b, thirty_two_bits=False, signed=signed)
    reg.set_register('lo', low)
    reg.set_register('hi', high)


def mov(dest: str, src: str, reg: Registers, double: bool = False) -> None:
    reg.set_register(dest, reg.get_register(src, double=double), double=double)


def neg(dest: str, src: str, reg: Registers, double: bool = False) -> None:
    reg.set_register(
        dest, -(reg.get_register(src, double=double)), double=double)


def _round(dest: str, src: str, reg: Registers, double: bool = False) -> None:
    a = reg.get_register(src, double=double)
    value = convert_to_int(a, round)
    reg.set_register(dest, interpret_as_float(value), double=double)


def sqrt(dest: str, src: str, reg: Registers, double: bool = False) -> None:
    a = reg.get_register(src, double=double)
    if a < 0:
        value = float32('nan') if type(a) is float32 else float('nan')
    else:
        value = float32(math.sqrt(a)) if type(a) is float32 else math.sqrt(a)
    reg.set_register(dest, value, double=double)


def trunc(dest: str, src: str, reg: Registers, double: bool = False) -> None:
    a = reg.get_register(src, double=double)
    value = convert_to_int(a, math.trunc)
    reg.set_register(dest, interpret_as_float(value), double=double)

# IType Instructions


def addi(dest: str, src: str, imm: int, reg: Registers, signed: bool = True) -> None:
    a, b = reg.get_register(src), imm
    if not valid_immed(b):
        raise ex.InvalidImmediate("Immediate is not 16-bit")

    reg.set_register(dest, add_helper(a, b, signed=signed))


def slti(dest: str, src: str, imm: int, reg: Registers, signed: bool = True) -> None:
    a, b = reg.get_register(src), imm
    if not valid_immed(b):
        raise ex.InvalidImmediate("Immediate is not 16 bit")

    result = result = a < b if signed else a & 0xFFFFFFFF < b & 0xFFFFFFFF
    reg.set_register(dest, int(result))  # 1 if True else 0


def andi(dest: str, src: str, imm: int, reg: Registers) -> None:
    a, b = reg.get_register(src), imm
    if not valid_immed_unsigned(b):
        raise ex.InvalidImmediate("Immediate is not unsigned 16 bit")

    reg.set_register(dest, a & b)


def ori(dest: str, src: str, imm: int, reg: Registers) -> None:
    a, b = reg.get_register(src), imm
    if not valid_immed_unsigned(b):
        raise ex.InvalidImmediate("Immediate is not unsigned 16 bit")

    reg.set_register(dest, a | b)


def sll(dest: str, src: str, imm: int, reg: Registers) -> None:
    a, b = reg.get_register(src), imm
    if not valid_shamt(b):
        raise ex.InvalidImmediate("Shift amount is not 0-31")

    b %= 32
    reg.set_register(dest, (a << b) & WORD_MASK)


def sra(dest: str, src: str, imm: int, reg: Registers) -> None:
    a, b = reg.get_register(src), imm
    if not valid_shamt(b):
        raise ex.InvalidImmediate("Shift amount is not 0-31")

    b %= 32
    reg.set_register(dest, a >> b)


def srl(dest: str, src: str, imm: int, reg: Registers) -> None:
    a, b = reg.get_register(src), imm
    if not valid_shamt(b):
        raise ex.InvalidImmediate("Shift amount is not 0-31")

    b %= 32
    reg.set_register(dest, a >> b if a >= 0 else (a + 0x100000000) >> b)


def xori(dest: str, src: str, imm: int, reg: Registers) -> None:
    a, b = reg.get_register(src), imm
    if not valid_immed_unsigned(b):
        raise ex.InvalidImmediate("Immediate is not unsigned 16 bit")

    reg.set_register(dest, a ^ b)

# Load Instructions


def lui(dest: str, addr: int, reg: Registers) -> int:  # Special Load
    if not valid_immed_unsigned(addr):
        raise ex.InvalidImmediate("Immediate is not unsigned 16 bit")

    reg.set_register(dest, addr << 16)


# Load byte (unsigned).
def lb(dest: str, src: str, imm: int, mem: Memory, reg: Registers, signed: bool = True) -> None:
    '''Load byte from address into destination register.'''
    reg.set_register(dest, mem.getByte(
        reg.get_register(src) + imm, signed=signed))


# Load half word (unsigned).
def lh(dest: str, src: str, imm: int, mem: Memory, reg: Registers, signed: bool = True) -> None:
    '''Load half word from address into destination register.'''
    reg.set_register(dest, mem.getHWord(
        reg.get_register(src) + imm, signed=signed))


# Load word.
def lw(dest: str, src: str, imm: int, mem: Memory, reg: Registers) -> None:
    '''Load word from address into destination register.'''
    reg.set_register(dest, mem.getWord(reg.get_register(src) + imm))


def lwl(dest: str, src: str, imm: int, mem: Memory, reg: Registers) -> None:  # Load word left
    '''Load word left from address into destination register.'''
    addr = reg.get_register(src) + imm
    orig = reg.get_register(dest)
    word_start = addr - addr % 4
    result = 0

    for i in range(addr % 4 + 1):
        byte = mem.getByte(word_start + i, signed=False)
        alignment = 3 - addr % 4 + i
        result |= byte << (8 * alignment)

    mask = (1 << ((3 - addr % 4) * 8)) - 1
    reg.set_register(dest, (orig & mask) + result)


def lwr(dest: str, src: str, imm: int, mem: Memory, reg: Registers) -> None:  # Load word right
    '''Load word right from address into destination register.'''
    addr = reg.get_register(src) + imm
    orig = reg.get_register(dest)
    word_start = addr - addr % 4
    result = 0

    for i in range(4 - addr % 4):
        byte = mem.getByte(word_start + 3 - i, signed=False)
        alignment = 3 - i - addr % 4
        result |= byte << (8 * alignment)

    mask = ((1 << (addr % 4 * 8)) - 1) << ((4 - addr % 4) * 8)
    reg.set_register(dest, (orig & mask) + result)


def load_float(dest: str, src: str, imm: int, mem: Memory, reg: Registers, double: bool = False) -> None:
    '''Load the float or double from address into destination register.'''
    addr = reg.get_register(src) + imm
    value = mem.getDouble(addr) if double else mem.getFloat(addr)
    reg.set_register(dest, value, double=double)

# Store Instructions


# Store byte.
def sb(dest: str, src: str, imm: int, mem: Memory, reg: Registers) -> None:
    '''Store the given byte in the given memory address.'''
    data = reg.get_register(dest)
    mem.addByte(data, reg.get_register(src) + imm)


# Store half.
def sh(dest: str, src: str, imm: int, mem: Memory, reg: Registers) -> None:
    '''Store the given half word in the given memory address.'''
    data = reg.get_register(dest)
    mem.addHWord(data, reg.get_register(src) + imm)


# Store word.
def sw(dest: str, src: str, imm: int, mem: Memory, reg: Registers) -> None:
    '''Store the given word in the given memory address.'''
    data = reg.get_register(dest)
    mem.addWord(data, reg.get_register(src) + imm)

# Helper function for swl, swr


def _get_reg_byte(data: int, i: int) -> int:
    # Get the ith byte of a 32-bit integer
    return data >> (8 * i) & 0xFF


def swl(dest: str, src: str, imm: int, mem: Memory, reg: Registers) -> None:  # Store word left
    '''Store the given word left in the given memory address.'''
    addr = reg.get_register(src) + imm
    data = reg.get_register(dest)
    alignment = addr % 4
    word_start = addr - alignment

    for i in range(alignment + 1):
        byte = _get_reg_byte(data, 3 - i)
        mem.addByte(byte, word_start + alignment - i)


def swr(dest: str, src: str, imm: int, mem: Memory, reg: Registers) -> None:  # Store word right
    '''Store the given word right in the given memory address.'''
    addr = reg.get_register(src) + imm
    data = reg.get_register(dest)
    alignment = addr % 4
    word_start = addr - alignment

    for i in range(4 - alignment):
        byte = _get_reg_byte(data, i)
        mem.addByte(byte, word_start + alignment + i)


def store_float(dest: str, src: str, imm: int, mem: Memory, reg: Registers, double: bool = False) -> None:
    '''Store the given float or double data in the given memory address.'''
    data = reg.get_register(dest, double=double)
    if double:
        mem.addDouble(data, reg.get_register(src) + imm)
    else:
        mem.addFloat(data, reg.get_register(src) + imm)

# Branch Instructions


# Branch on equal to.
def beq(label: str, left: str, right: str, mem: Memory, reg: Registers) -> None:
    '''Set the program counter to the target address if left_value is
    equal to the right_value.'''
    if reg.get_register(left) == reg.get_register(right):
        reg.set_register('pc', mem.getLabel(label))


# Branch on greater than or equal to.
def bgez(label: str, src: int, mem: Memory, reg: Registers) -> None:
    '''Set the program counter to the target address if value is
    greater than or equal to 0.'''
    if reg.get_register(src) >= 0:
        reg.set_register('pc', mem.getLabel(label))


# Branch on greater than or equal to.
def bgezal(label: str, src: int, mem: Memory, reg: Registers) -> None:
    '''Set the return address register to the current program counter and 
    set the program counter to the target address if value is greater than 
    or equal to 0.'''
    if reg.get_register(src) >= 0:
        reg.set_register('$ra', reg.get_register('pc'))
        reg.set_register('pc', mem.getLabel(label))


# Branch on greater than.
def bgtz(label: str, src: int, mem: Memory, reg: Registers) -> None:
    '''Set the program counter to the target address if value is
    greater than 0.'''
    if reg.get_register(src) > 0:
        reg.set_register('pc', mem.getLabel(label))


def blez(label: str, src: int, mem: Memory, reg: Registers) -> None:  # Branch on less than or equal to 0
    '''Set the program counter to the target address if value is
    less than or equal to 0.'''
    if reg.get_register(src) <= 0:
        reg.set_register('pc', mem.getLabel(label))


def bltz(label: str, src: int, mem: Memory, reg: Registers) -> None:  # Branch on less than 0
    '''Set the program counter to the target address if value is
    less than 0.'''
    if reg.get_register(src) < 0:
        reg.set_register('pc', mem.getLabel(label))


def bltzal(label: str, src: int, mem: Memory, reg: Registers) -> None:  # Branch on less than 0
    '''Set the return address register to the current program counter and 
    set the program counter to the target address if value is less than 0.'''
    if reg.get_register(src) < 0:
        reg.set_register('$ra', reg.get_register('pc'))
        reg.set_register('pc', mem.getLabel(label))


# Branch on not equal to.
def bne(label: str, left: str, right: str, mem: Memory, reg: Registers) -> None:
    '''Set the program counter to the target address if left_value is
    not equal to the right_value.'''
    if reg.get_register(left) != reg.get_register(right):
        reg.set_register('pc', mem.getLabel(label))

# J TYPE INSTRUCTIONS


def jal(target: int, reg: Registers) -> None:  # Jump and link.
    '''Set the return address register to the current program counter and
    set the program counter to the target address.'''
    reg.set_register('$ra', reg.get_register('pc'))
    reg.set_register('pc', target)


def j(target: int, reg: Registers) -> None:  # Unconditional jump.
    '''Set the program counter to the target address.'''
    reg.set_register('pc', target)


def jalr(dest: str, src: str, target: str, reg: Registers) -> None:  # Jump and link register
    '''Set the return address register to the current program counter and 
    set the program counter to the value in the target register.'''
    reg.set_register(src, reg.get_register('pc'))
    reg.set_register(dest, reg.get_register(target))


def jr(dest: str, target: str, reg: Registers) -> None:  # Jump register
    '''Set the program counter to the value in the target register.'''
    reg.set_register(dest, reg.get_register(target))

# Compare instructions


def compare_equal(left_value: str, right_value: str, flag_num: int, flags: List[bool],
                  reg: Registers, double: bool = False) -> None:
    '''Set the given condition flag to True if the values are equal else False.'''
    left_value = reg.get_register(left_value, double=double)
    right_value = reg.get_register(right_value, double=double)
    flags[flag_num] = left_value == right_value


def compare_less_equal(left_value: str, right_value: str, flag_num: int, flags: List[bool],
                       reg: Registers, double: bool = False) -> None:
    '''Set the given condition flag to True if the left value is less than 
    or equal to the right value else False.'''
    left_value = reg.get_register(left_value, double=double)
    right_value = reg.get_register(right_value, double=double)
    flags[flag_num] = left_value <= right_value


def compare_less_than(left_value: str, right_value: str, flag_num: int, flags: List[bool],
                      reg: Registers, double: bool = False) -> None:
    '''Set the given condition flag to True if the left value is less than 
    the right value else False.'''
    left_value = reg.get_register(left_value, double=double)
    right_value = reg.get_register(right_value, double=double)
    flags[flag_num] = left_value < right_value

# Convert Instructions


def convert_single_to_double(dest: str, src: str, reg: Registers) -> None:  # cvt.d.s
    '''Convert from single precision value to double precision value.'''
    reg.set_reg_double(dest, float(reg.get_register(src)))


def convert_word_to_double(dest: str, src: str, reg: Registers) -> None:  # cvt.d.w
    '''Convert from word fixed point to double precision value.'''
    reg.set_reg_double(dest, float(reg.get_reg_word(src)))


def convert_double_to_single(dest: str, src: str, reg: Registers) -> None:  # cvt.s.d
    '''Convert from double precision value to single precision value.'''
    reg.set_register(dest, float32(reg.get_reg_double(src)))


def convert_word_to_single(dest: str, src: str, reg: Registers) -> None:  # cvt.s.d
    '''Convert from word fixed point to single precision value.'''
    reg.set_register(dest, float32(reg.get_reg_word(src)))


def convert_double_to_word(dest: str, src: str, reg: Registers) -> None:  # cvt.w.d
    '''Convert from double precision value to word fixed point.'''
    reg.set_reg_word(dest, int(reg.get_reg_double(src)))


def convert_single_to_word(dest: str, src: str, reg: Registers) -> None:  # cvt.w.s
    '''Convert from single precision value to word fixed point.'''
    reg.set_reg_word(dest, int(reg.get_register(src)))

# MoveCond Instructions


# movf{.s|d}
def movf(dest: str, src: str, flag_num: int, flags: List[bool], reg: Registers, double: bool = False) -> None:
    '''Move source register value to destination register if flag is False.'''
    if not flags[flag_num]:
        reg.set_register(dest, reg.get_register(
            src, double=double), double=double)


# movt{.s|d}
def movt(dest: str, src: str, flag_num: int, flags: List[bool], reg: Registers, double: bool = False) -> None:
    '''Move source register value to destination register if flag is True.'''
    if flags[flag_num]:
        reg.set_register(dest, reg.get_register(
            src, double=double), double=double)

# Branch Float Instructions


# bc1f
def bc1f(label: str, flag_num: int, mem: Memory, flags: List[bool], reg: Registers) -> None:
    '''Branch if flag is False.'''
    if not flags[flag_num]:
        reg.set_register('pc', mem.getLabel(label))


# bc1f
def bc1t(label: str, flag_num: int, mem: Memory, flags: List[bool], reg: Registers) -> None:
    '''Branch if flag is True.'''
    if flags[flag_num]:
        reg.set_register('pc', mem.getLabel(label))

# Move Float instruction


def mfc1(dest: str, src: str, reg: Registers) -> None:
    '''Set destination register to the contents of float register source.'''
    def interpret_as_int(x: float32) -> int:
        x_bytes = struct.pack('>f', x)
        return struct.unpack('>i', x_bytes)[0]

    reg.set_register(dest, interpret_as_int(reg.get_register(src)))


def mtc1(dest: str, src: str, reg: Registers) -> None:
    '''Set destination register to the contents of integer register source.'''
    def interpret_as_float(x: int) -> float32:
        x_bytes = struct.pack('>i', x)
        return struct.unpack('>f', x_bytes)[0]

    reg.set_register(dest, interpret_as_float(reg.get_register(src)))


# movn{.d|s}
def movn(dest: str, src: str, operand: str, reg: Registers, double: bool = False) -> None:
    '''Set single precision destination register to the contents of the 
    single precision source register if the contents of the operand register is not 0.'''
    conditional = reg.get_register(operand)
    if conditional != 0:
        reg.set_register(dest, reg.get_register(
            src, double=double), double=double)


# movz{.d|s}
def movz(dest: str, src: str, operand: str, reg: Registers, double: bool = False) -> None:
    '''Set single precision destination register to the contents of the 
    single precision source register if the contents of the operand register is 0.'''
    conditional = reg.get_register(operand)
    if conditional == 0:
        reg.set_register(dest, reg.get_register(
            src, double=double), double=double)


def move(dest: str, src: str, reg: Registers) -> None:  # mfhi, mflo, mthi, mtlo
    '''Set the destination register to the contents of the source register.'''
    reg.set_register(dest, reg.get_register(src))


instruction_translation_table = {
    'l.s': load_float,
    's.s': store_float,
    'b': j,
    'c.eq.s': compare_equal,
    'c.le.s': compare_less_equal,
    'c.lt.s': compare_less_than,
    'cvt.d.s': convert_single_to_double,
    'cvt.d.w': convert_word_to_double,
    'cvt.s.d': convert_double_to_single,
    'cvt.s.w': convert_word_to_single,
    'cvt.w.d': convert_double_to_word,
    'cvt.w.s': convert_single_to_word,
    'movf.s': movf,
    'movt.s': movt,
    'movn.s': movn,
    'movz.s': movz,
    'mfhi': move,
    'mflo': move,
    'mthi': move,
    'mtlo': move,
    'abs.s': _abs,
    'mov.s': mov,
    'neg.s': neg,
    'sqrt.s': sqrt,
    'ceil.w.s': ceil,
    'floor.w.s': floor,
    'round.w.s': _round,
    'trunc.w.s': trunc,
    'add.s': add_f,
    'div.s': div_f,
    'mul.s': mul_f,
    'sub.s': sub_f,
    'and': _and,
    'or': _or,
}


def get_instr(op: str) -> Callable:
    '''Returns the instruction that corresponds to the given operation string.'''
    if op in instruction_translation_table:
        return instruction_translation_table[op]
    return globals()[op]
