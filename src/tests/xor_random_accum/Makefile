# Auto-generated test: xor_12345678_9ABCDEF0
# Instruction: xor, op1=0x12345678, op2=0x9ABCDEF0, repeats=1000

MARCH = rv32i_zicsr_zifencei
RISCV_PREFIX ?= riscv32-unknown-elf-
EFFORT = -Os

USER_FLAGS += -Wl,--defsym,__neorv32_rom_size=8k
USER_FLAGS += -Wl,--defsym,__neorv32_ram_size=8k

NEORV32_HOME ?= ../../cores/neorv32

include $(NEORV32_HOME)/sw/common/common.mk

STOP_TIME ?= 1ms

sim: install
	cd $(NEORV32_HOME)/sim && bash ghdl.sh --stop-time=$(STOP_TIME)

parse:
	python3 ../../scripts/neorv32/parse_trace.py -e main.elf -l $(NEORV32_HOME)/sim/neorv32.tracer0.log

run: sim parse
