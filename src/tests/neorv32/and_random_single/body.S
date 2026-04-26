# and | op1=0x12345678 op2=0x9ABCDEF0 | repeats=1 | mode=single

    # operand setup
    li t0, 0x12345678
    li t1, 0x9ABCDEF0

    rdcycle s0

.globl begin_measure
begin_measure:
    and t2, t0, t1
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
