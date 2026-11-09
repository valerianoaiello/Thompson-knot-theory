#!/bin/bash
#SBATCH --job-name=vecFdesc
#SBATCH --output=tmp_check/descent/slurm_%j.txt
#SBATCH --cpus-per-task=12
#SBATCH --mem=60G
#SBATCH --gpus=0
# vec{F} descent queue: server/descent_queue.sh on several knots, four at a time with three processes each.
# usage, from the copy of F_index/ on the cluster: sbatch server/descent_queue.sbatch KNOT1 KNOT2 ...
ENV=${ENV:-$HOME/envs/thompson}
export PATH=$ENV/bin:$PATH
cd "$SLURM_SUBMIT_DIR"
printf '%s\n' "$@" | xargs -P 4 -I{} bash server/descent_queue.sh {} 3 21
echo "all done ($*)"
