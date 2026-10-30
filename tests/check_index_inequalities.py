"""
Consistency of the final tables: F3-index <= F-index, F3-index <= vec{F}3-index <= vec{F}-index and
F-index <= vec{F}-index, for every knot.

usage (from F_index/):   sage -python tests/check_index_inequalities.py

A violation is a knot whose lower bound in the smaller group exceeds its known index in the larger one.
Also checked directly: for every vec{F} witness (T+, T-) with n leaves, iota(T+, T-) is in vec{F}3, has n - 1
internal vertices per tree, and the knot of bin/iota_knots eval has the HOMFLY polynomial (Sage, up to
mirror image) of the PD code of the witness computed by ftrees.py (an independent implementation), so
vec{F}3-index <= n by an explicit diagram.
"""
import csv
import os
import subprocess
import sys

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ftrees as F  # noqa: E402
from check_F3vec import in_vec, iota, words  # noqa: E402


def load(g):
    out = {}
    for r in csv.DictReader(open(os.path.join(HERE, 'results', g + '_index.csv'))):
        out[r['knot']] = (int(r[g + '_index']) if r[g + '_index'] else None, int(r['lower_bound']), r)
    return out


def same_homfly(task):
    from sage.all import Link
    i, comps, pd3, top, bottom = task
    if comps != '1':
        return i, False
    pd = F.pd_code(F.from_leaf_words(top.split(',')), F.from_leaf_words(bottom.split(',')))
    h3, h = Link(pd3).homfly_polynomial(), Link(pd).homfly_polynomial()
    return i, h3 == h or h3 == Link(pd).mirror_image().homfly_polynomial()


def main():
    t = {g: load(g) for g in ('F', 'F3', 'Fvec', 'F3vec')}
    bad = 0
    for small, big in (('F3', 'F'), ('F3', 'F3vec'), ('F3vec', 'Fvec'), ('F', 'Fvec')):
        v = [k for k in t[small] if k in t[big] and t[big][k][0] is not None and t[small][k][1] > t[big][k][0]]
        bad += len(v)
        print('%s-index <= %s-index: %d knots compared, %d violations %s' % (
            small, big, sum(1 for k in t[small] if k in t[big] and t[big][k][0] is not None), len(v), v[:10]))
    rows = [(k, n, r) for k, (n, _, r) in t['Fvec'].items() if n and r['top_tree']]
    lines, homfly = [], []
    for k, n, r in rows:
        tp = F.from_leaf_words(r['top_tree'].split(','))
        tm = F.from_leaf_words(r['bottom_tree'].split(','))
        a, b = iota(tp), iota(tm)
        if not in_vec(a, b) or len(words(a)) != 2 * n - 1:
            bad += 1
            print('iota of the witness of %s is not in vec{F}3 / wrong size' % k)
        lines.append('F3 %s %s\n' % (','.join(words(a)), ','.join(words(b))))
    out = subprocess.run([os.path.join(HERE, 'bin', 'iota_knots'), 'eval'], input=''.join(lines),
                         capture_output=True, text=True, check=True).stdout.splitlines()
    import json
    from identify_lib import RobustPool
    tasks = []
    for i, (k, n, r) in enumerate(rows):
        f3 = dict(kv.split('=', 1) for kv in out[i].split('\t'))
        tasks.append((i, f3['components'], json.loads(f3['pd']), r['top_tree'], r['bottom_tree']))
    same = {}
    with RobustPool(os.cpu_count()) as pool:
        for i, ok in pool.map(same_homfly, tasks):
            same[i] = ok
    for t in pool.dropped:
        same[t[0]] = False
    for i, (k, n, r) in enumerate(rows):
        if not same[i]:
            bad += 1
            print('iota changes the knot of the witness of %s' % k)
        f3vec = t['F3vec'].get(k)
        if f3vec and f3vec[1] > n:
            bad += 1
            print('%s: vec{F}3 lower bound %d > %d, but iota of the vec{F} witness has n = %d' % (k, f3vec[1], n, n))
    print('iota of %d vec{F} witnesses: %s' % (len(rows), 'ok' if not bad else 'see above'))
    print('all checks passed' if not bad else '%d FAILURES' % bad)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
