#!/bin/bash
# vec{F} diagram of a knot with no known diagram in vec{F}, then descent to the lower bound:
#   1. alexander.py (Aiello's Alexander theorem for vec{F} as an algorithm; best of several special diagrams);
#   2. greedy_descent.py --group Fvec (deletions of 2, 4, ..., 12 vertices per tree);
#   3. descent_search.py from the last diagram (extra = 1, beam 50) down to N_MIN.
# usage (from F_index/): bash server/vecF_pipeline.sh KNOT [processes] [n_min]
# Output: tmp_check/alexander/KNOT.json, KNOT_greedy.jsonl, tmp_check/descent/out_vecF_KNOT_last.csv and logs.
set -u
K=$1
P=${2:-3}
NMIN=${3:-19}
PY=${PY:-python}
mkdir -p tmp_check/alexander tmp_check/descent
if [ ! -f tmp_check/alexander/$K.json ]; then
  $PY alexander.py $K --seed 50 --minutes 3 --tries 4 > tmp_check/alexander_$K.log 2>&1
fi
if [ ! -f tmp_check/alexander/$K.json ]; then echo "$K: no construction"; exit 1; fi
$PY greedy_descent.py tmp_check/alexander/$K.json $P --group Fvec --n-min $NMIN > tmp_check/alexander/${K}_greedy.log 2>&1
$PY - "$K" "$NMIN" <<'EOF'
import json, sys
k, nmin = sys.argv[1], int(sys.argv[2])
steps = [json.loads(x) for x in open('tmp_check/alexander/%s_greedy.jsonl' % k) if x.strip()]
if steps:
    n, d = steps[-1]['n'], steps[-1]['diagram']
else:
    s = json.load(open('tmp_check/alexander/%s.json' % k))
    n, d = s['leaves'], s['Fvec']
json.dump([dict(name='vecF_%s_from%d' % (k, n), group='Fvec', knot=k, starts=[d], steps=max(0, (n - nmin) // 2),
                extra=1, beam=50)], open('tmp_check/descent/jobs_vecF_%s_last.json' % k, 'w'))
print(k, 'greedy reached', n)
EOF
DESCENT_OUT=tmp_check/descent/out_vecF_${K}_last.csv $PY descent_search.py tmp_check/descent/jobs_vecF_${K}_last.json $P \
  > tmp_check/descent/vecF_${K}_last.log 2>&1
echo "$K: $(grep -E ': FOUND|nothing at' tmp_check/descent/vecF_${K}_last.log | tail -1)"
