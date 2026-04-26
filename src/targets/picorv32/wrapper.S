.section .text
.globl _start

_start:
    .include "body.inc"

    # signal test passed
    li t3, 0x20000000
    li t4, 123456789
    sw t4, 0(t3)
    ebreak
