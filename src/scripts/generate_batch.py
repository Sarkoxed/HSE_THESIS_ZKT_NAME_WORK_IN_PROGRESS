#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

TESTS = [
    (
        "add",
        [
            ("0x00000000", "0x00000000", "zeros"),
            ("0x7FFFFFFF", "0x7FFFFFFF", "max_positive"),
            ("0x80000000", "0x80000000", "min_negative"),
            ("0xAAAAAAAA", "0x55555555", "alternating"),
            ("0x12345678", "0x9ABCDEF0", "random"),
        ],
    ),
    (
        "xor",
        [
            ("0x00000000", "0x00000000", "zeros"),
            ("0xFFFFFFFF", "0x00000000", "ones_zeros"),
            ("0xAAAAAAAA", "0x55555555", "alternating"),
            ("0x12345678", "0x9ABCDEF0", "random"),
            ("0xFFFFFFFF", "0xFFFFFFFF", "all_ones"),
        ],
    ),
    (
        "sub",
        [
            ("0x00000000", "0x00000000", "zeros"),
            ("0x7FFFFFFF", "0x7FFFFFFF", "equal_max"),
            ("0x80000000", "0x7FFFFFFF", "underflow"),
            ("0x12345678", "0x9ABCDEF0", "random"),
        ],
    ),
    (
        "and",
        [
            ("0x00000000", "0xFFFFFFFF", "zero_mask"),
            ("0xFFFFFFFF", "0xFFFFFFFF", "all_ones"),
            ("0xAAAAAAAA", "0x55555555", "no_overlap"),
            ("0x12345678", "0x9ABCDEF0", "random"),
        ],
    ),
    (
        "or",
        [
            ("0x00000000", "0x00000000", "zeros"),
            ("0xAAAAAAAA", "0x55555555", "full_merge"),
            ("0x12345678", "0x9ABCDEF0", "random"),
        ],
    ),
    (
        "sll",
        [
            ("0x00000001", "0x00000000", "shift_0"),
            ("0x00000001", "0x00000001", "shift_1"),
            ("0x00000001", "0x00000010", "shift_16"),
            ("0x00000001", "0x0000001F", "shift_31"),
            ("0x12345678", "0x00000008", "random_shift_8"),
        ],
    ),
    (
        "srl",
        [
            ("0x80000000", "0x00000000", "shift_0"),
            ("0x80000000", "0x00000001", "shift_1"),
            ("0x80000000", "0x00000010", "shift_16"),
            ("0x80000000", "0x0000001F", "shift_31"),
        ],
    ),
    (
        "sra",
        [
            ("0x80000000", "0x00000000", "shift_0"),
            ("0x80000000", "0x00000001", "shift_1"),
            ("0x80000000", "0x00000010", "shift_16"),
            ("0x80000000", "0x0000001F", "shift_31"),
            ("0x7FFFFFFF", "0x0000001F", "positive_shift_31"),
        ],
    ),
    (
        "slt",
        [
            ("0x00000001", "0x00000002", "less"),
            ("0x00000002", "0x00000001", "greater"),
            ("0xFFFFFFFF", "0x00000000", "neg_vs_zero"),
            ("0x80000000", "0x7FFFFFFF", "min_vs_max"),
        ],
    ),
    (
        "mul",
        [
            ("0x00000001", "0x00000001", "ones"),
            ("0x0000FFFF", "0x0000FFFF", "medium"),
            ("0x7FFFFFFF", "0x00000002", "large"),
            ("0x12345678", "0x9ABCDEF0", "random"),
            ("0x00000000", "0xFFFFFFFF", "zero"),
        ],
    ),
    (
        "div",
        [
            ("0x0000000F", "0x00000003", "small"),
            ("0x7FFFFFFF", "0x00000002", "large_by_2"),
            ("0xFFFFFFFF", "0x00000003", "neg_by_3"),
            ("0x12345678", "0x00000011", "random_by_17"),
        ],
    ),
    # Zbb rotate
    (
        "ror",
        [
            ("0x12345678", "0x00000000", "rot_0"),
            ("0x12345678", "0x00000001", "rot_1"),
            ("0x12345678", "0x00000010", "rot_16"),
            ("0x12345678", "0x0000001F", "rot_31"),
        ],
    ),
    (
        "rol",
        [
            ("0x12345678", "0x00000000", "rot_0"),
            ("0x12345678", "0x00000001", "rot_1"),
            ("0x12345678", "0x00000010", "rot_16"),
            ("0x12345678", "0x0000001F", "rot_31"),
        ],
    ),
    # Load
    (
        "lw",
        [
            ("0xDEADBEEF", "0x00000000", "word"),
            ("0x00000000", "0x00000000", "word_zero"),
        ],
    ),
    (
        "lh",
        [
            ("0xDEADBEEF", "0x00000000", "half"),
        ],
    ),
    (
        "lb",
        [
            ("0xDEADBEEF", "0x00000000", "byte"),
        ],
    ),
    # Store
    (
        "sw",
        [
            ("0xDEADBEEF", "0x00000000", "word"),
            ("0x00000000", "0x00000000", "word_zero"),
        ],
    ),
    (
        "sh",
        [
            ("0xDEADBEEF", "0x00000000", "half"),
        ],
    ),
    (
        "sb",
        [
            ("0xDEADBEEF", "0x00000000", "byte"),
        ],
    ),
]

REPEATS = 1000

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="generated")
    parser.add_argument("-r", "--repeats", type=int, default=REPEATS)
    args = parser.parse_args()

    LOAD_STORE = {"lw", "lh", "lhu", "lb", "lbu", "sw", "sh", "sb"}

    os.makedirs(args.output, exist_ok=True)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    count = 0

    for insn, operand_sets in TESTS:
        modes = ["static"] if insn in LOAD_STORE else ["static", "accum"]
        for mode in modes:
            for i, (op1, op2, desc) in enumerate(operand_sets):
                suffix = f"_{mode}" if mode != "static" else ""
                test_name = f"{insn}_{desc}{suffix}"
                test_dir = os.path.join(args.output, test_name)

                subprocess.run([
                    sys.executable, os.path.join(script_dir, "generate_test.py"),
                    "-i", insn, "-o1", op1, "-o2", op2,
                    "-r", str(args.repeats), "-o", test_dir,
                    "-m", mode
                ], check=True)
                count += 1

    print(f"\nGenerated {count} tests in {args.output}/")


if __name__ == "__main__":
    main()
