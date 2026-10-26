"""
Run bin/fknots for n = nmin..nmax leaves in parallel and merge the shards into results/raw/n<n>.tsv.

usage: python3 run.py NMAX [--group F|F3|Fvec] [--nmin 2] [--jobs 8] [--reps 50] [--force]

Each n already present in results/raw/ is skipped (unless --force), so the computation can be
resumed and extended to larger n later.

--group Fvec keeps only the elements of Jones' oriented subgroup vec{F} (bin/fknots ... vec) and
writes to results/raw_Fvec/.
--group F3 enumerates the ternary tree diagrams of F_3 with bin/iota_knots instead (n = number of
internal vertices + 1, as in the definition of the F_3-index) and writes to results/raw_F3/.
"""
import argparse
import os
import subprocess
import sys
import tempfile
import time
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
BINS = {'F': [os.path.join(HERE, 'bin', 'fknots')],
        'Fvec': [os.path.join(HERE, 'bin', 'fknots')],
        'F3': [os.path.join(HERE, 'bin', 'iota_knots'), 'F3']}
EXTRA_ARGS = {'Fvec': ['vec']}
RAWS = {'F': os.path.join(HERE, 'results', 'raw'),
        'Fvec': os.path.join(HERE, 'results', 'raw_Fvec'),
        'F3': os.path.join(HERE, 'results', 'raw_F3')}


def catalan(m):
    return comb(2 * m, m) // (m + 1)


def n_trees(group, n):
    """Number of trees with n - 1 internal vertices (binary for F, ternary for F_3)."""
    c = n - 1
    return catalan(c) if group in ('F', 'Fvec') else comb(3 * c, c) // (2 * c + 1)


def run_n(group, n, jobs, reps):
    tmp = tempfile.mkdtemp(prefix='fknots_%s_n%d_' % (group, n))
    outs = [os.path.join(tmp, 'shard%d.tsv' % s) for s in range(jobs)]
    procs = [subprocess.Popen(BINS[group] + [str(n), str(s), str(jobs), outs[s], str(reps)] + EXTRA_ARGS.get(group, []))
             for s in range(jobs)]
    for p in procs:
        if p.wait() != 0:
            sys.exit('fknots failed for n = %d' % n)

    stats = {}
    classes = {}  # key -> [count, min_crossings, reps]
    for out in outs:
        with open(out) as f:
            header = f.readline()
            for kv in header[2:].split():
                k, v = kv.split('=')
                if k not in ('n', 'shard', 'classes'):
                    stats[k] = stats.get(k, 0) + int(v)
            for line in f:
                key, count, mincr, rs = line.rstrip('\n').split('\t')
                c = classes.setdefault(key, [0, 10**9, []])
                c[0] += int(count)
                c[1] = min(c[1], int(mincr))
                c[2].extend(r for r in rs.split(';') if r)
        os.remove(out)
    os.rmdir(tmp)

    raw = RAWS[group]
    os.makedirs(raw, exist_ok=True)
    path = os.path.join(raw, 'n%d.tsv' % n)
    with open(path + '.part', 'w') as f:
        f.write('# n=%d pairs=%d %s classes=%d\n' % (
            n, n_trees(group, n) ** 2, ' '.join('%s=%d' % kv for kv in stats.items()), len(classes)))
        f.write('# homfly_lm_up_to_mirror\tdiagrams\tmin_crossings_after_RI_RII\trepresentatives\n')
        for key in sorted(classes, key=lambda k: (classes[k][1], k)):
            count, mincr, rs = classes[key]
            # keep the representatives with fewest crossings after simplification first
            rs = sorted(rs, key=lambda r: r.split('|')[2].count(','))[:reps]
            f.write('%s\t%d\t%d\t%s\n' % (key, count, mincr, ';'.join(rs)))
    os.replace(path + '.part', path)
    return stats, len(classes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('nmax', type=int)
    ap.add_argument('--group', choices=['F', 'F3', 'Fvec'], default='F')
    ap.add_argument('--nmin', type=int, default=2)
    ap.add_argument('--jobs', type=int, default=os.cpu_count())
    ap.add_argument('--reps', type=int, default=50, help='representatives kept per HOMFLY class')
    ap.add_argument('--force', action='store_true')
    args = ap.parse_args()
    if not os.path.exists(BINS[args.group][0]):
        sys.exit('build first with: make')
    for n in range(args.nmin, args.nmax + 1):
        path = os.path.join(RAWS[args.group], 'n%d.tsv' % n)
        if os.path.exists(path) and not args.force:
            print('n = %2d: already done (%s)' % (n, os.path.relpath(path, HERE)))
            continue
        t = time.time()
        stats, ncl = run_n(args.group, n, args.jobs, args.reps)
        print('n = %2d: %d prime knot diagrams (up to symmetry), %d HOMFLY classes, %.1f s'
              % (n, stats['knots'], ncl, time.time() - t), flush=True)


if __name__ == '__main__':
    main()
