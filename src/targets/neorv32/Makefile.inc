# NEORV32 target
NEORV32_HOME ?= $(TARGETS_DIR)/../../cores/neorv32
RISCV_PREFIX ?= riscv32-unknown-elf-
EFFORT = -Os

USER_FLAGS += -Wl,--defsym,__neorv32_rom_size=$(ROM_SIZE)
USER_FLAGS += -Wl,--defsym,__neorv32_ram_size=8k

include $(NEORV32_HOME)/sw/common/common.mk

sim: install
	cd $(NEORV32_HOME)/sim && bash ghdl.sh --stop-time=$(STOP_TIME)
