#!/bin/bash
#SBATCH --job-name=descent
#SBATCH --output=tmp_check/descent/slurm_%j.txt
#SBATCH --cpus-per-task=12
#SBATCH --mem=40G
#SBATCH --gpus=0
# Targeted search (descent_search.py) on a SLURM cluster.
# usage, from the copy of F_index/ on the cluster: sbatch server/descent_search.sbatch tmp_check/descent/jobs_<name>.json
# Needs a Python environment with Sage, SnapPy and spherogram (here $HOME/envs/thompson; change ENV if needed).
# Output: tmp_check/descent/out_<jobs file name>.csv (same columns as results/descent_search.csv), log in
# tmp_check/descent/slurm_<job id>.txt. Submitting the same file again resumes it (the done file skips the knots done).
ENV=${ENV:-$HOME/envs/thompson}
export PATH=$ENV/bin:$PATH
cd "$SLURM_SUBMIT_DIR"
J=$1
export DESCENT_OUT=$PWD/tmp_check/descent/out_$(basename $J .json).csv
python scripts/descent_search.py $J "${SLURM_CPUS_PER_TASK:-12}"
echo "all done ($J)"
