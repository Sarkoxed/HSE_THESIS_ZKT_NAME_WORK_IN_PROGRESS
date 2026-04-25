#!/usr/bin/env python3
import argparse
import subprocess


def get_symbol_addrs(elf_path):
    result = subprocess.run(
        ["riscv32-unknown-elf-nm", elf_path], capture_output=True, text=True
    )
    symbols = {}
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) == 3:
            addr, _, name = parts
            symbols[name] = int(addr, 16)
    return symbols


def parse_tracer_log(log_path):
    entries = []
    with open(log_path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 4:
                order = int(parts[0])
                cycle = int(parts[1])
                pc = int(parts[2], 16)
                insn = parts[3]
                rest = " ".join(parts[4:])
                entries.append((order, cycle, pc, insn, rest))
    return entries


def find_cycle_at_pc(entries, target_pc):
    for order, cycle, pc, insn, rest in entries:
        if pc == target_pc:
            return cycle


# metric 1: cycles_main [main -> ret]
def get_main_cycles(symbols, entries):
    main_addr = symbols.get("main")
    if main_addr is not None:
        main_start = find_cycle_at_pc(entries, main_addr)

        # find jalr x0 - ret after main
        main_end = None

        for order, cycle, pc, insn, rest in entries:
            if (pc >= main_addr) and ("jalr" in rest) and ("x0, 0(x1)" in rest):
                main_end = cycle
                break

        if main_start and main_end:
            print(f"cycles_main: {main_end - main_start}")
        else:
            print(main_start, main_end)
    else:
        print("main not found in elf")


# Metric 2: cycles_measure [begin_measure -> end_measure]
def get_measurement_cycles(symbols, entries):
    begin_addr = symbols.get("begin_measure")
    end_addr = symbols.get("end_measure")

    if begin_addr is not None and end_addr is not None:
        begin_cycle = find_cycle_at_pc(entries, begin_addr)
        end_cycle = find_cycle_at_pc(entries, end_addr)

        if begin_cycle and end_cycle:
            cycles = end_cycle - begin_cycle
            print(f"cycles_measure: {cycles}")

            measured_insns = sum(
                1 for _, _, pc, _, _ in entries if begin_addr <= pc < end_addr
            )
            print(f"insns_measure:  {measured_insns}")
            if measured_insns > 0:
                print(f"cycles_per_insn: {cycles / measured_insns}")
        else:
            print(begin_cycle, end_cycle)
    else:
        print("no measure labels found in elf")
        print([s for s in symbols if 'measure' in s.lower()])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--elf-path", required=True, help="elf path")
    parser.add_argument("-l", "--log-path", required=True, help="log path")

    args = parser.parse_args()
    elf_path = args.elf_path
    log_path = args.log_path

    symbols = get_symbol_addrs(elf_path)
    entries = parse_tracer_log(log_path)

    get_main_cycles(symbols, entries)
    get_measurement_cycles(symbols, entries)

    print("addresses: ")
    for name in ["main", "begin_measure", "end_measure"]:
        addr = symbols.get(name)
        if addr:
            print(f"{name}: 0x{addr:08x}")


if __name__ == "__main__":
    main()
