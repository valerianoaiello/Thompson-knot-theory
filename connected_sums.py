"""Indices of some connected sums of two knots, compared with the bound ind(K1 # K2) <= ind(K1) + ind(K2) - 1.

usage (from F_index/):   sage -python connected_sums.py

The enumerations skip the non-prime tree diagrams (grafts), but this loses nothing below the bound: a graft of
size m realizing K1 # K2 has two pieces whose knots have K1 # K2 as connected sum; by the uniqueness of the prime
decomposition either the pieces realize K1 and K2, and m >= ind(K1) + ind(K2) - 1, or one piece is trivial and
the other one, which is smaller, already realizes K1 # K2. Hence:
- lower bound: the first n at which the HOMFLY-PT class of K1 # K2 (the product of the polynomials) occurs in the
  enumeration (exact: the polynomial is computed for every diagram);
- witness: a diagram of that class whose simplified diagram is a connected sum of two pieces, identified by their
  crossing number and determinant (the factors have at most 4 crossings), with their chirality given by the
  signature.
All the factors are invertible, so the orientation plays no role in the oriented groups.
Output: results/connected_sums.md.
"""
import csv
import os
import re
from collections import Counter

import certify_indices as C
from make_table import normal_form, normal_form3

HERE = C.HERE
RAW = {'F': 'raw', 'F3': 'raw_F3', 'Fvec': 'raw_Fvec', 'F3vec': 'raw_F3vec'}
GROUPS = ('F', 'F3', 'Fvec', 'F3vec')
# (name, factor 1, factor 2, the two factors have the same chirality); 4_1 is amphicheiral
SUMS = [('3_1 # 3_1 (granny knot)', '3_1', '3_1', True),
        ('3_1 # 3_1^m (square knot)', '3_1', '3_1', False),
        ('3_1 # 4_1', '3_1', '4_1', True)]
PIECE = {(3, 3): '3_1', (4, 5): '4_1'}  # (crossings, determinant) of the knots with at most 4 crossings

csv.field_size_limit(10**9)


def parse(key):
    """HOMFLY-PT key of the enumerators (terms c*L^a*M^b) -> {(a, b): c}."""
    d = {}
    for c, a, b in re.findall(r'(-?\d+)\*L\^(-?\d+)\*M\^(-?\d+)', key):
        d[(int(a), int(b))] = d.get((int(a), int(b)), 0) + int(c)
    return {e: c for e, c in d.items() if c}


def mul(p, q):
    r = {}
    for (a, b), c in p.items():
        for (x, y), z in q.items():
            r[(a + x, b + y)] = r.get((a + x, b + y), 0) + c * z
    return {e: c for e, c in r.items() if c}


def mirror(p):
    return {(-a, b): c for (a, b), c in p.items()}  # knots: only even powers of M


def table(group):
    return {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', group + '_index.csv')))}


def key_of(knot):
    """HOMFLY-PT key of a knot, read from the class of its F witness."""
    r = table('F')[knot]
    w = (r['top_tree'], r['bottom_tree'])
    for line in open(os.path.join(HERE, 'results', 'raw', 'n%s.tsv' % r['F_index'])):
        f = line.rstrip('\n').split('\t')
        if not f[0].startswith('#') and any(tuple(x.split('|')[:2]) == w for x in f[3].split(';')):
            return parse(f[0])
    raise ValueError(knot)


def classify(group, top, bottom):
    """(factor names, same chirality) of a diagram that is a connected sum of two knots with <= 4 crossings."""
    import snappy  # noqa: F401
    import spherogram
    L = spherogram.Link([[x - 1 for x in c] for c in C.pd_of(group, top, bottom)])
    L.simplify('global')
    pieces = L.deconnect_sum()
    if len(pieces) != 2:
        return None
    out = []
    for P in pieces:
        P.simplify('global')
        name = PIECE.get((len(P.crossings), P.determinant()))
        if name is None:
            return None
        out.append((name, P.signature()))
    names = tuple(sorted(n for n, _ in out))
    if names == ('3_1', '4_1'):
        return names, True
    return names, out[0][1] == out[1][1]


def first_class(group, target, nmax):
    step = 2 if group in ('Fvec', 'F3vec') else 1
    for n in range(1 if step == 2 else 2, nmax + 1, step):
        path = os.path.join(HERE, 'results', RAW[group], 'n%d.tsv' % n)
        if not os.path.exists(path):
            continue
        for line in open(path):
            f = line.rstrip('\n').split('\t')
            if not f[0].startswith('#') and 'L^' in f[0] and parse(f[0]) in target:
                return n, int(f[1]), [x.split('|')[:2] for x in f[3].split(';')]
    return None


def main():
    lines = ['# Indices of connected sums', '', 'Script `connected_sums.py` (see its docstring). The bound is '
             'ind(K1) + ind(K2) - 1 (graft of two minimal diagrams).', '',
             '| knot | ' + ' | '.join('%s (bound)' % g for g in GROUPS) + ' |', '|---' * (len(GROUPS) + 1) + '|']
    witnesses = []
    for name, k1, k2, same in SUMS:
        p1, p2 = key_of(k1), key_of(k2)
        P = mul(p1, p2 if same else mirror(p2))
        target = (P, mirror(P))
        want = (tuple(sorted((k1, k2))), same)
        cells = []
        for g in GROUPS:
            T = table(g)
            bound = int(T[k1][g + '_index']) + int(T[k2][g + '_index']) - 1
            hit = first_class(g, target, bound)
            if hit is None:
                cells.append('? (%d)' % bound)
                continue
            n, size, reps = hit
            res = Counter()
            wit = None
            for t, b in reps[:8]:
                c = classify(g, t, b)
                res[c == want] += 1
                if c == want and wit is None:
                    wit = (t, b)
            if wit is None:
                cells.append('? (%d)' % bound)
                continue
            cells.append('%s%d%s (%d)' % ('**' if n < bound else '', n, '**' if n < bound else '', bound))
            nf = (normal_form3 if g in ('F3', 'F3vec') else normal_form)(wit[0], wit[1])
            witnesses.append('- %s in %s, n = %d (%d diagrams in the class, %d of %d checked): `%s`; trees `%s | %s`'
                             % (name, g, n, size, res[True], sum(res.values()), nf, wit[0], wit[1]))
            print(name, g, n, bound, flush=True)
        lines.append('| %s | %s |' % (name, ' | '.join(cells)))
    lines += ['', 'Bold: the inequality is strict.', '', '## Witnesses', '',
              'Normal form (x_i: generators of F; y_i: generators of F_3, with y_{2m} = iota(x_m), see make_table.py) '
              'and tree diagram (leaf addresses of the top and bottom trees).', ''] + witnesses
    open(os.path.join(HERE, 'results', 'connected_sums.md'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
