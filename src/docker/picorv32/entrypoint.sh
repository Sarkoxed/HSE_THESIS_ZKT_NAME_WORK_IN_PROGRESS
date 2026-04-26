#!/bin/bash
set -e
SECONDS=0

TEST_DIR="${1:?Usage: entrypoint.sh <test_dir>}"
TEST_NAME=$(basename "$TEST_DIR")
OUTPUT_DIR="/data/picorv32/${TEST_NAME}"
BUILD_DIR="/tmp/build"

mkdir -p "$OUTPUT_DIR"

exec > >(tee "$OUTPUT_DIR/session.log") 2>&1

echo "=== ZKT Bench (PicoRV32) ==="
echo "Test:      $TEST_DIR"
echo "Output:    $OUTPUT_DIR"
echo ""

# copy test to temp build dir
cp -r "$TEST_DIR" "$BUILD_DIR"
cd "$BUILD_DIR"

# build + simulate
make TARGETS_DIR=/project/targets sim
echo "Sim time: ${SECONDS}s"

# collect
cp main.elf "$OUTPUT_DIR/"
cp testbench.trace "$OUTPUT_DIR/" 2>/dev/null || true
cp main.hex "$OUTPUT_DIR/" 2>/dev/null || true

echo ""
echo "=== Done ==="
echo "Results saved to $OUTPUT_DIR"
echo "Total time: ${SECONDS}s"
