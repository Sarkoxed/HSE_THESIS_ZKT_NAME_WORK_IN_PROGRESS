# xor | op1=0xFFFFFFFF op2=0x00000000 | repeats=1000 | mode=static

    # operand setup
    li t0, 0xFFFFFFFF
    li t1, 0x00000000

    rdcycle s0

.globl begin_measure
begin_measure:
.rept 1000
    xor t2, t0, t1
.endr
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
