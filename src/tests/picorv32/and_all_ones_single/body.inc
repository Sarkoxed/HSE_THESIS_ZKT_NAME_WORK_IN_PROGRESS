# and | op1=0xFFFFFFFF op2=0xFFFFFFFF | repeats=1 | mode=single

    # operand setup
    li t0, 0xFFFFFFFF
    li t1, 0xFFFFFFFF

    rdcycle s0

.globl begin_measure
begin_measure:
    and t2, t0, t1
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
