"""
For the non-invertible knots with one orientation realized in vec{F}_3 at n = 11 and the other not: the reverse
moves of Theorem 3.2(vii) of the paper (the ternary versions of the two moves of Aiello, Rev. Un. Mat. Argentina
69 (2026), Theorem 4.2) bound the index of the other orientation. If the stored minimal diagram of the realized
orientation has first and last Tait vertices of different colours, the move with two new vertices gives the
reverse knot at n = 13, so the other index is exactly 13 (it is > 11 and odd); otherwise the move with four new
vertices gives 13 or 15. Only the stored witness is used: another minimal diagram with ends of different colours
could turn some '13-15' into '13'.
usage (from F_index/): python3 reverse_bound_F3vec.py  -> results/reverse_bound_F3vec.csv
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oriented as O  # noqa: E402

csv.field_size_limit(10**9)


def main():
    rows = []
    for r in csv.DictReader(open(os.path.join(HERE, 'results', 'oriented_index_F3vec.csv'))):
        a, b = r['index_K'], r['index_Kr']
        if a.isdigit() == b.isdigit():
            continue
        want = 'K' if a.isdigit() else 'Kr'
        n = int(r['index_' + want])
        t, bb = [x.strip() for x in r['witness_' + want].split('|')]
        col = O.tait_colours3(O.ternary_from_words(t.split(',')), O.ternary_from_words(bb.split(',')))
        different = col[0] != col[-1]
        rows.append({'knot': r['knot'], 'realized': want, 'index_realized': n,
                     'index_other': str(n + 2) if different else '%d-%d' % (n + 2, n + 4),
                     'witness_ends_different_colours': 'yes' if different else 'no'})
    with open(os.path.join(HERE, 'results', 'reverse_bound_F3vec.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), 'knots:', sum(r['witness_ends_different_colours'] == 'yes' for r in rows), 'exact,',
          sum(r['witness_ends_different_colours'] == 'no' for r in rows), 'with two possible values')


if __name__ == '__main__':
    main()
