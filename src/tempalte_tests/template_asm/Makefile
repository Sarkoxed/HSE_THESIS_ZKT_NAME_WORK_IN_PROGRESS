# ASM test template for NEORV32
# Usage:
#   make clean_all exe     - compile only
#   make clean_all install - compile + generate IMEM image
#   make sim               - run GHDL simulation

MARCH = rv32i_zicsr_zifencei
RISCV_PREFIX ?= riscv32-unknown-elf-
EFFORT = -Os

USER_FLAGS += -Wl,--defsym,__neorv32_rom_size=16k
USER_FLAGS += -Wl,--defsym,__neorv32_ram_size=8k

NEORV32_HOME ?= ../../cores/neorv32

include $(NEORV32_HOME)/sw/common/common.mk

sim: install
	cd $(NEORV32_HOME)/sim && bash ghdl.sh --stop-time=200ms

#parse:
#	python3 ../parse_trace.py main.elf $(NEORV32_HOME)/sim/neorv32.tracer0.log

#run: sim parse
