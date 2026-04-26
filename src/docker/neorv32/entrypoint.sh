#!/bin/bash
set -e
SECONDS=0

TEST_DIR="${1:?Usage: entrypoint.sh <test_dir>}"
TEST_NAME=$(basename "$TEST_DIR")
OUTPUT_DIR="/data/neorv32/${TEST_NAME}"
BUILD_DIR="/tmp/build"

NEORV32_HOME="/project/cores/neorv32"

mkdir -p "$OUTPUT_DIR"

exec > >(tee "$OUTPUT_DIR/session.log") 2>&1

echo "=== ZKT Bench ==="
echo "Test:       $TEST_DIR"
echo "Output:    $OUTPUT_DIR"
echo ""

# copy test to temp build dir (keep mounted test dir clean)
cp -r "$TEST_DIR" "$BUILD_DIR"
cd "$BUILD_DIR"

# build + simulate
make NEORV32_HOME="$NEORV32_HOME" RISCV_PREFIX=riscv32-unknown-elf- clean_all sim
echo "Sim time: ${SECONDS}s"

# collect artifacts to output
cp main.elf "$OUTPUT_DIR/"
cp "$NEORV32_HOME/sim/neorv32.tracer0.log" "$OUTPUT_DIR/"
cp "$NEORV32_HOME/sim/neorv32.tracer1.log" "$OUTPUT_DIR/" 2>/dev/null || true
cp "$NEORV32_HOME/sim/tb.uart0_rx.log" "$OUTPUT_DIR/"
cp "$NEORV32_HOME/sim/ghdl.log" "$OUTPUT_DIR/"

echo ""
echo "=== Done ==="
echo "Results saved to $OUTPUT_DIR"
echo "Total time: ${SECONDS}s"
