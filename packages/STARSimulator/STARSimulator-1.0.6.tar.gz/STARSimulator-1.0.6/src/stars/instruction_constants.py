# I-type encoding:
# op rt, rs, imm -> op REG REG NUMBER
ITYPE_1 = ["addi", "addiu", "andi", "ori", "slti", "sltiu", "xori"]
# op rt, offset(base) (= op, rt, base, offset) -> op REG NUMBER(REG)
# op rt, base (= op, rt, base, 0) -> op REG, REG
# op rt, label (= op, rt, addr(label), 0) -> op REG LABEL
ITYPE_2 = ["l.d", "l.s", "lb", "lbu", "lh", "lhu", "lw", "lwl", "lwr",
           "s.d", "s.s", "sb", "sh", "sw", "swl", "swr"]
# op rt, immediate (= op rt, $0, imm) -> op REG NUMBER
ITYPE_3 = ["lui"]


# Branch Extends I-Type
# op rs, rt, offset (offset = label) -> op REG REG LABEL
BRANCH_1 = ["beq", "bne"]
# op rs, offset (= op rs, $0, offset) -> op REG LABEL
BRANCH_2 = ["bgez", "bgezal", "bgtz", "blez", "blitz", "bltzal"]
# op cc, offset [cc between 0-7]  -> op NUMBER LABEL
# op offset (= op, 0, offset) -> op LABEL
BRANCH_3 = ["bclf", "bclt"]

# J-type encoding:
# op target -> op LABEL
JTYPE_1 = ["j", "jal", "b"]
# op rs -> op REG
JTYPE_2 = ["jr"]  # technically RTYPE


# R-type encoding:
# op rd, rs, rt -> op REG REG REG
RTYPE_1 = ["add", "addu",  "and", "mul", "sub", "subu",
           "movn", "movz", "nor", "or", "xor",
           "slt", "sltu", "sllv", 'srav', "srlv"]
# op rd, rs (= op, rd, rs, 0) -> op REG REG
RTYPE_2 = ["clo", "clz"]
# op rs (= op, rd=HI/LO, rs, 0) -> OP REG
# op rd (= op, rd, rs=HI/LO, 0)
RTYPE_3 = ["mthi", "mtlo", "mfhi", "mflo"]  # Move currently
# op rd, rs, cc (= op, rd, rs, rt=cc) -> op REG REG NUMBER
RTYPE_4 = ["movf", "movt"]
# op rs, rt (= op, 0, rs, rt) -> op REG REG
RTYPE_5 = ["div", "divu", "madd", "maddu", "msub", "msubu", "mult", "multu"]
# op, rd, rs, sa (= op, rd, rs, rt=sa) [sa between 0-31] -> op REG REG NUMBER
RTYPE_6 = ["sll", "sra", "srl"]
# op [rd,], rs -> op REG; op REG REG (rd default to $ra)
RTYPE_7 = ["jalr"]

# Float R-type (extends R-type)
# op.fmt fd, fs, ft (= op.fmt fd, fs, ft=0) -> op F_REG F_REG F_REG
FLOAT_RTYPE_1 = ["add.fmt", "div.fmt", "mul.fmt", "sub.fmt"]
# op.fmt fd, fs, rt -> op F_REG F_REG REG
FLOAT_RTYPE_2 = ["movn.fmt", "movz.fmt"]
# op.fmt fd, fs (= op.fmt fd, fs, ft=0) -> op F_REG F_REG
FLOAT_RTYPE_3 = ["ceil.w.fmt", "floor.w.fmt", "round.w.fmt",
                 "abs.fmt", "neg.fmt", "sqrt.fmt", 'trunc.fmt',
                 "cvt.d.fmt", 'cvt.s.fmt', "cvt.w.fmt", 'mov.fmt']
# op.fmt fd, fs, cc(0-7, 0 default) (= op.fmt fd, fs, ft=cc) -> op F_REG F_REG NUMBER
# op.fmt fd, fs = (op.fmt fd, fs, cc=0) -> op F_REG F_REG
FLOAT_RTYPE_4 = ["movf.fmt", "movt.fmt"]
# c.cond.fmt cc, fs, ft -> op NUMBER F_REG F_REG
# c.cond.fmt fs, ft (= c.cond.fmt 0, fs, ft) -> op F_REG F_REG
# cond = {eq, le, lt}, fmt = {d, s}
FLOAT_RTYPE_5 = [r'\b(c\.(eq|le|lt)\.[sd])\b']
# op rt, fs -> op REG F_REG (LIKE AN ITYPE)
FLOAT_RTYPE_6 = ["mfc1", "mtc1"]

# break [code] -> op NUMBER
SPECIAL_1 = ["break"]
# op -> op
SPECIAL_2 = ["nop", "syscall"]

# Pseudo Instruction:
# abs, beqz, bge, bgeu, bgt, bgtu, ble, bleu, blt, bltu, bnez, la, li, move, neg, not, rol, ror, seq, sge, sgeu, sgt, sgtu, sle, sleu, sne


ALL = ITYPE_1 + ITYPE_2 + ITYPE_3
ALL += JTYPE_1 + JTYPE_2
ALL += RTYPE_1 + RTYPE_2 + RTYPE_3 + RTYPE_4 + RTYPE_5 + RTYPE_6 + RTYPE_7
ALL += FLOAT_RTYPE_1 + FLOAT_RTYPE_2 + FLOAT_RTYPE_3 + \
    FLOAT_RTYPE_4 + FLOAT_RTYPE_5 + FLOAT_RTYPE_6
ALL += SPECIAL_1 + SPECIAL_2


# # Operators w/ immediates
# ITYPE_1 = tokenize_list(ITYPE_1)
# # Loads and store instructions
# ITYPE_2 = tokenize_list(ITYPE_2)
# # lui special load
# ITYPE_3 = tokenize_list(ITYPE_3)

# # Branch equality
# BRANCH_1 = tokenize_list(BRANCH_1)
# # Branch (in)equality against zero
# BRANCH_2 = tokenize_list(BRANCH_2)
# # Branch depending on coprocessor 1 condition flag
# BRANCH_3 = tokenize_list(BRANCH_3)

# # Jump instructions
# JTYPE_1 = tokenize_list(JTYPE_1)
# # Jump register
# JTYPE_2 = tokenize_list(JTYPE_2)

# # Operations; Move/Set if zero or not; Variable shifts
# RTYPE_1 = tokenize_list(RTYPE_1)
# # Count leading ones/zeroes
# RTYPE_2 = tokenize_list(RTYPE_2)
# # HI/LO move instructions
# RTYPE_3 = tokenize_list(RTYPE_3)
# # Move depending on coprocessor 1 condition flag
# RTYPE_4 = tokenize_list(RTYPE_4)
# # Operation involving HI/LO registers
# RTYPE_5 = tokenize_list(RTYPE_5)
# # Shifts w/ shamat
# RTYPE_6 = tokenize_list(RTYPE_6)
# # Jump and link register
# RTYPE_7 = tokenize_list(RTYPE_7)

CURRENT_ITYPE = ITYPE_1 + RTYPE_6
CURRENT_RTYPE3 = RTYPE_1 + FLOAT_RTYPE_1
CURRENT_RTYPE2 = RTYPE_2 + RTYPE_5 + FLOAT_RTYPE_3  # -convert functions
CURRENT_BRANCH = BRANCH_1 + BRANCH_2
CURRENT_MOVE_FLOAT = FLOAT_RTYPE_2 + FLOAT_RTYPE_6

instruction_list = [
    'abs', 'abs.d', 'abs.s', 'add', 'add.d', 'add.s', 'addi', 'addiu', 'addu', 'and', 'andi',
    'b', 'bc1f', 'bc1t', 'beq', 'beqz', 'bge', 'bgeu', 'bgez', 'bgezal', 'bgt', 'bgtu', 'bgtz',
    'ble', 'bleu', 'blez', 'blt', 'bltu', 'bltz', 'bltzal', 'bne', 'bnez', 'break', 'c.eq.d',
    'c.eq.s', 'c.le.d', 'c.le.s', 'c.lt.d', 'c.lt.s', 'ceil.w.d', 'ceil.w.s', 'clo', 'clz',
    'cvt.d.s', 'cvt.d.w', 'cvt.s.d', 'cvt.s.w', 'cvt.w.d', 'cvt.w.s', 'div', 'div.d', 'div.s',
    'divu', 'floor.w.d', 'floor.w.s', 'j', 'jal', 'jalr', 'jr', 'l.d', 'l.s', 'la', 'lb', 'lb',
    'lbu', 'lbu', 'lh', 'lh', 'lhu', 'lhu', 'li', 'li', 'li', 'lui', 'lw', 'lw', 'lwl', 'lwl',
    'lwr', 'lwr', 'madd', 'maddu', 'mfc1', 'mfhi', 'mflo', 'mov.d', 'mov.s', 'move', 'movf',
    'movf.d', 'movf.s', 'movn', 'movn.d', 'movn.s', 'movt', 'movt.d', 'movt.s', 'movz', 'movz.d',
    'movz.s', 'msub', 'msubu', 'mtc1', 'mthi', 'mtlo', 'mul', 'mul.d', 'mul.s', 'mult', 'multu',
    'neg', 'neg.d', 'neg.s', 'nop', 'nor', 'not', 'or', 'ori', 'rol', 'ror', 'round.w.d',
    'round.w.s', 's.d', 's.s', 'sb', 'sb', 'seq', 'sge', 'sgeu', 'sgt', 'sgtu', 'sh', 'sh',
    'sle', 'sleu', 'sll', 'sllv', 'slt', 'slti', 'sltiu', 'sltu', 'sne', 'sqrt.d', 'sqrt.s',
    'sra', 'srav', 'srl', 'srlv', 'sub', 'sub.d', 'sub.s', 'subu', 'sw', 'sw', 'swl', 'swl',
    'swr', 'swr', 'syscall', 'trunc.w.d', 'trunc.w.s', 'xor', 'xori'
]

pseudo_instrs = [
    'abs', 'beqz', 'bge', 'bgeu', 'bgt', 'bgtu', 'ble', 'bleu', 'blt', 'bltu', 'bnez', 'la',
    'li', 'move', 'neg', 'not', 'rol', 'ror', 'seq', 'sge', 'sgeu', 'sgt', 'sgtu', 'sle',
    'sleu', 'sne'
]

special = SPECIAL_1 + SPECIAL_2

signed_functions = set()
doubled = set()

missing = set()
sub_cat = set()
if __name__ == "__main__":
    from interpreter import instructions as instrs
    for x in instruction_list:
        if x not in pseudo_instrs and x not in special:
            if x[-1] == 'u':
                signed_functions.add(x)
                x = x[:-1]
            if x.split('.')[-1] == 'd' and x.split('.')[0] != 'cvt':
                doubled.add(x)
                x = '.'.join(x.split('.')[:-1]+['s'])
            try:
                instrs.table[x]
            except:
                sub = x.split('.')[0]
                if sub in instrs.table:
                    sub_cat.add(x)
                else:
                    missing.add(x)

    print(sorted(list(signed_functions)))
    print(sorted(list(doubled)))
    print(missing)
    print(sub_cat)
