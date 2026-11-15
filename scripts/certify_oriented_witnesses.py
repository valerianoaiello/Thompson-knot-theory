"""
Certified orientation of the witnesses of K and K^r of given non-invertible knots (results/oriented_index_<G>.csv),
also when index(K) = index(K^r), a case not covered by verify_oriented.py.

usage (from F_index/):   sage -python scripts/certify_oriented_witnesses.py GROUP KNOT [KNOT ...]
                         (GROUP = Fvec or F3vec)

Every witness is compared with the oriented KnotInfo diagram of the knot through the verified canonical
retriangulations of the two complements (interval arithmetic, SnapPy verified=True) and all their combinatorial
isomorphisms; their action on (meridian, longitude) gives exactly which of K, K^r, K^m, K^mr the witness is
(relation() of verify_oriented.py, step 3). By the inverse rule, g^-1 then realizes K^mr, K^m, K^r or K.
Used for the Kinoshita-Terasaka knot 11n_42 in vec{F} (paper, theorem on mutants: index 15 in every orientation).
Output: results/oriented_witnesses_certified_<G>.md.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root (the scripts are in scripts/)
sys.path.insert(0, os.path.join(HERE, 'scripts'))
csv.field_size_limit(10**9)

import verify_oriented as V  # noqa: E402


def main():
    group, knots = sys.argv[1], sys.argv[2:]
    rows = {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', 'oriented_index_%s.csv' % group)))}
    lines = ['# Certified orientation of the witnesses of K and K^r (%s)' % group, '',
             'Script `certify_oriented_witnesses.py` (see its docstring): verified canonical retriangulations and '
             'their combinatorial isomorphisms, action on (meridian, longitude). K = KnotInfo orientation.', '',
             '| knot | orientation | leaves | certified relation | ok |', '|---|---|---|---|---|']
    bad = 0
    for knot in knots:
        r = rows[knot]
        for o in ('K', 'Kr'):
            w = r['witness_' + o]
            if not w:
                lines.append('| %s | %s | | no witness | |' % (knot, o))
                continue
            top, bottom = [x.strip() for x in w.split('|')]
            kind, info = V.relation(V.oriented_pd(group, top, bottom), knot, need_volume=False)
            got = ', '.join(sorted(info)) if kind == 'rel' else '%s (%s)' % (kind, info)
            ok = kind == 'rel' and o in info
            bad += not ok
            lines.append('| %s | %s | %d | %s | %s |' % (knot, o, len(top.split(',')), got, 'yes' if ok else '**no**'))
            print(lines[-1], flush=True)
    lines += ['', '**Witnesses not certified: %d.**' % bad]
    out = os.path.join(HERE, 'results', 'oriented_witnesses_certified_%s.md' % group)
    open(out, 'w').write('\n'.join(lines) + '\n')
    print('written', out)


if __name__ == '__main__':
    main()
