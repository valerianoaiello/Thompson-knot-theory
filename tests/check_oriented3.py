"""
Checks of the orientation of L(g), g in vec{F}_3 (oriented.oriented_pd_code3).

usage (from F_index/):   sage -python tests/check_oriented3.py [cmax] [samples]      (defaults 4, 300)

1. For every pair of ternary trees with c <= cmax internal vertices in vec{F}_3: the colours given by the
   weights c+- (vertex left of leaf 2v, even = +) are the 2-colouring of the Tait graph with vertex 0 = +
   (on both trees), and the orientation of the strands is coherent (asserted in oriented_components3).
2. On `samples` hyperbolic knots of results/raw_F3vec/n9.tsv and n11.tsv (first representative of each
   HOMFLY class, then the next ones):
   a. the oriented PD code is the knot of bin/iota_knots eval (same knot or its reverse, not the mirror:
      the C++ engine is an independent implementation of the crossings, without orientation);
   b. L(g^-1) is the mirror image of the reverse of L(g), as for vec{F}.
3. On `samples` hyperbolic knots of results/raw_Fvec/n9.tsv .. n13.tsv: L(iota(g)) = L(g) as oriented
   knots (oriented.oriented_pd_code3 vs oriented.oriented_pd_code), so vec{F}_3-index(K) <= vec{F}-index(K)
   for every oriented knot K.
"""
import itertools
import json
import os
import subprocess
import sys

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, HERE)
import ftrees as F  # noqa: E402
import oriented as O  # noqa: E402

BIN = os.path.join(HERE, 'bin', 'iota_knots')


def ternary_trees(c):
    if c == 0:
        return [None]
    return [(l, m, r) for c1 in range(c) for c2 in range(c - c1)
            for l in ternary_trees(c1) for m in ternary_trees(c2) for r in ternary_trees(c - 1 - c1 - c2)]


def reps(path, limit):
    """Representatives (top words, bottom words) of the classes of a raw file, round robin over classes."""
    classes = []
    for line in open(path):
        if line.startswith('#'):
            continue
        f = line.rstrip('\n').split('\t')
        classes.append([r.split('|')[:2] for r in f[3].split(';') if r])
    out = []
    for group in itertools.zip_longest(*classes):
        out += [g for g in group if g]
        if len(out) >= limit:
            break
    return out[:limit]


def hyperbolic(pd):
    import snappy  # noqa: F401
    import spherogram
    E = spherogram.Link([[x - 1 for x in c] for c in pd]).exterior()
    for _ in range(5):
        if E.solution_type() == 'all tetrahedra positively oriented':
            return True
        E.randomize()
    return False


def main():
    cmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    samples = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    bad = 0

    for c in range(1, cmax + 1):
        trees = ternary_trees(c)
        k = 0
        for tp in trees:
            for tm in trees:
                if O.tait_colours3(tp, tm) is None:
                    continue
                try:
                    O.oriented_components3(tp, tm)
                    k += 1
                except AssertionError as e:
                    bad += 1
                    print('FAILED', O.ternary_words(tp), O.ternary_words(tm), e)
        print('c = %d: %d pairs of vec{F}_3, colours and orientation ok' % (c, k), flush=True)

    stats = dict(engine=0, inverse=0, skipped=0)
    pairs = reps(os.path.join(HERE, 'results', 'raw_F3vec', 'n9.tsv'), samples // 3) + \
        reps(os.path.join(HERE, 'results', 'raw_F3vec', 'n11.tsv'), samples - samples // 3)
    inp = ''.join('F3 %s %s\n' % (t, b) for t, b in pairs)
    out = subprocess.run([BIN, 'eval'], input=inp, capture_output=True, text=True, check=True).stdout.splitlines()
    for (t, b), line in zip(pairs, out):
        tp, tm = O.ternary_from_words(t.split(',')), O.ternary_from_words(b.split(','))
        pd = O.oriented_pd_code3(tp, tm)
        if not hyperbolic(pd):
            stats['skipped'] += 1
            continue
        cpp = json.loads(dict(kv.split('=', 1) for kv in line.split('\t'))['pd'])
        rel = O.relation_to(pd, cpp)
        if not rel & {'same', 'reverse'}:
            bad += 1
            print('engine mismatch', t, b, rel)
        else:
            stats['engine'] += 1
        rel = O.relation_to(O.oriented_pd_code3(tm, tp), pd)
        if 'mirror reverse' not in rel:
            bad += 1
            print('inverse rule fails', t, b, rel)
        else:
            stats['inverse'] += 1
    print('vec{F}_3 knots: %(engine)d agree with bin/iota_knots, inverse rule on %(inverse)d, '
          '%(skipped)d non-hyperbolic skipped' % stats, flush=True)

    ok = skipped = 0
    per = samples // 3
    for n in (9, 11, 13):
        for t, b in reps(os.path.join(HERE, 'results', 'raw_Fvec', 'n%d.tsv' % n), per):
            tp, tm = F.from_leaf_words(t.split(',')), F.from_leaf_words(b.split(','))
            pd = O.oriented_pd_code(tp, tm)
            if not hyperbolic(pd):
                skipped += 1
                continue
            rel = O.relation_to(O.oriented_pd_code3(O.iota(tp), O.iota(tm)), pd)
            if 'same' not in rel:
                bad += 1
                print('iota does not preserve the oriented knot', t, b, rel)
            else:
                ok += 1
    print('iota: L(iota(g)) = L(g) as oriented knots on %d vec{F} knots (%d non-hyperbolic skipped)' % (ok, skipped))
    print('all checks passed' if not bad else '%d FAILURES' % bad)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
