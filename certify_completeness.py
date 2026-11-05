"""Completeness check of the certified verification (certify_indices.py + certify_retry.py).

usage (from F_index/):   sage -python certify_completeness.py

For every group it checks that
1. every knot with a known index (and at least 3 crossings) has a witness certified by the first pass or by
   the second one;
2. every knot of the table whose index (or, if not found, n_max + 1) is larger than the first n at which its
   HOMFLY-PT class occurs is in the complete check;
3. for every knot of the complete check, every diagram of its class with lower_bound <= n < index was
   certified not to be the knot (first pass, or second pass for the diagrams that it left open or that were in
   crashed tasks), and the number of these diagrams is compared with the complete check;
4. no contradiction was found.
Output: results/certified_completeness.md.
"""
import csv
import json
import os
import sys

import certify_indices as C

HERE = C.HERE


def first_pass(group):
    done = {}
    for line in open(os.path.join(HERE, 'tmp_check', 'certify_%s.jsonl' % group)):
        r = json.loads(line)
        done[json.dumps(r['task'])] = r
    return done


def second_pass(group):
    out = {}
    path = os.path.join(HERE, 'tmp_check', 'certify_retry_%s.jsonl' % group)
    if os.path.exists(path):
        for line in open(path):
            r = json.loads(line)
            out[tuple(r['item'])] = r
    return out


def check(group):
    table, keys, nmax = C.inputs(group)
    col = group + '_index'
    done, retry = first_pass(group), second_pass(group)
    problems, viol = [], 0
    viol += sum(len(r['violations']) for r in done.values())
    viol += sum(r['kind'] == 'violation' for r in retry.values())

    # 1. witnesses: rebuild the batches of the first pass (20, then 5, then 1 knot per task)
    # witnesses found by the targeted searches (n beyond the enumeration) are certified by certify_descent.py
    targeted = [(k, r['top_tree'], r['bottom_tree']) for k, r in table.items()
                if r[col] and 'targeted search' in r['status']]
    wit = [(k, r['top_tree'], r['bottom_tree']) for k, r in table.items()
           if r[col] and r['top_tree'] and int(r['crossing_number']) >= 3 and 'targeted search' not in r['status']]
    certified, rest = set(), list(wit)
    for size, name in ((20, 'witness'), (5, 'witness5')):
        left = []
        for i in range(0, len(rest), size):
            batch = rest[i:i + size]
            r = done.get(json.dumps([name, batch[0][0]]))
            if r is None:
                left += batch
                continue
            bad = {u[0] for u in r['uncertified']} | {v[0] for v in r['violations']}
            certified.update(k for k, _, _ in batch if k not in bad)
        rest = left
    for k, _, _ in rest:
        r = done.get(json.dumps(['witness1', k]))
        if r and not r['uncertified'] and not r['violations']:
            certified.add(k)
    for (g, k, t, b), r in retry.items():
        if r['part'] == 'witnesses' and r['kind'] == 'ok':
            certified.add(k)
    path = os.path.join(HERE, 'results', 'descent_certified.csv')
    desc = {(r['knot'], r['diagram']) for r in csv.DictReader(open(path))
            if r['group'] == group and r['certified'] == 'yes'} if os.path.exists(path) else set()
    certified.update(k for k, t, b in targeted if (k, '%s | %s' % (t, b)) in desc)
    wit += targeted
    missing_w = [k for k, _, _ in wit if k not in certified]
    if missing_w:
        problems.append('witnesses not certified: %s' % missing_w[:20])

    # 2. knots with a gap between the HOMFLY-PT lower bound and the index are in the complete check
    cc = {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', 'complete_check_%s.csv' % group)))}
    gap = [k for k, r in table.items() if r['lower_bound'] and k not in cc
           and int(r['lower_bound']) < (int(r[col]) if r[col] else nmax + 1)]
    if gap:
        problems.append('knots with lower bound < index outside the complete check: %s' % gap[:20])

    # 3. exclusions
    per_knot = {}
    for task in C.exclusion_tasks(group, table, keys, nmax):
        _, knot, path, offset, count = task
        r = done.get(json.dumps(task))
        if r is not None:
            n_done = sum(r['ok'].values()) + len(r['uncertified']) + len(r['violations'])
            if n_done != count:
                problems.append('task %s: %d of %d diagrams' % (task[1:], n_done, count))
            open_items = [(group, knot, t, b) for t, b, _ in r['uncertified']]
        else:
            open_items = []
            with open(path) as f:
                f.seek(offset)
                for _ in range(count):
                    fl = f.readline().rstrip('\n').split('\t')
                    open_items.append((group, knot, fl[1], fl[2]))
        for it in open_items:
            s = retry.get(it)
            if s is None or s['kind'] != 'ok':
                problems.append('exclusion not certified: %s' % (it[1:],))
        per_knot[knot] = per_knot.get(knot, 0) + count
    cmp = [(k, per_knot.get(k, 0), int(r['diagrams_compared'])) for k, r in cc.items()
           if r.get('diagrams_compared', '').isdigit() and per_knot.get(k, 0) > int(r['diagrams_compared'])]
    n_exc = sum(per_knot.values())
    return {'witnesses': len(wit), 'witnesses certified': len(wit) - len(missing_w),
            'complete-check knots': len(cc), 'exclusion diagrams': n_exc,
            'knots with more excluded diagrams than compared by the complete check': len(cmp),
            'contradictions': viol}, problems, cmp


def main():
    lines = ['# Completeness of the certified verification', '',
             'Script `certify_completeness.py` (see its docstring).', '']
    groups = sys.argv[1:] or ['F', 'F3', 'Fvec', 'F3vec']
    for group in groups:
        stats, problems, cmp = check(group)
        lines += ['## %s' % group, ''] + ['- %s: %s' % kv for kv in stats.items()]
        lines += ['- **problems: %d**' % len(problems)] + ['  - %s' % p for p in problems[:50]]
        lines += ['  - more diagrams than compared: %s' % (c,) for c in cmp[:10]] + ['']
    open(os.path.join(HERE, 'results', 'certified_completeness%s.md' % ('' if not sys.argv[1:] else '_' + '_'.join(groups))), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
