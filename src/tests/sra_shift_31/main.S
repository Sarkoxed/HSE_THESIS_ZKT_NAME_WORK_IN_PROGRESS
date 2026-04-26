.section .text
.globl main

main:
    # --- operand setup ---
    li t0, 0x80000000
    li t1, 0x0000001F

    # --- measured block: 1000x sra ---
.globl begin_measure
begin_measure:
.rept 1000
    sra t2, t0, t1
.endr
.globl end_measure
end_measure:

    # --- return ---
    li a0, 0
    ret
