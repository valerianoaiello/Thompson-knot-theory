"""
Applies the certified results of the targeted searches (results/descent_certified.csv, certify_descent.py) to
the tables. Run it after apply_complete_check.py, reverse_bound.py and reverse_bound_F3vec.py, which rewrite
the files below; it is idempotent.

1. results/<G>_index.csv: a knot not found by the enumeration (n <= n_max) with a certified diagram of size n
   gets index n if n is its lower bound (the next n allowed in the group: knots only occur for odd n in
   vec{F} and vec{F}_3), status 'identified (targeted search, n beyond the enumeration)'; otherwise its status
   records the upper bound.
   In vec{F}, a knot whose HOMFLY-PT class has no diagram with 19 leaves (results/Fvec_n19_classes.csv,
   fvec_beyond17.py) gets lower bound 20 first.
2. results/reverse_bound_<G>.csv (vec{F}, vec{F}_3): a knot whose other orientation was 'a-b' gets index_other
   = n when a certified diagram of size n = a realizes the other orientation (column other_orientation_diagram).
usage (from F_index/): python3 scripts/apply_descent.py
"""
import csv
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root (the scripts are in scripts/)
csv.field_size_limit(10**9)
ODD = {'Fvec', 'F3vec'}


def best(rows):
    """(group, knot) -> (n, diagram) of the smallest certified diagram."""
    out = {}
    for r in rows:
        k, n = (r['group'], r['knot']), int(r['n'])
        if r['certified'] == 'yes' and (k not in out or n < out[k][0]):
            out[k] = (n, r['diagram'])
    return out


def write(path, rows, fields):
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    rows = list(csv.DictReader(open(os.path.join(HERE, 'results', 'descent_certified.csv'))))
    unoriented = best(r for r in rows if r['relation'] == 'isometric')
    oriented = best(r for r in rows if r['relation'] != 'isometric')

    for G in ('F', 'F3', 'Fvec', 'F3vec'):
        path = os.path.join(HERE, 'results', '%s_index.csv' % G)
        table = list(csv.DictReader(open(path)))
        col, changed = G + '_index', []
        n19 = os.path.join(HERE, 'results', 'Fvec_n19_classes.csv')
        if G == 'Fvec' and os.path.exists(n19):
            # fvec_beyond17.py: no knot diagram with 19 leaves in the HOMFLY-PT class -> lower bound 20 (index >= 21)
            absent = {x['knot'] for x in csv.DictReader(open(n19)) if x['diagrams_at_19'] == '0'}
            raised = 0
            for r in table:
                if r['knot'] in absent and r['lower_bound'] == '18':
                    r['lower_bound'], raised = '20', raised + 1
            print(G, 'lower bound 18 -> 20 (class absent at n = 19):', raised)
        for r in table:
            if (G, r['knot']) not in unoriented or r[col] and 'targeted search' not in r['status']:
                continue
            n, d = unoriented[(G, r['knot'])]
            lb = int(r['lower_bound'])
            if G in ODD and lb % 2 == 0:
                lb += 1
            if n == lb:
                r[col] = str(n)
                r['top_tree'], r['bottom_tree'] = [x.strip() for x in d.split('|')]
                r['status'] = 'identified (targeted search, n beyond the enumeration)'
            else:
                r['status'] = r['status'].split('; upper bound')[0] + '; upper bound %d (targeted search)' % n
            changed.append('%s %s' % (r['knot'], r[col] or '<= %d' % n))
        write(path, table, list(table[0]))
        print(G, 'index table:', ', '.join(changed) or 'no change')

    for G in ('Fvec', 'F3vec'):
        path = os.path.join(HERE, 'results', 'reverse_bound_%s.csv' % G)
        table = list(csv.DictReader(open(path)))
        fields = list(table[0]) + (['other_orientation_diagram'] if 'other_orientation_diagram' not in table[0] else [])
        n_changed = 0
        for r in table:
            r.setdefault('other_orientation_diagram', '')
            if (G, r['knot']) in oriented and '-' in r['index_other']:
                n, d = oriented[(G, r['knot'])]
                if n == int(r['index_other'].split('-')[0]):
                    r['index_other'], r['other_orientation_diagram'] = str(n), d
                    n_changed += 1
        write(path, table, fields)
        print(G, 'reverse bounds made exact:', n_changed, '; still two values:',
              sum('-' in r['index_other'] for r in table))


if __name__ == '__main__':
    main()
