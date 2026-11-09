#!/bin/bash
#SBATCH --job-name=fvecT
#SBATCH --output=tmp_check/fvec_targeted/slurm_%j.txt
#SBATCH --cpus-per-task=12
#SBATCH --mem=140G
#SBATCH --gpus=0
# Targeted enumeration of vec{F}: all the tree diagrams of size N are enumerated (bin/fknots, vec mode), and every
# diagram of the HOMFLY-PT classes listed in KEYS is written (one file <out>.<shard>.all per worker).
# usage, from the copy of F_index/ on the cluster: sbatch server/fvec_targeted.sbatch N KEYS [OUTDIR]
# (OUTDIR, default tmp_check/fvec_targeted: use a new one for every run, so that earlier outputs are kept)
ENV=${ENV:-$HOME/envs/thompson}
export PATH=$ENV/bin:$PATH
cd "$SLURM_SUBMIT_DIR"
N=$1
KEYS=$2
OUT=${3:-tmp_check/fvec_targeted}
mkdir -p $OUT
/usr/bin/time -v bin/fknots $N -1 12 $OUT/n$N.tsv -1 vec @$KEYS
echo "all done (n = $N)"
