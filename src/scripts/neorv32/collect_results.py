#!/usr/bin/env python3
import argparse
import csv
import os

from parse_trace import extract_metrics


def parse_test_name(test_name):
    parts = test_name.split("_", 1)
    return {"instruction": parts[0], "desc": parts[1] if len(parts) > 1 else ""}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", required=True)
    parser.add_argument("-o", "--output", default="results.csv")
    args = parser.parse_args()

    results = []

    for test_name in sorted(os.listdir(args.dir)):
        test_path = os.path.join(args.dir, test_name)
        if not os.path.isdir(test_path):
            continue

        elf_path = os.path.join(test_path, "main.elf")
        tracer_log = os.path.join(test_path, "neorv32.tracer0.log")

        if not os.path.exists(tracer_log) or not os.path.exists(elf_path):
            continue

        meta = parse_test_name(test_name)
        metrics = extract_metrics(elf_path, tracer_log)

        results.append({"test_name": test_name, **meta, **metrics})

    if not results:
        print(f"No results found in {args.dir}/")
        return

    fields = [
        "test_name", "instruction", "desc",
        "cycles_main", "cycles_measure",
        "insns_measure", "cycles_per_insn",
        "cycles_mode", "cycles_mode_pct",
    ]

    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    print(f"Collected {len(results)} results -> {args.output}")
    print(f"\n{'test_name':<30} {'insn':<6} {'cycles_measure':>14} {'cycles/insn':>12} {'mode':>6} {'mode%':>6}")
    print("-" * 78)
    for r in results:
        print(f"{r['test_name']:<30} {r.get('instruction', '?'):<6} "
              f"{str(r.get('cycles_measure', 'N/A')):>14} "
              f"{str(r.get('cycles_per_insn', 'N/A')):>12} "
              f"{str(r.get('cycles_mode', 'N/A')):>6} "
              f"{str(r.get('cycles_mode_pct', '')):>6}")


if __name__ == "__main__":
    main()
