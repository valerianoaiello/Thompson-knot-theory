"""
Applies results/complete_check_<G>.csv (complete_check.py) to results/<G>_index.csv and rewrites
results/<G>_index_summary.txt.

usage (from F_index/):   sage -python apply_complete_check.py GROUP          (GROUP = F, F3, Fvec, F3vec)

identify.sage looks at no more than 50 representatives per HOMFLY class, so it may miss a knot hidden in a
large class; complete_check.py compares every diagram of those classes. Run this script after every
identify.sage run (identify.sage overwrites <G>_index.csv), then make_table.py.
  - FOUND / LOWERED: new index and witness, status 'identified';
  - 'not found up to n = N' with no undecided diagram: status 'not found', lower bound N + 1;
  - confirmed: unchanged (the stored index is exact).
A knot with undecided diagrams below its new index (or below N + 1) keeps a status that says so.
"""
import csv
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def crossings(group, top, bottom):
    """Number of crossings of the witness after spherogram's global simplification."""
    import spherogram
    if group in ('F', 'Fvec'):
        import ftrees as F
        pd = F.pd_code(F.from_leaf_words(top.split(',')), F.from_leaf_words(bottom.split(',')))
    else:
        out = subprocess.run([os.path.join(HERE, 'bin', 'iota_knots'), 'eval'], input='F3 %s %s\n' % (top, bottom),
                             capture_output=True, text=True, check=True).stdout
        pd = json.loads(dict(kv.split('=', 1) for kv in out.strip().split('\t'))['pd'])
    S = spherogram.Link([[x - 1 for x in c] for c in pd])
    S.simplify('global')
    return len(S.crossings)


def summary(group, rows, path):
    old = open(path).read().splitlines() if os.path.exists(path) else []
    head = [line for line in old[:2] if line]
    lines = head + ['complete check applied (results/complete_check_%s.md): every diagram of the HOMFLY classes '
                    'of the knots found late or not found was compared' % group, '']
    for c in sorted({r['crossing_number'] for r in rows}):
        if c < 3:
            continue
        rc = [r for r in rows if r['crossing_number'] == c]
        done = [r for r in rc if r['status'] == 'identified']
        lines.append('crossing number %2d: %4d / %4d knots with known %s-index' % (c, len(done), len(rc), group))
    lines.append('')
    for r in rows:
        if r['status'] == 'identified' and r['crossing_number'] <= 10:
            lines.append('%-8s %s-index %2d   T+ = %s   T- = %s' % (r['knot'], group, int(r[group + '_index']),
                                                                   r['top_tree'], r['bottom_tree']))
    open(path, 'w').write('\n'.join(lines) + '\n')


def main():
    group = sys.argv[1]
    res = os.path.join(HERE, 'results')
    index_csv = os.path.join(res, group + '_index.csv')
    with open(index_csv) as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    by_name = {r['knot']: r for r in rows}
    changed = 0
    for c in csv.DictReader(open(os.path.join(res, 'complete_check_%s.csv' % group))):
        r = by_name[c['knot']]
        unc = int(c['undecided_before_index'] or 0)
        verdict = c['verdict']
        if verdict.startswith(('FOUND', 'LOWERED')):
            r[group + '_index'] = c['new_index']
            r['top_tree'], r['bottom_tree'] = c['top_tree'], c['bottom_tree']
            r['crossings_simplified'] = crossings(group, c['top_tree'], c['bottom_tree'])
            r['status'] = 'identified' if not unc else \
                'identified (%d undecided diagrams with fewer leaves)' % unc
        elif verdict.startswith('not found'):
            nmax = int(re.search(r'up to n = (\d+)', verdict).group(1))
            if not unc:
                r['status'], r['lower_bound'] = 'not found', max(nmax + 1, int(r['lower_bound']))
            else:
                r['status'] = 'not found up to n = %d except %d undecided diagrams' % (nmax, unc)
        else:
            continue
        changed += 1
    for r in rows:
        r['crossing_number'] = int(r['crossing_number'])
    with open(index_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    summary(group, rows, os.path.join(res, group + '_index_summary.txt'))
    print('%s: %d rows updated' % (group, changed))


if __name__ == '__main__':
    main()
