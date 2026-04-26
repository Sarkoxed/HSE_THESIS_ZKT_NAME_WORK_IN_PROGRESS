# div | op1=0x0000000F op2=0x00000003 | repeats=1000 | mode=static

    # operand setup
    li t0, 0x0000000F
    li t1, 0x00000003

    rdcycle s0

.globl begin_measure
begin_measure:
.rept 1000
    div t2, t0, t1
.endr
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
