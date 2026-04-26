# PicoRV32 target
PICORV32_HOME ?= $(TARGETS_DIR)/../cores/picorv32
WRAPPER = $(TARGETS_DIR)/picorv32/wrapper.S
RISCV_PREFIX ?= riscv32-unknown-elf-

main.elf: $(WRAPPER) body.inc
	$(RISCV_PREFIX)gcc -mabi=ilp32 -march=$(MARCH) -nostdlib -Ttext=0x00000000 -I . -o $@ $(WRAPPER)

main.bin: main.elf
	$(RISCV_PREFIX)objcopy -O binary $< $@

main.hex: main.bin
	python3 $(PICORV32_HOME)/firmware/makehex.py $< 32768 > $@

testbench.vvp: $(PICORV32_HOME)/testbench.v $(PICORV32_HOME)/picorv32.v
	iverilog -o $@ $^

sim: main.hex testbench.vvp
	vvp -N testbench.vvp +firmware=main.hex +trace +noerror

clean:
	rm -f main.elf main.bin main.hex testbench.vvp testbench.trace testbench.vcd
