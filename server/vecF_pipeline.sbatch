#!/bin/bash
#SBATCH --job-name=vecF
#SBATCH --output=tmp_check/descent/slurm_%j.txt
#SBATCH --cpus-per-task=12
#SBATCH --mem=60G
#SBATCH --gpus=0
# Runs server/alternate_descent.py (construction, then greedy and exhaustive descent alternated) on several knots,
# four at a time with three processes each.
# usage, from the copy of F_index/ on the cluster: sbatch server/vecF_pipeline.sbatch KNOT1 KNOT2 ...
ENV=${ENV:-$HOME/envs/thompson}
export PATH=$ENV/bin:$PATH
cd "$SLURM_SUBMIT_DIR"
printf '%s\n' "$@" | xargs -P 4 -I{} python server/alternate_descent.py {} 3 19
echo "all done ($*)"
