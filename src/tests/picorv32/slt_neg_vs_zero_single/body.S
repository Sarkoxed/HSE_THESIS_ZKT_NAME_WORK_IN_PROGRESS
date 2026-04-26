# slt | op1=0xFFFFFFFF op2=0x00000000 | repeats=1 | mode=single

    # operand setup
    li t0, 0xFFFFFFFF
    li t1, 0x00000000

    rdcycle s0

.globl begin_measure
begin_measure:
    slt t2, t0, t1
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
