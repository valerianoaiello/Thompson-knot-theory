"""
Second pass on the undecided diagrams of complete_check.py: diagrams of a target's HOMFLY class on which
SnapPy found no hyperbolic structure (5 tries) and no name.

usage (from F_index/):   sage -python resolve_undecided.py GROUP [processes]

For every knot of results/complete_check_<G>.csv with undecided diagrams below its index (or below n_max + 1
when not found), every such diagram is examined again:
  1. knot Floer homology (spherogram, up to mirror image): if it differs from the target's, the diagram
     is not the target;
  2. otherwise 100 randomizations looking for a hyperbolic structure; if found, volume + isometry;
  3. otherwise equal isomorphism signatures of random retriangulations of the two complements: the diagram
     is the target (exact);
  4. otherwise an essential torus found by Regina (incompressible and not boundary parallel, as in
     certify_indices.py; at most 120 s, in a separate process): the knot is a satellite, so it is not the target, provided the
     target is hyperbolic (some targets are satellites, e.g. 13n_4587).
Steps 1, 3 and 4 are exact. (An earlier version used SnapPy's splitting_surfaces in step 4, whose tori need
not be essential: it excluded a diagram of 13n_4587, vec{F}_3, n = 11.) A diagram passing all of them stays
undecided, and the certified verification (certify_indices.py) has to decide it. The csv is updated (undecided_before_index = what is left),
and results/complete_check_<G>.md gets a note. Then run apply_complete_check.py.
"""
import csv
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import complete_check as C  # noqa: E402
import certify_indices as CI  # noqa: E402
from identify_lib import with_timeout  # noqa: E402

_HFK = {}
STEP = 100            # diagrams per task


def hfk(L):
    r = L.knot_floer_homology()['ranks']
    return frozenset(r.items()), frozenset(((-a, -m), v) for (a, m), v in r.items())


def _target_hfk(knot):
    if knot not in _HFK:
        import spherogram
        from sage.all import KnotInfo
        pd = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + knot).link().pd_code()]
        _HFK[knot] = hfk(spherogram.Link([[x - 1 for x in c] for c in pd]))[0]
    return _HFK[knot]


def examine(task):
    """task = [knot, path, offset, start]: counts of the outcomes on the undecided diagrams among lines
    start .. start + STEP - 1 of the chunk."""
    import spherogram
    knot, path, offset, start = task
    hyp, vk, Ek = C._target(knot)
    out, left = Counter(), []
    with open(path) as f:
        f.seek(offset)
        for i in range(min(C.CHUNK, start + STEP)):
            line = f.readline()
            if not line:
                break
            if i < start:
                continue
            fl = line.rstrip('\n').split('\t')
            pd = json.loads(fl[3]) if len(fl) > 3 else None
            if C._compare(fl[1], fl[2], pd, [knot])[knot] != 'undecided':
                continue
            if pd is None:
                import ftrees as F
                pd = F.pd_code(F.from_leaf_words(fl[1].split(',')), F.from_leaf_words(fl[2].split(',')))
            L = spherogram.Link([[x - 1 for x in c] for c in pd])
            L.simplify('global')
            if _target_hfk(knot) not in hfk(L):
                out['knot Floer homology differs'] += 1
                continue
            E = L.exterior()
            if C._geometric(E, 100):
                same = abs(float(E.volume()) - vk) < C.VOLUME_EPS and E.is_isometric_to(Ek)
                out['hyperbolic, the target' if same else 'hyperbolic, not the target'] += 1
                if same:
                    left.append((fl[1], fl[2], 'IS THE TARGET'))
                continue
            if C.same_as_target(E, knot, tries=2000):
                # exact: the complements are homeomorphic (Gordon-Luecke); needed above all for targets that
                # are satellites, whose diagrams also contain essential tori
                left.append((fl[1], fl[2], 'IS THE TARGET'))
                out['the target (equal isomorphism signatures)'] += 1
                continue
            if hyp and essential_torus_killable(E, timeout=120):
                out['satellite (essential torus, Regina)'] += 1
                continue
            out['still undecided'] += 1
            left.append((fl[1], fl[2], 'undecided'))
    return {'task': task, 'knot': knot, 'counts': dict(out), 'left': left}


def essential_torus_killable(E, timeout=120):
    """CI.essential_torus(E) in a separate process, killed after `timeout` seconds (Regina's normal surface
    enumeration can take very long on large triangulations and is not interrupted by an alarm). True or False,
    None on a timeout or an error."""
    import subprocess
    code = ('import sys; sys.path.insert(0, %r); import snappy, certify_indices as C; '
            'print(C.essential_torus(snappy.Manifold(sys.argv[1])))' % HERE)
    try:
        out = subprocess.run([sys.executable, '-c', code, E.triangulation_isosig(decorated=False)],
                             capture_output=True, text=True, timeout=timeout).stdout.strip()
    except subprocess.TimeoutExpired:
        return None
    return {'True': True, 'False': False}.get(out.splitlines()[-1] if out else '')


def main():
    group = sys.argv[1]
    processes = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    from identify_lib import RobustPool
    csv_path = os.path.join(HERE, 'results', 'complete_check_%s.csv' % group)
    rows = list(csv.DictReader(open(csv_path)))
    fields = list(rows[0].keys())
    todo = {}
    for r in rows:
        if int(r['undecided_before_index'] or 0):
            todo[r['knot']] = int(r['new_index']) if r['new_index'] else 10 ** 9
    tasks = []
    for line in open(os.path.join(HERE, 'tmp_check', 'progress_%s.jsonl' % group)):
        p = json.loads(line)
        for k in p.get('undecided', {}):
            if k in todo and p['n'] < todo[k]:
                tasks += [[k, p['path'], p['offset'], s] for s in range(0, C.CHUNK, STEP)]
    print('%d chunks to examine for %s' % (len(tasks), ', '.join(sorted(todo))), flush=True)
    counts = {k: Counter() for k in todo}
    left = {k: [] for k in todo}
    progress = os.path.join(HERE, 'tmp_check', 'resolve_%s.jsonl' % group)   # resumed after a restart
    done = set()
    if os.path.exists(progress):
        for line in open(progress):
            res = json.loads(line)
            done.add(tuple(res['task']))
            counts[res['knot']].update(res['counts'])
            left[res['knot']] += [tuple(x) for x in res['left']]
    tasks = [t for t in tasks if tuple(t) not in done]
    print('%d chunks already examined, %d to go' % (len(done), len(tasks)), flush=True)
    with RobustPool(processes) as pool, open(progress, 'a') as prog:
        for i, res in enumerate(pool.map(examine, tasks), 1):
            counts[res['knot']].update(res['counts'])
            left[res['knot']] += res['left']
            prog.write(json.dumps(res) + '\n')
            prog.flush()
            if i % 20 == 0:
                print('  %d / %d chunks' % (i, len(tasks)), flush=True)
        dropped = list(pool.dropped)
    for t in dropped:
        counts[t[0]]['chunk crashed SnapPy (diagrams stay undecided)'] += 1
        left[t[0]].append(('chunk %s:%d' % (t[1], t[2]), '', 'crashed'))
    notes = ['', '## Second pass on the undecided diagrams (resolve_undecided.py)', '']
    for r in rows:
        k = r['knot']
        if k not in todo:
            continue
        found = [x for x in left[k] if x[2] == 'IS THE TARGET']
        rest = sum(1 for x in left[k] if x[2] != 'IS THE TARGET')
        notes.append('- %s: %s; %d left undecided%s' % (
            k, ', '.join('%s %d' % kv for kv in sorted(counts[k].items())), rest,
            '; **a diagram with fewer leaves is the knot**: %s | %s' % found[0][:2] if found else ''))
        if found:
            print('WARNING: %s is realized by %s | %s (rerun the check for it)' % (k, found[0][0], found[0][1]))
        else:
            r['undecided_before_index'] = str(rest)
            if not rest:
                r['verdict'] = r['verdict'].split(' (')[0] + ' (undecided diagrams resolved, see the note)'
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    md = os.path.join(HERE, 'results', 'complete_check_%s.md' % group)
    open(md, 'a').write('\n'.join(notes) + '\n')
    print('\n'.join(notes))


if __name__ == '__main__':
    main()
