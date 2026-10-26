"""
Final table of the F-index: one row per knot with its F-index, its KnotInfo name and a
representative, i.e. an element of F realizing the knot with that number of leaves, given both as
a tree diagram (leaf addresses, 0 = left, 1 = right) and in normal form.

usage (from F_index/, after identify.sage):   python3 make_table.py [F|F3|Fvec] [results_dir]
reads  <results_dir>/F_index.csv and <results_dir>/knots_beyond_table.csv
writes <results_dir>/F_index_table.csv and <results_dir>/F_index_table.md
With F3: F3_index.csv, knots_beyond_table_F3.csv -> F3_index_table.csv / .md; the representative is
the ternary tree diagram (leaf addresses 0, 1, 2 = left, middle, right), without normal form.

Normal form: for a reduced tree diagram (T+, T-) (prime diagrams are reduced) the element is
x_0^a_0 ... x_k^a_k x_k^-b_k ... x_0^-b_0, where a_i (resp. b_i) is the exponent of leaf i of T+
(resp. T-): the number of trailing 0's of its address, minus one if the rest of the address only
contains 1's (the leaf hangs from the right side of the tree). Every normal form is checked by
multiplying the generators with ftrees.py.
"""
import csv
import os
import re
import sys

import ftrees as F

HERE = os.path.dirname(os.path.abspath(__file__))


def leaf_exponents(words):
    out = []
    for w in words:
        t = len(w) - len(w.rstrip('0'))
        out.append(t - 1 if t and set(w.rstrip('0')) <= {'1'} else t)
    return out


def normal_form(top, bottom):
    """Normal form of the element (top, bottom) (comma-separated leaf addresses) of F."""
    tw, bw = top.split(','), bottom.split(',')
    a, b = leaf_exponents(tw), leaf_exponents(bw)
    letters = [i for i, e in enumerate(a) for _ in range(e)]
    letters += [-i if i else '-0' for i in reversed(range(len(b))) for _ in range(b[i])]
    g = (F.from_leaf_words(tw), F.from_leaf_words(bw))
    assert min(a + b) >= 0 and F.word(*letters) == F.reduce_diagram(g), (top, bottom, letters)

    def power(i, e):
        return 'x%d' % i + ('^%d' % e if e != 1 else '')

    pos = [power(i, e) for i, e in enumerate(a) if e]
    neg = [power(i, -e) for i, e in reversed(list(enumerate(b))) if e]
    return ' '.join(pos + neg) or '1'


def crossing_key(name):
    m = re.match(r'(\d+)([an]?)_(\d+)', name)
    return (int(m.group(1)), m.group(2), int(m.group(3))) if m else (99, '', 0)


def main():
    group = sys.argv[1] if len(sys.argv) > 1 else 'F'
    assert group in ('F', 'F3', 'Fvec')
    d = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'results')
    suffix = {'F': '', 'F3': '_F3', 'Fvec': '_Fvec'}[group]
    col = group + '_index'
    rows = []
    for r in csv.DictReader(open(os.path.join(d, col + '.csv'))):
        if r[col] and r['knot'] != '0_1':
            rows.append({col: int(r[col]), 'knot': r['knot'], 'note': '',
                         'top_tree': r['top_tree'], 'bottom_tree': r['bottom_tree']})
    beyond = os.path.join(d, 'knots_beyond_table%s.csv' % suffix)
    if os.path.exists(beyond):
        for r in csv.DictReader(open(beyond)):
            rows.append({col: int(r['upper_bound_' + col]), 'knot': r['knot'],
                         'note': 'not in KnotInfo (SnapPy name); upper bound',
                         'top_tree': r['top_tree'], 'bottom_tree': r['bottom_tree']})
    for r in rows:
        r['normal_form'] = normal_form(r['top_tree'], r['bottom_tree']) if group != 'F3' else ''
    rows.sort(key=lambda r: (r[col], crossing_key(r['knot'])))

    fields = [col, 'knot', 'normal_form', 'top_tree', 'bottom_tree', 'note']
    if group == 'F3':
        fields.remove('normal_form')
        for r in rows:
            del r['normal_form']
    name = '%s_index_table' % group
    with open(os.path.join(d, name + '.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    rawdir = os.path.join(d, {'F': 'raw', 'F3': 'raw_F3', 'Fvec': 'raw_Fvec'}[group])
    nmax = max(int(m) for m in re.findall(r'n(\d+)\.tsv', ' '.join(os.listdir(rawdir)))) \
        if os.path.isdir(rawdir) else None
    G = {'F': 'F', 'F3': 'F₃', 'Fvec': 'F⃗'}[group]
    with open(os.path.join(d, name + '.md'), 'w') as f:
        f.write('# %s-index of knots\n\n' % G)
        if nmax:
            f.write('Computed with all tree diagrams with n <= %d: a knot that is not listed has '
                    '%s-index > %d (or is the unknot, index 1).\n' % (nmax, G, nmax))
        if group != 'F3':
            f.write('Knots up to mirror image, KnotInfo names. The representative is an element of %s '
                    'realizing the knot with %s-index leaves: normal form and tree diagram (leaf addresses, '
                    '0 = left, 1 = right).\n' % (G, G))
            if group == 'Fvec':
                f.write('F⃗ is Jones\' oriented subgroup: the representatives are oriented knots (the '
                        'orientation comes from the 2-colouring of the Tait graph). Knots are also listed up '
                        'to reversal of the orientation, which HOMFLY does not see.\n')
            f.write('\n| %s-index | knot | representative (normal form) | top tree | bottom tree |\n' % G)
            f.write('|---|---|---|---|---|\n')
        else:
            f.write('Knots up to mirror image, KnotInfo names. n = number of internal vertices of each '
                    'ternary tree + 1. The representative is a ternary tree diagram of F₃ realizing the '
                    'knot (leaf addresses, 0 = left, 1 = middle, 2 = right).\n\n')
            f.write('| F₃-index | knot | top tree | bottom tree |\n')
            f.write('|---|---|---|---|\n')
        for r in rows:
            knot = r['knot'] + (' *' if r['note'] else '')
            nf = ' %s |' % r['normal_form'] if group != 'F3' else ''
            f.write('| %d | %s |%s `%s` | `%s` |\n' % (r[col], knot, nf, r['top_tree'], r['bottom_tree']))
        if any(r['note'] for r in rows):
            f.write('\n\\* knot with 14 or 15 crossings, not in KnotInfo (name from the SnapPy census); '
                    'the number is an upper bound for its %s-index.\n' % G)
    print('%d knots written to %s' % (len(rows), os.path.join(d, name + '.md')))


if __name__ == '__main__':
    main()
