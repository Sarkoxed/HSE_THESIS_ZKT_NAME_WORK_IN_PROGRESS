# add | op1=0x7FFFFFFF op2=0x7FFFFFFF | repeats=1 | mode=single

    # operand setup
    li t0, 0x7FFFFFFF
    li t1, 0x7FFFFFFF

    rdcycle s0

.globl begin_measure
begin_measure:
    add t2, t0, t1
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
