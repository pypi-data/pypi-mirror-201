from collections import OrderedDict
import os
import re
from interpreter.classes import *
# from sbumips.src.stars import settings


# def check_function_bruteforce(func_name, func_instructions, net_id):
#     regdests = set()
#     stored_sregs = set()
#     stored_tregs = set()
#     read_registers = set()
#     # Matches stack push for a,t,v,s registers, ignores ra
#     # stack_store = re.compile('\s*sw\s*\$[astv]\d{1,2}\s*,?\s*-?\d{0,3}\(\s*\$sp\s*\)')
#     # currently checking only for unnecessary pushing of $s registers
#     stack_store_sreg = re.compile(
#         r'\s*sw\s+\$s\d{1,2}\s*,?\s*-?\d{0,3}\(\s*\$sp\s*\)')
#     stack_store_treg = re.compile(
#         r'\s*sw\s+\$t\d{1,2}\s*,?\s*-?\d{0,3}\(\s*\$sp\s*\)')
#     # Matches stack push for $ra
#     ra_stack_store = re.compile(r'\s*sw\s+\$ra\s*,?\s*-?\d{0,3}\(\s*\$sp\s*\)')
#     function_call = re.compile(r'\s*jal\s+.*')
#     # stack_load = re.compile('\s*lw\s*\$(t|a|s|v|ra)\d{1,2}\s*,?\s*-?\d{0,3}\(\s*\$sp\s*\)')
#     stack_load = re.compile(
#         r'\s*lw\s+\$(s|ra)\d{1,2}\s*,?\s*-?\d{0,3}\(\s*\$sp\s*\)')
#     ra_was_saved = False
#     function_is_caller = False
#     # ignored_instructions = ['b', 'beq', 'bne', 'blt', 'blez', 'bltz', 'ble', 'bgt',
#     #                       'bgez', 'bgtz', 'beqz', 'bnez', 'bge',  'j', 'jr']
#     ignored_instructions = ['j', 'b']
#     for inst in func_instructions:
#         if inst.split()[0] in ignored_instructions:
#             continue
#         # if net_id == 'jo' and inst.strip().startswith('li'):
#         #     print(func_name, inst)
#         regdest_index = inst.find('$')
#         regdest = inst[regdest_index:regdest_index + 3]

#         regsrc_index1 = inst.find('$', regdest_index+1)
#         read_register1 = None
#         if regsrc_index1 != -1:
#             read_register1 = inst[regsrc_index1:regsrc_index1 + 3]

#         read_register2 = None
#         if read_register1:
#             regsrc_index2 = inst.find('$', regsrc_index1 + 1)
#             read_register2 = inst[regsrc_index2:regsrc_index2 + 3]

#         if ra_stack_store.match(inst):  # Check if ra was saved
#             ra_was_saved = True
#             stored_sregs.add(regdest)
#             continue

#         # Check if s register was saved(excluding ra)
#         if stack_store_sreg.match(inst):
#             stored_sregs.add(regdest)
#             continue

#         if stack_store_treg.match(inst):
#             stored_tregs.add(regdest)  # print(net_id, inst)

#         # Check if there is a nested function call, negates ra being saved
#         if function_call.match(inst):
#             function_is_caller = True
#             read_registers.add('$ra')
#             continue

#         # For a function that takes arguments only through $a registers, the
#         # only reason to lw $s is for the sake of implementing register conventions.
#         # if stack_load.match(inst):
#         #      continue

#         if not stack_load.match(inst):
#             regdests.add(regdest)
#         if read_register1:
#             read_registers.add(read_register1)
#         if read_register2:
#             read_registers.add(read_register2)

#     if len(stored_tregs) >= 3:  # possible brute-force saving of $t registers
#         print('Possible brute-force saving of $t registers:', net_id, func_name)

#     unnecessary_stores = stored_sregs - regdests - read_registers
#     if ra_was_saved and not function_is_caller:
#         unnecessary_stores.add('$ra')
#     brute_forced = len(unnecessary_stores) > 0

#     brute_force_manual = {}
#     try:
#         with open('brute_force_manual.csv') as csv_file:
#             for line in csv_file:
#                 line = line.split(',')
#                 brute_force_manual[(line[0], line[1])] = line[2].strip()
#     except FileNotFoundError:
#         pass  # print('Code edits CSV file not found.')

#     # print(brute_force_manual)

#     # VERY HACKY!!!
#     for pair in brute_force_manual:
#         if pair[0] == net_id and pair[1] == func_name:
#             unnecessary_stores.add(brute_force_manual[pair])
#         # print(brute_force_manual[id])

#     report = ''
#     if brute_forced:
#         unnecessary_stores = ' '.join(sorted(unnecessary_stores))
#         report = f'    Registers preserved unnecessarily in {func_instructions[0]} {unnecessary_stores}'
#     else:
#         # check if the function was implemented
#         details_file = open(
#             os.path.join(os.path.abspath(settings['gradesheets_dir']), 'details', net_id + '_details.txt'))
#         details = details_file.readlines()
#         details_file.close()

#         if len(func_instructions) == 0 or any(f'{func_instructions[0]} No function implementation found. Aborting test.' in line for line in details):
#             report = f'    No implementation found for {func_name}'

#     return report


def check_function_uninit(func_name, func_instructions):
    reg_first_read = OrderedDict()
    reg_first_write = OrderedDict()
    ignored_regs = ['$sp', '$fp', '$ra', '$k0', '$k1', '$a0',
                    '$a1', '$a2', '$a3', '$v0', '$v1', '$0', '$ze']
    warnings = []
    ignored_instructions = ['j', 'sw', 'jal', 'syscall', 'jr']
    for inst in func_instructions:
        if str(inst).split()[0] in ignored_instructions:
            continue
        regdest_index = str(inst).find('$')
        regdest = str(
            inst)[regdest_index:regdest_index + 3].strip(' ,')
        regsrc_index1 = str(inst).find('$', regdest_index+1)
        read_register1 = None
        if regsrc_index1 != -1:
            read_register1 = str(
                inst)[regsrc_index1:regsrc_index1 + 3].strip(' ,')
        read_register2 = None
        if read_register1:
            regsrc_index2 = str(inst).find('$', regsrc_index1 + 1)
            if regsrc_index2 != -1:
                read_register2 = str(
                    inst)[regsrc_index2:regsrc_index2 + 3].strip(' ,')

        if regdest not in reg_first_write:
            # print(type(inst))
            if type(inst) is PseudoInstr:
                reg_first_write[regdest] = str(
                    inst.instrs[0].filetag)
            else:
                reg_first_write[regdest] = str(inst.filetag)
        for reg in [read_register1, read_register2]:
            if reg is not None and reg not in reg_first_read and reg not in ignored_regs:
                if type(inst) is PseudoInstr:
                    reg_first_read[reg] = str(inst.instrs[0].filetag)
                else:
                    reg_first_read[reg] = str(inst.filetag)

    for reg in reg_first_read:
        if reg not in reg_first_write:
            warnings.append(
                f'{func_name} function, line {reg_first_read[reg]}: register {reg} read without initialization')
            # print(net_id, warnings[-1])
            # print(net_id, func_name, 'line', reg_first_read[reg], reg, 'read but never written')
        elif reg_first_write[reg] >= reg_first_read[reg]:
            warnings.append(
                f'{func_name} function, line {reg_first_read[reg]}: register {reg} read before initialization (initialized line {reg_first_write[reg]})')
            # print(net_id, warnings[-1])
            # print(net_id, func_name, reg, 'read line', reg_first_read[reg], 'but written line', reg_first_write[reg])

    return warnings
