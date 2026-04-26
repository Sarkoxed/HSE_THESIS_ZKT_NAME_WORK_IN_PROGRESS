# sra | op1=0x80000000 op2=0x00000001 | repeats=1 | mode=single

    # operand setup
    li t0, 0x80000000
    li t1, 0x00000001

    rdcycle s0

.globl begin_measure
begin_measure:
    sra t2, t0, t1
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
