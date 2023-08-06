from collections import OrderedDict
import os
import random
import struct
import sys
from typing import Union, Tuple, Dict

from numpy import float32

import constants as const
from interpreter import exceptions as ex
from interpreter import utility
from settings import settings


class Registers:
    def __init__(self, toggle_garbage: bool = False):
        self.reg_initialized = set()
        self.reg = OrderedDict()
        self.init_registers(toggle_garbage)

    def init_registers(self, randomize: bool) -> None:
        for r in const.REGS:
            if f'initial_{r}' in settings.keys():
                self.reg[r] = settings[f'initial_{r}']
            elif randomize and r not in const.CONST_REGS:
                self.reg[r] = random.randint(0, 2 ** 32 - 1)
            else:
                self.reg[r] = 0

        for r in const.F_REGS:
            if randomize:
                random_bytes = os.urandom(4)
                self.reg[r] = float32(struct.unpack('>f', random_bytes)[0])
            else:
                self.reg[r] = float32(0.0)

    def get_register(self, reg: str, double: bool = False) -> Union[int, float32, float]:
        if reg[1:].isdigit() and int(reg[1:]) < 32:
            reg = const.REGS[int(reg[1:])]
        if reg not in self.reg:
            raise ex.InvalidRegister(f"{reg} is an invalid register.")
        if double:
            return self.get_reg_double(reg)
        if settings['warnings'] and reg not in const.CONST_REGS and reg not in self.reg_initialized:
            print(
                f'Reading from uninitialized register {reg}!', file=sys.stderr)
        if reg[1] == 'f':
            return self.reg[reg]
        return utility.overflow_detect(self.reg[reg])

    def set_register(self, reg: str, data: Union[int, float32, float], double: bool = False) -> None:
        if reg[1:].isdigit() and int(reg[1:]) < 32:
            reg = const.REGS[int(reg[1:])]
        if reg not in self.reg:
            raise ex.InvalidRegister(f"{reg} is an invalid register.")
        if double:
            self.set_reg_double(reg, data)
        else:
            if reg == '$zero':
                raise ex.WritingToZeroRegister(
                    'You can not change the value of the zero register.')
            self.reg_initialized.add(reg)
            self.reg[reg] = data if reg[1] == 'f' else utility.overflow_detect(
                data)

    def get_reg_double(self, reg: str) -> float:
        reg_number = int(reg[2:])
        if reg_number & 1:
            raise ex.InvalidRegister('Double-precision instructions can only be done'
                                     ' with even numbered registers')
        next_reg = f'$f{reg_number + 1}'
        double_bytes = struct.pack(
            '>f', self.reg[next_reg]) + struct.pack('>f', self.reg[reg])

        return struct.unpack('>d', double_bytes)[0]

    def set_reg_double(self, reg: str, data: float) -> None:
        reg_number = int(reg[2:])
        if reg_number & 1:
            raise ex.InvalidRegister('Double-precision instructions can only be done'
                                     ' with even numbered registers')
        next_reg = f'$f{reg_number + 1}'
        double_bytes = struct.pack('>d', data)
        self.reg[reg] = struct.unpack('>f', double_bytes[4:])[0]
        self.reg[next_reg] = struct.unpack('>f', double_bytes[:4])[0]

    def get_reg_word(self, reg: str) -> int:
        bytes = struct.pack('>f', self.reg[reg])
        return struct.unpack('>i', bytes)[0]

    def set_reg_word(self, reg: str, data: int) -> None:
        bytes = struct.pack('>i', data)
        self.reg[reg] = struct.unpack('>f', bytes)[0]

    def dump(self) -> None:
        '''Dump the contents in registers (REGS only).'''
        header = f'{"reg":4} {"hex":10} {"dec"}\n'
        rows = [f'{k:4} {utility.format_hex(value)} {utility.overflow_detect(value):d}'
                for k, value in self.reg.items() if k in const.REGS]
        return header + "\n".join(rows)
