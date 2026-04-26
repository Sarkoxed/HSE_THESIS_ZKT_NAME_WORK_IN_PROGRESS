.section .text
.globl main

main:
    # --- operand setup ---
    li t0, 0x12345678
    li t1, 0x9ABCDEF0

    # --- measured block: 1000x and ---
.globl begin_measure
begin_measure:
.rept 1000
    and t0, t0, t1
.endr
.globl end_measure
end_measure:

    # --- return ---
    li a0, 0
    ret
