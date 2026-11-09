"""
Which orientations of a knot K are realized by the oriented knots L(g), g in vec{F}, with n leaves.

usage (from F_index/):   sage -python scripts/oriented_index.py KNOT N [N2 ...] [--processes P]
e.g.                     sage -python scripts/oriented_index.py 8_17 13 15

For each n: bin/fknots (vec mode, all representatives, P shards in parallel) lists every prime knot
diagram g in vec{F} (one of g, g^-1) whose HOMFLY polynomial is that of K (up to mirror). Then, in
parallel, for g and for g^-1 the oriented knot (orientation from the 2-colouring of the Tait graph, see
oriented.py) is compared with the oriented KnotInfo diagram of K through the isometries of the
complements (oriented.relation_to; K must be hyperbolic):
    K     = the oriented knot of KnotInfo,           Kr  = its reverse,
    Km    = its mirror image,                        Kmr = the mirror image of the reverse.
A diagram realizes K if the relation 'same' holds, Kr if 'reverse' holds, Km if 'mirror', Kmr if
'mirror reverse' (several can hold at once, according to the symmetries of K). The output says, for
each n, how many diagrams realize each of them: the vec{F}-index of K is the first n where K occurs.

The global convention (colour + = counterclockwise boundary, leftmost Tait vertex coloured +) fixes
which of K, Kr is which; reversing it exchanges them, so "are the indices of K and Kr different?" does
not depend on it.
"""
import argparse
import multiprocessing as mp
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root (the scripts are in scripts/)
sys.path.insert(0, os.path.join(HERE, 'scripts'))


def homfly_key(pd):
    """The key of bin/fknots: HOMFLY (libhomfly variables L, M) up to mirror, as a canonical string."""
    from sage.all import Link
    p = Link(pd).homfly_polynomial('L', 'M', 'lm')
    terms = [(int(e[0]), int(e[1]), int(c)) for e, c in p.dict().items()]
    a = sorted(terms)
    b = sorted((-l, m, c) for l, m, c in terms)
    best = min([[l, m, c] for l, m, c in a], [[l, m, c] for l, m, c in b])
    return ''.join('%d*L^%d*M^%d ' % (c, l, m) for l, m, c in best)


def reference_pd(name):
    from sage.all import KnotInfo
    K = getattr(KnotInfo, 'K' + name)
    return [list(map(int, c)) for c in K.link().pd_code()]


def diagrams(n, key, processes):
    """All (top words, bottom words) of the prime knot diagrams in vec{F} with HOMFLY key `key`
    (one of g, g^-1 for each pair)."""
    tmp = tempfile.mkdtemp(prefix='oriented_n%d_' % n)
    outs = [os.path.join(tmp, 's.tsv.%d' % s) for s in range(processes)]
    # one fknots process: it builds the trees once and forks the workers, which share them
    procs = [subprocess.Popen([os.path.join(HERE, 'bin', 'fknots'), str(n), '-1', str(processes),
                               os.path.join(tmp, 's.tsv'), '1000000000', 'vec', key])]
    for p in procs:
        assert p.wait() == 0
    found = []
    for out in outs:
        with open(out) as f:
            next(f)
            for line in f:
                k, count, mincr, reps = line.rstrip('\n').split('\t')
                if k == key:
                    found += [tuple(r.split('|')[:2]) for r in reps.split(';')]
        os.remove(out)
    os.rmdir(tmp)
    return found


def classify(task):
    """Relations of g and of g^-1 to the reference knot."""
    top, bottom, ref = task
    import ftrees as F
    import oriented as O
    tp, tm = F.from_leaf_words(top.split(',')), F.from_leaf_words(bottom.split(','))
    return (top, bottom, sorted(O.relation_to(O.oriented_pd_code(tp, tm), ref)),
            sorted(O.relation_to(O.oriented_pd_code(tm, tp), ref)))


NAMES = {'same': 'K', 'reverse': 'Kr', 'mirror': 'Km', 'mirror reverse': 'Kmr'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('knot')
    ap.add_argument('n', type=int, nargs='+')
    ap.add_argument('--processes', type=int, default=os.cpu_count())
    args = ap.parse_args()
    ref = reference_pd(args.knot)
    key = homfly_key(ref)
    print('%s: HOMFLY key %s' % (args.knot, key), flush=True)
    for n in args.n:
        ds = diagrams(n, key, args.processes)
        print('n = %d: %d diagrams (up to g <-> g^-1) with the HOMFLY of %s' % (n, len(ds), args.knot),
              flush=True)
        counts = {v: 0 for v in NAMES.values()}
        example = {}
        with ProcessPoolExecutor(args.processes, mp_context=mp.get_context('spawn')) as ex:
            for top, bottom, rel_g, rel_ginv in ex.map(classify, [(t, b, ref) for t, b in ds], chunksize=4):
                for (t, b), rel in (((top, bottom), rel_g), ((bottom, top), rel_ginv)):
                    for r in rel:
                        counts[NAMES[r]] += 1
                        example.setdefault(NAMES[r], (t, b))
        for v in ('K', 'Kr', 'Km', 'Kmr'):
            print('   %-3s realized by %6d elements g in vec{F}%s' % (
                v, counts[v], ('   e.g. T+ = %s  T- = %s' % example[v]) if v in example else ''), flush=True)


if __name__ == '__main__':
    main()
