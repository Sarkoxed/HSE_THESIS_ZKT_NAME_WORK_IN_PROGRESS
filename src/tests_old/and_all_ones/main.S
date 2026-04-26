.section .text
.globl main

main:
    # --- operand setup ---
    li t0, 0xFFFFFFFF
    li t1, 0xFFFFFFFF

    # --- measured block: 1000x and ---
.globl begin_measure
begin_measure:
.rept 1000
    and t2, t0, t1
.endr
.globl end_measure
end_measure:

    # --- return ---
    li a0, 0
    ret
