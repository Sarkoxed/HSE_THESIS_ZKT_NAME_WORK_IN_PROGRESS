# slt | op1=0x00000001 op2=0x00000002 | repeats=1000 | mode=accum

    # operand setup
    li t0, 0x00000001
    li t1, 0x00000002

    rdcycle s0

.globl begin_measure
begin_measure:
.rept 1000
    slt t0, t0, t1
.endr
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
