.section .text
.globl main

main:
    # --- operand setup ---
    la t0, test_data
    li t1, 0xDEADBEEF

    # --- measured block: 1000x lh ---
.globl begin_measure
begin_measure:
.rept 1000
    lh t2, 0(t0)
.endr
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
