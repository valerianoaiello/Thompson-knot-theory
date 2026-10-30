"""
Mutant knots from the literature (Stoimenow, Tabulating and distinguishing mutants, Internat. J. Algebra
Comput. 20 (2010) 525-559; tables 12mut.out and 13mut.out of http://stoimenov.net/stoimeno/homepage/ptab/),
up to 13 crossings, compared with the four indices.

usage (from F_index/):   sage -python mutants_literature.py DIR      (DIR contains 12mut.out and 13mut.out)
                         -> results/mutants_literature.csv

The tables list groups of mutant prime knots (crossing number, KnotScape number, Dowker-Thistlethwaite code),
groups separated by blank lines. The KnotScape number is converted to the KnotInfo name (alternating knots
first: 11a_1..11a_367, 12a_1..12a_1288, 13a_1..13a_4878, then the non-alternating ones), and every conversion
is checked: the knot of the DT code must be isometric to the KnotInfo knot (SnapPy).
For every pair of knots in a group, the indices of results/<G>_index.csv (for the oriented groups
min(index K, index Kr)) and whether an index distinguishes the two knots.
"""
import csv
import os
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
GROUPS = ('F', 'F3', 'Fvec', 'F3vec')
ALTERNATING = {11: 367, 12: 1288, 13: 4878}


def name(c, i):
    return '%da_%d' % (c, i) if i <= ALTERNATING[c] else '%dn_%d' % (c, i - ALTERNATING[c])


def read_groups(path):
    groups, cur = [], []
    for line in open(path):
        f = line.split()
        if not f:
            if cur:
                groups.append(cur)
            cur = []
            continue
        c, i, dt = int(f[0]), int(f[1]), [int(x) for x in f[2:]]
        cur.append((name(c, i), dt))
    if cur:
        groups.append(cur)
    return groups


def check(task):
    """task = [(name, dt)]: True if the DT code gives the KnotInfo knot."""
    import snappy
    import spherogram
    from sage.all import KnotInfo
    out = []
    for nm, dt in task:
        M = snappy.Manifold('DT: [(%s)]' % ','.join(map(str, dt)))
        pd = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + nm).link().pd_code()]
        E = spherogram.Link([[x - 1 for x in c] for c in pd]).exterior()
        try:
            ok = bool(M.is_isometric_to(E))
        except Exception:
            ok = None
        out.append((nm, ok))
    return out


def main():
    from identify_lib import RobustPool
    d = sys.argv[1]
    groups = read_groups(os.path.join(d, '12mut.out')) + read_groups(os.path.join(d, '13mut.out'))
    knots = [k for g in groups for k in g]
    with RobustPool(os.cpu_count()) as pool:
        ok = {}
        for res in pool.map(check, [knots[i:i + 20] for i in range(0, len(knots), 20)]):
            ok.update(res)
    bad = [k for k, v in ok.items() if not v]
    print('%d groups, %d knots; name conversion checked by SnapPy, failures: %s' % (len(groups), len(knots), bad or 'none'))
    tables = {g: {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', g + '_index.csv')))}
              for g in GROUPS}
    rows = []
    for gid, grp in enumerate(groups, 1):
        names = [k for k, _ in grp]
        for a, b in combinations(names, 2):
            row = {'group': gid, 'group_size': len(names), 'knot_1': a, 'knot_2': b,
                   'name_check': 'ok' if ok[a] and ok[b] else 'FAILED'}
            dist = []
            for g in GROUPS:
                ra, rb = tables[g][a], tables[g][b]
                ia, ib = ra[g + '_index'], rb[g + '_index']
                row[g + '_1'] = ia or '>=%s' % ra['lower_bound']
                row[g + '_2'] = ib or '>=%s' % rb['lower_bound']
                if (ia and ib and ia != ib) or (ia and not ib and int(ia) < int(rb['lower_bound'])) or \
                        (ib and not ia and int(ib) < int(ra['lower_bound'])):
                    dist.append(g)
            row['distinguished_by'] = ' '.join(dist)
            rows.append(row)
    with open(os.path.join(HERE, 'results', 'mutants_literature.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    by_c = {}
    for r in rows:
        c = r['knot_1'].split('_')[0][:2]
        by_c.setdefault(c, [0, 0])
        by_c[c][0] += 1
        by_c[c][1] += bool(r['distinguished_by'])
    print('pairs of mutants (all pairs within the groups), distinguished by an index:', by_c)


if __name__ == '__main__':
    main()
