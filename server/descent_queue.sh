#!/bin/bash
# One knot of the vec{F} descent queue: server/alternate_descent.py down to N_MIN, with the default construction
# (seed 50) and, if the descent stops above N_MIN, with the construction of seed 100 (other seeds:
# SEEDS="50 100 150 200").
# Progress is resumable (tmp_check/alexander/KNOT[_sS]_greedy.jsonl).
# usage, from F_index/: bash server/descent_queue.sh KNOT [processes] [n_min]
K=$1; P=${2:-3}; NMIN=${3:-21}
for S in ${SEEDS:-50 100}; do
  out=$(python server/alternate_descent.py "$K" "$P" "$NMIN" --seed "$S" | tail -1)
  echo "$(date +%m-%d_%H:%M) $K seed $S: $out"
  case "$out" in *FOUND*) exit 0;; esac
done
