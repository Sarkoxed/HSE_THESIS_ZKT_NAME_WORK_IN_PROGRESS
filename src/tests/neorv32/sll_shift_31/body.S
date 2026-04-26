# sll | op1=0x00000001 op2=0x0000001F | repeats=1000 | mode=static

    # operand setup
    li t0, 0x00000001
    li t1, 0x0000001F

    rdcycle s0

.globl begin_measure
begin_measure:
.rept 1000
    sll t2, t0, t1
.endr
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
