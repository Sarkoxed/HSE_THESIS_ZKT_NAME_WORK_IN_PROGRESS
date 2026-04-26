#!/usr/bin/env python3

# instructions
# ALU:  add, sub, and, or, xor, slt, sltu
# Shift: sll, srl, sra (op2 = shift amount 0-31)
# Rotate (Zbb): ror, rol
# Mul/Div: mul, mulh, mulhu, div, divu, rem, remu
# Load/Store: lw, lh, lhu, lb, lbu, sw, sh, sb

import argparse
import os
import sys

TEMPLATE = """\
.section .text
.globl main

main:
    # --- operand setup ---
    li t0, {op1}
    li t1, {op2}

    # --- measured block: {repeats}x {instruction} ---
.globl begin_measure
begin_measure:
{body}
.globl end_measure
end_measure:

    # --- return ---
    li a0, 0
    ret
"""

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

LOAD_STORE_TEMPLATE = """\
.section .text
.globl main

main:
    # --- operand setup ---
    la t0, test_data
    li t1, {op1}

    # --- measured block: {repeats}x {instruction} ---
.globl begin_measure
begin_measure:
{body}
.globl end_measure
end_measure:

    # --- return ---
    li a0, 0
    ret

.section .data
.align 4
test_data:
    .word 0xDEADBEEF
    .word 0xCAFEBABE
    .word 0x12345678
    .word 0x9ABCDEF0
"""

MAKEFILE_TEMPLATE = """\
# Auto-generated test: {test_name}
# Instruction: {instruction}, op1={op1}, op2={op2}, repeats={repeats}

MARCH = {march}
RISCV_PREFIX ?= riscv32-unknown-elf-
EFFORT = -Os

USER_FLAGS += -Wl,--defsym,__neorv32_rom_size={rom_size}
USER_FLAGS += -Wl,--defsym,__neorv32_ram_size=8k

NEORV32_HOME ?= ../../cores/neorv32

include $(NEORV32_HOME)/sw/common/common.mk

STOP_TIME ?= {stop_time}ms

sim: install
\tcd $(NEORV32_HOME)/sim && bash ghdl.sh --stop-time=$(STOP_TIME)

parse:
\tpython3 ../../scripts/neorv32/parse_trace.py -e main.elf -l $(NEORV32_HOME)/sim/neorv32.tracer0.log

run: sim parse
"""


def get_march(instruction):
    march = "rv32i_zicsr_zifencei"
    if instruction in {"mul", "mulh", "mulhu", "mulhsu", "div", "divu", "rem", "remu"}:
        march = "rv32im_zicsr_zifencei"
    elif instruction in ZBB_INSNS:
        march = "rv32i_zbb_zicsr_zifencei"
    return march


def generate_body(instruction, repeats=1, mode="static"):
    if instruction in LOAD_INSNS:
        line = f"    {instruction} t2, 0(t0)"
    elif instruction in STORE_INSNS:
        line = f"    {instruction} t1, 0(t0)"
    elif mode == "accum":
        line = f"    {instruction} t0, t0, t1"
    else:
        line = f"    {instruction} t2, t0, t1"
    if repeats > 1:
        return f".rept {repeats}\n" + line + '\n.endr'
    return line


def estimate_stop_time_ms(repeats, cycles_per_insn=2):
    cycles = repeats * cycles_per_insn + 1000
    ms = (cycles * 10) / 1_000_000  # 10ns per cycle at 100MHz
    return max(1, int(ms + 1))


def estimate_rom_size(repeats):
    # instruction - 4 bytes, overhead (~256 bytes for crt0 + setup)
    raw = repeats * 4 + 512

    # [4k, next power of 2]
    size = 4096
    while size < raw:
        size *= 2
    return f"{size // 1024}k"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instruction", required=True, help="")
    parser.add_argument("-o1", "--operand-1", required=True, help="lhs")
    parser.add_argument("-o2", "--operand-2", required=True, help="rhs/shift")
    parser.add_argument(
        "-r", "--repeats", required=False, type=int, default=1, help="reps"
    )
    parser.add_argument("-o", "--output", required=True, help="output dir")
    parser.add_argument("-m", "--mode", default="static", choices=["static", "accum"])

    args = parser.parse_args()

    instruction = args.instruction.lower()
    op1 = args.operand_1
    op2 = args.operand_2
    repeats = args.repeats
    output_dir = args.output
    mode = args.mode

    if instruction not in ALL_INSNS:
        print(f"unknown instruction '{instruction}'")
        print(f"supported: {sorted(ALL_INSNS)}")
        sys.exit(1)

    op1_short = op1.replace("0x", "")
    op2_short = op2.replace("0x", "")
    test_name = f"{instruction}_{op1_short}_{op2_short}"

    os.makedirs(output_dir, exist_ok=True)

    body = generate_body(instruction, repeats, mode)
    template = LOAD_STORE_TEMPLATE if instruction in LOAD_INSNS | STORE_INSNS else TEMPLATE
    asm_content = template.format(
        instruction=instruction,
        op1=op1,
        op2=op2,
        repeats=repeats,
        body=body,
    )

    march = get_march(instruction)

    makefile_content = MAKEFILE_TEMPLATE.format(
        test_name=test_name,
        instruction=instruction,
        op1=op1,
        op2=op2,
        repeats=repeats,
        march=march,
        rom_size=estimate_rom_size(repeats),
        stop_time=estimate_stop_time_ms(repeats),
    )

    asm_path = os.path.join(output_dir, "main.S")
    makefile_path = os.path.join(output_dir, "Makefile")

    with open(asm_path, "w") as f:
        f.write(asm_content)

    with open(makefile_path, "w") as f:
        f.write(makefile_content)

    print(f"Generated test: {output_dir}/")
    print(f"  Instruction: {instruction}")
    print(f"  Operands:    {op1}, {op2}")
    print(f"  Repeats:     {repeats}")
    print(f"  MARCH:       {march}")
    print(f"  ROM size:    {estimate_rom_size(repeats)}")


if __name__ == "__main__":
    main()
