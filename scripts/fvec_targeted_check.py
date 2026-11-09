"""
Check of a targeted enumeration of vec{F} (server/fvec_targeted.sbatch): for every target knot, every tree diagram
of size N in its HOMFLY-PT class (files <dir>/n<N>.tsv.*.all, lines 'key<TAB>top<TAB>bottom') is compared with
the knot: SnapPy (volume, then isometry) for hyperbolic knots, recognition in KnotInfo for the others (torus
knots). A knot with a matching diagram has vec{F}-index N (its lower bound); a knot without any has index > N.
These floating-point verdicts are then certified with the methods of certify_indices.py.

usage (from F_index/): sage -python scripts/fvec_targeted_check.py DIR N TARGETS.json [processes]
Output: DIR/check_n<N>.csv (knot, diagrams in its class, matching diagrams, first matching diagram).
"""
import csv
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root (the scripts are in scripts/)
sys.path.insert(0, os.path.join(HERE, 'scripts'))


def task(args):
    knot, diagrams = args
    import snappy  # noqa: F401
    import spherogram
    import complete_check as C
    import descent_search as D
    ref, vk, Ek, _ = D._ref(knot)
    hits = []
    for top, bottom in diagrams:
        pd = D.pd_code('Fvec', D.tree('Fvec', top), D.tree('Fvec', bottom))
        if pd is None:
            continue
        S = spherogram.Link([[x - 1 for x in c] for c in pd])
        if vk is None:
            if D.same_by_knotinfo(S, knot):
                hits.append(top + ' | ' + bottom)
            continue
        E = S.exterior()
        try:
            if C._geometric(E) and abs(float(E.volume()) - vk) < C.VOLUME_EPS and E.is_isometric_to(Ek):
                hits.append(top + ' | ' + bottom)
        except Exception:
            continue
    return knot, len(diagrams), hits


def main():
    d, n, targets = sys.argv[1], int(sys.argv[2]), json.load(open(sys.argv[3]))
    procs = int(sys.argv[4]) if len(sys.argv) > 4 else os.cpu_count()
    knots_of = {}
    for k in targets['targets']:
        knots_of.setdefault(targets['keys'][k], []).append(k)
    per_key = {}
    for f in sorted(glob.glob(os.path.join(d, 'n%d.tsv.*.all' % n))):
        for line in open(f):
            key, top, bottom = line.rstrip('\n').split('\t')
            per_key.setdefault(key, []).append((top, bottom))
    tasks = []
    for key, ks in knots_of.items():
        diags = per_key.get(key, [])
        for k in ks:
            for i in range(0, max(1, len(diags)), 500):
                tasks.append((k, diags[i:i + 500]))
    from identify_lib import RobustPool
    res = {}
    with RobustPool(procs) as pool:
        for k, m, hits in pool.map(task, tasks):
            r = res.setdefault(k, [0, []])
            r[0] += m
            r[1] += hits
    out = os.path.join(d, 'check_n%d.csv' % n)
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['knot', 'diagrams_in_class', 'matching', 'first_matching'])
        for k in targets['targets']:
            m, hits = res.get(k, [0, []])
            w.writerow([k, m, len(hits), hits[0] if hits else ''])
            print('%s: %d diagrams in its class at n = %d, %d realize it' % (k, m, n, len(hits)), flush=True)
    print('written to', out)


if __name__ == '__main__':
    main()
