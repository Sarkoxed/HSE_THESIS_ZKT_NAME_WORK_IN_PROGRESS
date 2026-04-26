.section .text
.globl main

main:
    # --- operand setup ---
    li t0, 0xAAAAAAAA
    li t1, 0x55555555

    # --- measured block: 1000x xor ---
.globl begin_measure
begin_measure:
.rept 1000
    xor t0, t0, t1
.endr
.globl end_measure
end_measure:

    # --- return ---
    li a0, 0
    ret
