.section .text
.globl main

main:
    # --- operand setup ---
    li t0, 0x00000001
    li t1, 0x00000001

    # --- measured block: 1000x mul ---
.globl begin_measure
begin_measure:
.rept 1000
    mul t0, t0, t1
.endr
.globl end_measure
end_measure:

    # --- return ---
    li a0, 0
    ret
