#!/bin/bash
set -e
SECONDS=0

TEST_DIR="${1:?Usage: entrypoint.sh <test_dir> [stop_time]}"
STOP_TIME="${2:-200ms}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TEST_NAME=$(basename "$TEST_DIR")
OUTPUT_DIR="/data/${TEST_NAME}/${TIMESTAMP}"

NEORV32_HOME="/project/cores/neorv32"

# Create output dir early so we can log everything
mkdir -p "$OUTPUT_DIR"

exec > >(tee "$OUTPUT_DIR/session.log") 2>&1

echo "=== ZKT Bench ==="
echo "Test:       $TEST_DIR"
echo "Stop time:  $STOP_TIME"
echo "Output:    $OUTPUT_DIR"
echo ""

# bulid
cd "$TEST_DIR"
make NEORV32_HOME="$NEORV32_HOME" RISCV_PREFIX=riscv32-unknown-elf- clean_all install
echo "Build time: ${SECONDS}s"

# simulate
SIM_START=$SECONDS
cd "$NEORV32_HOME/sim"
bash ghdl.sh --stop-time="$STOP_TIME"
echo "Simulation time: $((SECONDS - SIM_START))s"

# collect
mkdir -p "$OUTPUT_DIR"
cp neorv32.tracer0.log "$OUTPUT_DIR/"
cp neorv32.tracer1.log "$OUTPUT_DIR/"
cp tb.uart0_rx.log "$OUTPUT_DIR/"
cp ghdl.log "$OUTPUT_DIR/"

echo ""
echo "=== Done ==="
echo "Results saved to $OUTPUT_DIR"
echo "Total time: ${SECONDS}s"
