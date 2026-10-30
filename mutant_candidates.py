"""
Candidate mutant pairs among the knots of KnotInfo, and their indices.

usage (from F_index/):   sage -python mutant_candidates.py [processes]      -> results/mutant_candidates.csv / .md

Mutant knots have the same HOMFLY polynomial and, if hyperbolic, the same volume (Ruberman). Two distinct
knots with ≤ 13 crossings with the same HOMFLY polynomial (up to mirror image) and the same hyperbolic volume
(|difference| < 1e-8) are listed as candidate mutants: these are necessary conditions only, mutation is not
checked. For each pair the four indices of results/<G>_index.csv are given (for the oriented groups:
min(index K, index Kr)), and the pair is marked when an index distinguishes it: both indices known and
different, or a known index of one knot smaller than the exact lower bound of the other.
"""
import csv
import os
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
GROUPS = ('F', 'F3', 'Fvec', 'F3vec')


def volume(task):
    import snappy  # noqa: F401
    import spherogram
    from sage.all import KnotInfo
    out = []
    for name in task:
        pd = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + name).link().pd_code()]
        E = spherogram.Link([[x - 1 for x in c] for c in pd]).exterior()
        v = None
        for _ in range(10):
            if E.solution_type() == 'all tetrahedra positively oriented':
                v = float(E.volume())
                break
            E.randomize()
        out.append((name, v))
    return out


def main():
    from identify_lib import RobustPool
    processes = int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count()
    tables = {g: {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', g + '_index.csv')))}
              for g in GROUPS}
    names = [k for k, r in tables['F'].items() if int(r['crossing_number']) >= 3]
    from sage.all import LaurentPolynomialRing, ZZ, sage_eval
    R = LaurentPolynomialRing(ZZ, 'v,z')
    v, z = R.gens()

    def canonical_vz(s):  # the mirror image replaces v by v^-1
        h = sage_eval(s, locals={'v': v, 'z': z})
        return min(str(h), str(h.subs(v=v ** -1)))

    by_homfly = {}
    for k in names:  # HOMFLY up to mirror image (KnotInfo's diagram of a knot may be the mirror of its mutant's)
        by_homfly.setdefault(canonical_vz(tables['F'][k]['homfly_vz']), []).append(k)
    todo = sorted({k for ks in by_homfly.values() if len(ks) > 1 for k in ks})
    print('%d knots share their HOMFLY polynomial with another knot' % len(todo), flush=True)
    vol = {}
    with RobustPool(processes) as pool:
        for res in pool.map(volume, [todo[i:i + 20] for i in range(0, len(todo), 20)]):
            vol.update(res)
    rows = []
    for ks in by_homfly.values():
        for a, b in combinations(sorted(ks), 2):
            if vol.get(a) is None or vol.get(b) is None or abs(vol[a] - vol[b]) > 1e-8:
                continue
            row = {'knot_1': a, 'knot_2': b, 'volume': '%.8f' % vol[a]}
            distinguished = []
            for g in GROUPS:
                ra, rb = tables[g][a], tables[g][b]
                fa = ra[g + '_index'] or '>=%s' % ra['lower_bound']
                fb = rb[g + '_index'] or '>=%s' % rb['lower_bound']
                row[g + '_1'], row[g + '_2'] = fa, fb
                ia, ib = ra[g + '_index'], rb[g + '_index']
                # the indices of the tables are exact, the lower bounds too
                if (ia and ib and ia != ib) or (ia and not ib and int(ia) < int(rb['lower_bound'])) or \
                        (ib and not ia and int(ib) < int(ra['lower_bound'])):
                    distinguished.append(g)
            row['distinguished_by'] = ' '.join(distinguished)
            rows.append(row)
    rows.sort(key=lambda r: (int(tables['F'][r['knot_1']]['crossing_number']), r['knot_1'], r['knot_2']))
    with open(os.path.join(HERE, 'results', 'mutant_candidates.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print('%d candidate pairs, %d distinguished by some index' % (
        len(rows), sum(1 for r in rows if r['distinguished_by'])), flush=True)


if __name__ == '__main__':
    main()
