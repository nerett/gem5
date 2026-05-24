#!/bin/bash

RESULTS_DIR="results_baseline"
mkdir -p "$RESULTS_DIR"

for bench in bc bfs cc cc_sv pr pr_spmv sssp tc; do
    ./build/ARM/gem5.opt -d m5out_${bench} configs/example/arm/gapbs_neoverse_v2.py \
        --benchmark $bench \
        --binary-dir ../gapbs \
        --graph-scale 10 \
        --num-trials 1 > log_${bench}.txt 2>&1 &
done

wait

for bench in bc bfs cc cc_sv pr pr_spmv sssp tc; do
    if [ -f m5out_${bench}/stats.txt ]; then
        grep "board.processor.cores.core.ipc" m5out_${bench}/stats.txt > "${RESULTS_DIR}/ipc_${bench}.txt"
    fi
done
