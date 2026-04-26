# add | op1=0x12345678 op2=0x9ABCDEF0 | repeats=1000 | mode=accum

    # operand setup
    li t0, 0x12345678
    li t1, 0x9ABCDEF0

    rdcycle s0

.globl begin_measure
begin_measure:
.rept 1000
    add t0, t0, t1
.endr
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
