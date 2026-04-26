# sw | op1=0x00000000 | repeats=1000 | mode=static

    # operand setup
    la t0, test_data
    li t1, 0x00000000

    rdcycle s0

.globl begin_measure
begin_measure:
.rept 1000
    sw t1, 0(t0)
.endr
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
