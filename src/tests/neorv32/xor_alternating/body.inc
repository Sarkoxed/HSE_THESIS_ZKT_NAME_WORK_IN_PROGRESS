# xor | op1=0xAAAAAAAA op2=0x55555555 | repeats=1000 | mode=static

    # operand setup
    li t0, 0xAAAAAAAA
    li t1, 0x55555555

    rdcycle s0

.globl begin_measure
begin_measure:
.rept 1000
    xor t2, t0, t1
.endr
.globl end_measure
end_measure:

    rdcycle s1
    sub s2, s1, s0
