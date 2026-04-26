RISCV_PREFIX ?= riscv32-unknown-elf-
PICORV32_HOME ?= ../../cores/picorv32
MARCH = rv32i_zicsr

main.elf: main.S
	$(RISCV_PREFIX)gcc -mabi=ilp32 -march=$(MARCH) -nostdlib -Ttext=0x00000000 -o $@ $<

main.bin: main.elf
	$(RISCV_PREFIX)objcopy -O binary $< $@

main.hex: main.bin
	python3 $(PICORV32_HOME)/firmware/makehex.py $< 32768 > $@

testbench.vvp: $(PICORV32_HOME)/testbench.v $(PICORV32_HOME)/picorv32.v
	iverilog -o $@ $^

sim: main.hex testbench.vvp
	vvp testbench.vvp +firmware=main.hex +trace

clean:
	rm -f main.elf main.bin main.hex testbench.vvp testbench.trace testbench.vcd

run: sim
