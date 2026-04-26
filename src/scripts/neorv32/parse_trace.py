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
                cycle = int(parts[1])
                pc = int(parts[2], 16)
                entries.append((cycle, pc))
    return entries


def find_cycle_at_pc(entries, target_pc):
    for cycle, pc in entries:
        if pc == target_pc:
            return cycle


def extract_metrics(elf_path, log_path):
    symbols = get_symbol_addrs(elf_path)
    entries = parse_tracer_log(log_path)

    if not entries:
        return {}

    main_addr = symbols.get("main")
    begin_addr = symbols.get("begin_measure")
    end_addr = symbols.get("end_measure")

    m = {}

    if main_addr is not None:
        m["main_start"] = find_cycle_at_pc(entries, main_addr)
        for i in range(len(entries) - 1, -1, -1):
            if entries[i][1] >= main_addr:
                m["main_end"] = entries[i][0]
                break
        if m.get("main_start") and m.get("main_end"):
            m["cycles_main"] = m["main_end"] - m["main_start"]

    if begin_addr is not None and end_addr is not None:
        measured = [(c, pc) for c, pc in entries if begin_addr <= pc < end_addr]
        m["insns_measure"] = len(measured)

        if len(measured) > 1:
            m["measure_start"] = measured[0][0]
            m["measure_end"] = measured[-1][0]
            deltas = [
                measured[i + 1][0] - measured[i][0] for i in range(len(measured) - 1)
            ]
            m["cycles_measure"] = sum(deltas)
            m["cycles_per_insn"] = round(m["cycles_measure"] / len(deltas), 4)

            from collections import Counter

            counts = Counter(deltas)
            mode_delta, mode_count = counts.most_common(1)[0]
            m["cycles_mode"] = mode_delta
            m["cycles_mode_pct"] = round(mode_count / len(deltas) * 100, 1)

    return m


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--elf-path", required=True)
    parser.add_argument("-l", "--log-path", required=True)
    args = parser.parse_args()

    m = extract_metrics(args.elf_path, args.log_path)
    for k, v in m.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
