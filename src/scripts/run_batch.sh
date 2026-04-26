#!/bin/bash
set -e

TESTS_DIR="${1:?Usage: run_batch.sh <tests_dir> [n_parallel] [docker_image]}"
N="${2:-2}"
DOCKER_IMAGE="${3:-zkt-bench}"
DATA_DIR="$(pwd)/data"

mkdir -p "$DATA_DIR"

# collect test dirs
TESTS=()
for d in "$TESTS_DIR"/*/; do
    [ -f "$d/Makefile" ] && TESTS+=("$(realpath "$d")")
done

echo "=== Batch runner ==="
echo "Tests:    ${#TESTS[@]}"
echo "Parallel: $N"
echo "Image:    $DOCKER_IMAGE"
echo "Data:     $DATA_DIR"
echo ""

RUNNING=0
DONE=0
FAILED=0
PIDS=()
NAMES=()

run_test() {
    local test_dir="$1"
    local name=$(basename "$test_dir")
    echo "[START] $name"
    docker run --rm \
        -v "$test_dir":/project/tests/"$name":ro \
        -v "$DATA_DIR":/data \
        "$DOCKER_IMAGE" /project/tests/"$name" > /dev/null 2>&1 &
    PIDS+=($!)
    NAMES+=("$name")
    RUNNING=$((RUNNING + 1))
}

wait_for_slot() {
    while [ $RUNNING -ge $N ]; do
        for i in "${!PIDS[@]}"; do
            if ! kill -0 "${PIDS[$i]}" 2>/dev/null; then
                wait "${PIDS[$i]}" && DONE=$((DONE + 1)) || FAILED=$((FAILED + 1))
                echo "[DONE]  ${NAMES[$i]}"
                unset 'PIDS[i]' 'NAMES[i]'
                RUNNING=$((RUNNING - 1))
                # reindex arrays
                PIDS=("${PIDS[@]}")
                NAMES=("${NAMES[@]}")
                return
            fi
        done
        sleep 5
    done
}

# queue all tests
for test_dir in "${TESTS[@]}"; do
    wait_for_slot
    run_test "$test_dir"
done

# wait for remaining
for pid in "${PIDS[@]}"; do
    wait "$pid" && DONE=$((DONE + 1)) || FAILED=$((FAILED + 1))
done

echo ""
echo "=== Batch complete ==="
echo "Done:   $DONE"
echo "Failed: $FAILED"
echo "Total:  ${#TESTS[@]}"
