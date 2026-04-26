#!/usr/bin/env python3

# ALU:  add, sub, and, or, xor, slt, sltu
# Shift: sll, srl, sra
# Rotate (Zbb): ror, rol
# Mul/Div: mul, mulh, mulhu, mulhsu, div, divu, rem, remu
# Load/Store: lw, lh, lhu, lb, lbu, sw, sh, sb

import argparse
import os
import sys

REG_REG_INSNS = {
    "add",
    "sub",
    "and",
    "or",
    "xor",
    "slt",
    "sltu",
    "mul",
    "mulh",
    "mulhu",
    "mulhsu",
    "div",
    "divu",
    "rem",
    "remu",
}
SHIFT_INSNS = {"sll", "srl", "sra"}
ZBB_INSNS = {"ror", "rol"}
LOAD_INSNS = {"lw", "lh", "lhu", "lb", "lbu"}
STORE_INSNS = {"sw", "sh", "sb"}
ALL_INSNS = REG_REG_INSNS | SHIFT_INSNS | ZBB_INSNS | LOAD_INSNS | STORE_INSNS

# body.S template — target-agnostic, included by wrapper.S
BODY_TEMPLATE = """\
# {instruction} | op1={op1} op2={op2} | repeats={repeats} | mode={mode}

    # operand setup
    li t0, {op1}
    li t1, {op2}

    rdcycle s0

.globl begin_measure
begin_measure:
{insn_block}
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
"""

BODY_LOADSTORE_TEMPLATE = """\
# {instruction} | op1={op1} | repeats={repeats} | mode={mode}

    # operand setup
    la t0, test_data
    li t1, {op1}

    rdcycle s0

.globl begin_measure
begin_measure:
{insn_block}
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0

.section .data
.align 4
test_data:
    .word 0xDEADBEEF
    .word 0xCAFEBABE
    .word 0x12345678
    .word 0x9ABCDEF0
"""

MAKEFILE_TEMPLATE = """\
# {test_name} | {instruction} | op1={op1} op2={op2} | reps={repeats} | mode={mode}
MARCH = {march}
TARGETS_DIR ?= ../../targets
ROM_SIZE = {rom_size}
STOP_TIME = {stop_time}ms

include $(TARGETS_DIR)/{target}/Makefile.inc
"""


def get_march(instruction):
    if instruction in {"mul", "mulh", "mulhu", "mulhsu", "div", "divu", "rem", "remu"}:
        return "rv32im_zicsr_zifencei"
    if instruction in ZBB_INSNS:
        return "rv32i_zbb_zicsr_zifencei"
    return "rv32i_zicsr_zifencei"


def make_insn_line(instruction, mode):
    if instruction in LOAD_INSNS:
        return f"    {instruction} t2, 0(t0)"
    if instruction in STORE_INSNS:
        return f"    {instruction} t1, 0(t0)"
    if mode == "accum":
        return f"    {instruction} t0, t0, t1"
    return f"    {instruction} t2, t0, t1"


def make_insn_block(instruction, repeats, mode):
    line = make_insn_line(instruction, mode)
    if repeats > 1:
        return f".rept {repeats}\n{line}\n.endr"
    return line


def estimate_stop_time_ms(repeats, cycles_per_insn=2):
    cycles = repeats * cycles_per_insn + 1000
    return max(1, int((cycles * 10) / 1_000_000 + 1))


def estimate_rom_size(repeats):
    raw = repeats * 4 + 512
    size = 4096
    while size < raw:
        size *= 2
    return f"{size // 1024}k"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instruction", required=True)
    parser.add_argument("-o1", "--operand-1", required=True)
    parser.add_argument("-o2", "--operand-2", required=True)
    parser.add_argument("-r", "--repeats", type=int, default=1000)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument(
        "-m", "--mode", default="static", choices=["static", "accum", "single"]
    )
    parser.add_argument(
        "-t", "--target", default="neorv32", choices=["neorv32", "picorv32"]
    )
    args = parser.parse_args()

    instruction = args.instruction.lower()
    if instruction not in ALL_INSNS:
        print(f"unknown: {instruction}\nsupported: {sorted(ALL_INSNS)}")
        sys.exit(1)

    repeats = 1 if args.mode == "single" else args.repeats

    insn_block = make_insn_block(instruction, repeats, args.mode)

    if instruction in LOAD_INSNS | STORE_INSNS:
        body = BODY_LOADSTORE_TEMPLATE.format(
            instruction=instruction,
            op1=args.operand_1,
            op2=args.operand_2,
            repeats=repeats,
            mode=args.mode,
            insn_block=insn_block,
        )
    else:
        body = BODY_TEMPLATE.format(
            instruction=instruction,
            op1=args.operand_1,
            op2=args.operand_2,
            repeats=repeats,
            mode=args.mode,
            insn_block=insn_block,
        )

    makefile = MAKEFILE_TEMPLATE.format(
        test_name=os.path.basename(args.output),
        instruction=instruction,
        op1=args.operand_1,
        op2=args.operand_2,
        repeats=repeats,
        mode=args.mode,
        target=args.target,
        march=get_march(instruction),
        rom_size=estimate_rom_size(repeats),
        stop_time=estimate_stop_time_ms(repeats),
    )

    os.makedirs(args.output, exist_ok=True)
    with open(os.path.join(args.output, "body.inc"), "w") as f:
        f.write(body)
    with open(os.path.join(args.output, "Makefile"), "w") as f:
        f.write(makefile)

    print(
        f"{args.output}/ | {instruction} | {args.mode} | {args.target} | reps={repeats}"
    )


if __name__ == "__main__":
    main()
