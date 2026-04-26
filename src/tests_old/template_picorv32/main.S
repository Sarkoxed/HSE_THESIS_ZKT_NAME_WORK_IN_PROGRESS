.section .text
.globl _start

_start:
    li t0, 0x12345678
    li t1, 0x9ABCDEF0

    rdcycle s0            # cycle count before

.globl begin_measure
begin_measure:
.rept 100
    add t2, t0, t1
.endr
.globl end_measure
end_measure:

    rdcycle s1            # cycle count after
    sub s2, s1, s0        # delta

    # store result to memory for extraction
    la t3, result_cycles
    sw s0, 0(t3)          # start
    sw s1, 4(t3)          # end
    sw s2, 8(t3)          # delta

    # print delta to console (byte by byte to 0x10000000)
    li t3, 0x10000000
    sb s2, 0(t3)
    srli s2, s2, 8
    sb s2, 0(t3)
    srli s2, s2, 8
    sb s2, 0(t3)
    srli s2, s2, 8
    sb s2, 0(t3)

    # signal test passed to testbench
    li t3, 0x20000000
    li t4, 123456789
    sw t4, 0(t3)
    ebreak

.section .data
.align 4
.globl result_cycles
result_cycles:
    .word 0   # start
    .word 0   # end
    .word 0   # delta
