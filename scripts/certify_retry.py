"""Second pass of certify_indices.py on what the first pass left open.

usage (from F_index/):   sage -python scripts/certify_retry.py GROUP [processes] [timeout]

1. Witnesses not certified (timeout, or K not hyperbolic): first same_complement (equal isomorphism
   signatures of random retriangulations of the two complements, exact, valid also for satellite knots), then
   is_K with the longer timeout.
2. Exclusions not certified: not_K with the longer timeout.
3. Crashed tasks (exclusion tasks of 25 diagrams, or witnesses, missing from tmp_check/certify_<G>.jsonl):
   every diagram again, one per task, so that RobustPool isolates the diagram that crashes SnapPy.
Progress: tmp_check/certify_retry_<G>.jsonl (resumed). Output: results/certified_retry_<G>.md.
"""
import ast
import json
import os
import re
import sys

import certify_indices as C

HERE = C.HERE


def witness_retry(item):
    group, knot, top, bottom = item
    import snappy  # noqa: F401
    import spherogram

    def run():
        pd = C.pd_of(group, top, bottom)
        L = spherogram.Link([[x - 1 for x in c] for c in pd])
        L.simplify('global')
        K = spherogram.Link([[x - 1 for x in c] for c in C.knot_pd(knot)])
        if C.same_complement(L.exterior(), K.exterior()):
            return 'ok', 'isosig'
        return C.is_K(pd, knot)
    try:
        kind, info = C.timed(run)
    except Exception as e:
        kind, info = 'uncertified', str(e)[:60]
    return {'item': list(item), 'part': 'witnesses', 'kind': kind, 'info': info}


def exclusion_retry(item):
    group, knot, top, bottom = item
    try:
        kind, info = C.timed(C.not_K, C.pd_of(group, top, bottom), knot)
    except Exception as e:
        kind, info = 'uncertified', str(e)[:60]
    return {'item': list(item), 'part': 'exclusions', 'kind': kind, 'info': info}


def open_items(group):
    """(witness items, exclusion items) left open by the first pass."""
    done = {}
    for line in open(os.path.join(HERE, 'tmp_check', 'certify_%s.jsonl' % group)):
        r = json.loads(line)
        done[json.dumps(r['task'])] = r
    wit, exc = [], []
    for r in done.values():
        if r['task'][0].startswith('witness'):
            wit += [(group, k, t, b) for k, t, b, _ in r['uncertified']]
        else:
            exc += [(group, r['task'][1], t, b) for t, b, _ in r['uncertified']]
    table, keys, nmax = C.inputs(group)
    for task in C.exclusion_tasks(group, table, keys, nmax):
        if json.dumps(task) in done:
            continue
        _, knot, path, offset, count = task
        with open(path) as f:
            f.seek(offset)
            for _ in range(count):
                fl = f.readline().rstrip('\n').split('\t')
                exc.append((group, knot, fl[1], fl[2]))
    # crashed witness tasks, as reported by the first pass
    md = open(os.path.join(HERE, 'results', 'certified_%s.md' % group)).read()
    for m in re.finditer(r"^- \['%s', (\[\(.*\)\])\]$" % group, md, re.M):
        wit += [(group,) + tuple(w) for w in ast.literal_eval(m.group(1))]
    return wit, exc


def main():
    from identify_lib import RobustPool
    group = sys.argv[1]
    processes = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    C.TIMEOUT = int(sys.argv[3]) if len(sys.argv) > 3 else 1800
    os.environ['CERTIFY_TIMEOUT'] = str(C.TIMEOUT)  # for the spawned workers
    wit, exc = open_items(group)
    progress = os.path.join(HERE, 'tmp_check', 'certify_retry_%s.jsonl' % group)
    done = {}
    if os.path.exists(progress):
        for line in open(progress):
            r = json.loads(line)
            done[json.dumps(r['item'])] = r
    wtodo = [list(w) for w in wit if json.dumps(list(w)) not in done]
    etodo = [list(e) for e in exc if json.dumps(list(e)) not in done]
    print('%s: %d witnesses, %d exclusion diagrams (%d to do)' % (
        group, len(wit), len(exc), len(wtodo) + len(etodo)), flush=True)
    with RobustPool(processes) as pool, open(progress, 'a') as prog:
        for func, ts in ((witness_retry, wtodo), (exclusion_retry, etodo)):
            for r in pool.map(func, ts):
                prog.write(json.dumps(r) + '\n')
                prog.flush()
                done[json.dumps(r['item'])] = r
        dropped = list(pool.dropped)

    rs = [done[json.dumps(list(x))] for x in wit + exc if json.dumps(list(x)) in done]
    ok = {}
    for r in rs:
        if r['kind'] == 'ok':
            key = '%s: %s' % (r['part'], r['info'])
            ok[key] = ok.get(key, 0) + 1
    viol = [r for r in rs if r['kind'] == 'violation']
    unc = [r for r in rs if r['kind'] == 'uncertified']
    lines = ['# Second pass of the certified verification of the %s-index table' % group, '',
             'Script `certify_retry.py` (timeout %d s; see its docstring).' % C.TIMEOUT, '',
             '- open items: %d witnesses, %d exclusion diagrams' % (len(wit), len(exc)),
             '- certified now: %s' % ok,
             '- **contradictions with the table: %d**' % len(viol),
             '- still not certified: %d; crashed: %d' % (len(unc), len(dropped)), '']
    for title, rows in (('Contradictions', viol), ('Still not certified', unc)):
        if rows:
            lines += ['## ' + title, ''] + ['- %s %s: %s' % (r['part'], r['item'][1:], r['info']) for r in rows] + ['']
    if dropped:
        lines += ['## Crashed', ''] + ['- %s' % (t,) for t in dropped] + ['']
    open(os.path.join(HERE, 'results', 'certified_retry_%s.md' % group), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[:8]), flush=True)


if __name__ == '__main__':
    main()
