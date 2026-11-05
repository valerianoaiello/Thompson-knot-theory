"""
Certified check of the diagrams found by descent_search.py (results/descent_search.csv; the intermediate ones too,
which give upper bounds).
Unoriented searches (F, F_3, and vec{F}_3 for the table up to orientation): the PD code is recomputed
independently (certify_indices.pd_of: ftrees for F, the C++ evaluator of bin/iota_knots for F_3; oriented.py for
vec{F}_3) and certify_indices.is_K certifies that the diagram is the knot (verified canonical triangulations, or
equal isomorphism signatures). Oriented searches (a 'want' relation): verify_oriented.relation computes, from
verified canonical triangulations, which of K, K^r, K^m, K^mr the diagram is.
usage (from F_index/): sage -python certify_descent.py [processes]  -> results/descent_certified.csv
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OTHER = {'K': {'Kr', 'Km'}, 'Kr': {'K', 'Kmr'}}  # the unrealized orientation, up to the inverse rule
_TARGET = {}


def target(group, knot):
    """Names (K, Kr, Km, Kmr) of the orientation searched by an oriented job (results/reverse_bound_<G>.csv)."""
    if group not in _TARGET:
        _TARGET[group] = {r['knot']: OTHER[r['realized']]
                          for r in csv.DictReader(open(os.path.join(HERE, 'results', 'reverse_bound_%s.csv' % group)))}
    return _TARGET[group][knot]


def certify(row):
    import certify_indices as CI
    import verify_oriented as V
    group, knot = row['group'], row['knot']
    top, bottom = [x.strip() for x in row['diagram'].split('|')]
    try:
        if row['relation'] == 'isometric':
            pd = V.oriented_pd(group, top, bottom) if group == 'F3vec' else CI.pd_of(group, top, bottom)
            res = CI.is_K(pd, knot)
            return row, res[0] == 'ok', '%s %s' % res
        kind, info = V.relation(V.oriented_pd(group, top, bottom), knot, need_volume=False)
        if kind != 'rel':
            return row, False, '%s %s' % (kind, info)
        return row, bool(info & target(group, knot)), 'canonical: ' + ' '.join(sorted(info))
    except Exception as e:
        return row, False, 'error %s' % str(e)[:80]


def main():
    processes = int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count()
    from identify_lib import RobustPool
    rows = list(csv.DictReader(open(os.path.join(HERE, 'results', 'descent_search.csv'))))  # final and intermediate
    out = []
    with RobustPool(processes) as pool:
        for row, ok, info in pool.map(certify, rows):
            out.append(dict(row, certified='yes' if ok else 'no', certificate=info))
    out.sort(key=lambda r: (r['name'], r['knot'], int(r['n'])))
    with open(os.path.join(HERE, 'results', 'descent_certified.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(sum(r['certified'] == 'yes' for r in out), 'of', len(out), 'diagrams certified')


if __name__ == '__main__':
    main()
