"""
Table of the vec{F}-index (with F-, F_3- and vec{F}_3-index for comparison) of all the knots with few crossings.

usage (from F_index/, after identify.sage for F, F3 and Fvec):   python3 small_knots_table.py [max_crossings]
reads  results/Fvec_index.csv, results/F_index.csv, results/F3_index.csv, results/F3vec_index.csv,
       results/reverse_scan.csv
writes results/Fvec_index_upto<C>.md and .csv

One row per knot of KnotInfo up to mirror image, including the knots not found yet (lower bound). For the
non-invertible knots (results/reverse_scan.csv) the vec{F}-index of K and of its reverse Kr is given too.
"""
import csv
import os
import re
import sys

from make_table import normal_form

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, 'results')


def load(name, col):
    path = os.path.join(R, name)
    if not os.path.exists(path):
        return {}
    return {r['knot']: r for r in csv.DictReader(open(path))}


def value(r, col):
    if not r:
        return '?'
    return r[col] if r[col] else '≥ %s' % r['lower_bound']


def main():
    cmax = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    vec, f, f3 = load('Fvec_index.csv', 'Fvec_index'), load('F_index.csv', 'F_index'), load('F3_index.csv', 'F3_index')
    vec3 = load('F3vec_index.csv', 'F3vec_index')
    rev = load('reverse_scan.csv', None)
    # lower bounds are odd in vec{F} (parity theorem: knots only occur for odd n, results/parity_theorem.md)
    rows = []
    for knot, r in vec.items():
        c = int(r['crossing_number'])
        if c > cmax:
            continue
        idx = r['Fvec_index']
        lb = int(r['lower_bound'])
        vec_value = idx if idx else '≥ %d' % (lb + 1 - lb % 2 if lb % 2 == 0 else lb)
        orient = ''
        if knot in rev:
            orient = 'K: %s, Kr: %s' % (rev[knot]['Fvec_index_K'], rev[knot]['Fvec_index_Kr'])
        rows.append({'knot': knot, 'crossing_number': c, 'Fvec_index': vec_value,
                     'F3vec_index': value(vec3.get(knot), 'F3vec_index'),
                     'F_index': value(f.get(knot), 'F_index'), 'F3_index': value(f3.get(knot), 'F3_index'),
                     'orientations': orient,
                     'normal_form': normal_form(r['top_tree'], r['bottom_tree']) if idx and r['top_tree'] else '',
                     'top_tree': r['top_tree'] if idx else '', 'bottom_tree': r['bottom_tree'] if idx else ''})

    def key(r):
        c, rest = r['knot'].split('_')
        return (int(c.rstrip('an')), int(re.sub(r'\D', '', rest)))

    rows.sort(key=key)
    name = os.path.join(R, 'Fvec_index_upto%d' % cmax)
    with open(name + '.csv', 'w', newline='') as fo:
        w = csv.DictWriter(fo, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    nmax = max(int(m) for m in re.findall(r'n(\d+)\.tsv', ' '.join(os.listdir(os.path.join(R, 'raw_Fvec')))))
    known = sum(1 for r in rows if not r['Fvec_index'].startswith('≥'))
    with open(name + '.md', 'w') as fo:
        fo.write('# vec{F}-index of the knots with at most %d crossings\n\n' % cmax)
        fo.write('All tree diagrams of vec{F} with n <= %d leaves (knots only occur for odd n: results/parity_theorem.md): %d of the %d knots '
                 'have a known vec{F}-index; for the others "≥" is a lower bound (no diagram with fewer leaves has '
                 'their HOMFLY polynomial). Knots up to mirror image (and, for invertible knots, the orientation '
                 'does not matter: L(g^-1) is the mirror image of the reverse of L(g)). For the non-invertible '
                 'knots the index of K (orientation of KnotInfo) and of its reverse Kr is given. F-index and '
                 'F₃-index and F⃗₃-index (oriented subgroup of F₃) for comparison. The representative is an element of vec{F} realizing the index.\n\n'
                 % (nmax, known, len(rows)))
        fo.write('| knot | vec{F}-index | orientations | F⃗₃-index | F-index | F₃-index | representative (normal form) | '
                 'top tree | bottom tree |\n|---|---|---|---|---|---|---|---|---|\n')
        for r in rows:
            fo.write('| %s | %s | %s | %s | %s | %s | %s | %s | %s |\n' % (
                r['knot'], r['Fvec_index'], r['orientations'], r['F3vec_index'], r['F_index'], r['F3_index'], r['normal_form'],
                '`%s`' % r['top_tree'] if r['top_tree'] else '', '`%s`' % r['bottom_tree'] if r['bottom_tree'] else ''))
    print('%s.md: %d knots, %d with known vec{F}-index' % (name, len(rows), known))


if __name__ == '__main__':
    main()
