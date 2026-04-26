# ror | op1=0x12345678 op2=0x0000001F | repeats=1000 | mode=accum

    # operand setup
    li t0, 0x12345678
    li t1, 0x0000001F

    rdcycle s0

.globl begin_measure
begin_measure:
.rept 1000
    ror t0, t0, t1
.endr
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
