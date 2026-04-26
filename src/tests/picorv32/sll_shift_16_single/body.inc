# sll | op1=0x00000001 op2=0x00000010 | repeats=1 | mode=single

    # operand setup
    li t0, 0x00000001
    li t1, 0x00000010

    rdcycle s0

.globl begin_measure
begin_measure:
    sll t2, t0, t1
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
