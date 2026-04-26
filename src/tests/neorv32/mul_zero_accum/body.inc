# mul | op1=0x00000000 op2=0xFFFFFFFF | repeats=1000 | mode=accum

    # operand setup
    li t0, 0x00000000
    li t1, 0xFFFFFFFF

    rdcycle s0

.globl begin_measure
begin_measure:
.rept 1000
    mul t0, t0, t1
.endr
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
