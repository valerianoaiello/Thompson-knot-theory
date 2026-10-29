"""
Complete check of the indices found by identify.sage, using every diagram of the relevant HOMFLY classes.

usage (from F_index/):   sage -python complete_check.py GROUP [processes]

Why.  run.py stores at most 50 representatives per HOMFLY class and identify.sage only looks at those, so
a knot can hide among the diagrams that were not stored: its index would come out too large (or the knot
not found). Also, a representative that neither get_knotinfo nor SnapPy could identify was treated as
"not this knot". Both problems only matter for a knot K whose HOMFLY class appears at some n before K is
identified (index > lower bound, or K not found): the lower bound itself is exact, because the HOMFLY
polynomial is computed for every diagram.

Steps (all files in tmp_check/, which is not in git; each step is skipped if already done).
  1. targets_<G>.tsv: knot, lower bound, index (or empty), HOMFLY key, from results/<G>_index.csv.
  2. <G>_n<n>/*.all for every n from the smallest lower bound to the last n of results/raw*/: every diagram
     (up to symmetry) of the HOMFLY classes of the targets, one line "key \\t top \\t bottom [\\t PD]", by
     `fknots n -1 8 ... -1 all|vec @keys` (F, vec{F}) or `iota_knots F3|F3vec n s 8 ... -1 @keys` (F_3,
     vec{F}_3, with the PD code). Run it with `caffeinate -i`: n = 13 for F takes ~30 min.
  3. the comparison below.

Method.  For every target K and every n from its lower bound to its index (or to the last n), every
diagram of the class of K at n is compared with K: the diagram is simplified with spherogram, the
hyperbolic volume of its complement is compared with that of K, and if they agree SnapPy looks for an
isometry (by Gordon-Luecke the complement determines the knot up to mirror image). When SnapPy finds
no hyperbolic structure, get_knotinfo (<= 13 crossings) or SnapPy's census decides; if nothing decides,
the diagram is counted as undecided. A target is done as soon as it is found at some n; the classes
of the larger n are then skipped. Progress is appended to tmp_check/progress_<G>.jsonl, so an
interrupted run continues where it stopped.

Output.  results/complete_check_<G>.csv and .md: old and new index of every target, number of diagrams
compared and of undecided ones, a witness for every new value.
"""
import csv
import glob
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CHUNK = 2000          # diagrams per task
VOLUME_EPS = 1e-7

_TARGETS = {}         # per process: knot -> (hyperbolic, volume, exterior)


def _geometric(E, tries=5):
    for _ in range(tries):
        if E.solution_type() == 'all tetrahedra positively oriented':
            return True
        E.randomize()
    return False


def _target(knot):
    if knot not in _TARGETS:
        import snappy  # noqa: F401
        import spherogram
        from sage.all import KnotInfo
        pd = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + knot).link().pd_code()]
        E = spherogram.Link([[x - 1 for x in c] for c in pd]).exterior()
        hyp = _geometric(E)
        _TARGETS[knot] = (hyp, float(E.volume()) if hyp else 0.0, E)
    return _TARGETS[knot]


def _compare(top, bottom, pd, knots):
    """{knot: 'yes' | 'no' | 'undecided'} for the diagram (top, bottom) of F, or with the given PD code."""
    import snappy  # noqa: F401
    import spherogram
    import ftrees as F
    from identify_lib import knotinfo_name, snappy_name
    if pd is None:
        pd = F.pd_code(F.from_leaf_words(top.split(',')), F.from_leaf_words(bottom.split(',')))
    S = spherogram.Link([[x - 1 for x in c] for c in pd])
    S.simplify('global')
    E = S.exterior()
    geo = _geometric(E)
    vol = float(E.volume()) if geo else None
    name = None  # exact name, computed only if needed
    res = {}
    for k in knots:
        hyp, vk, Ek = _target(k)
        if geo and hyp:
            if abs(vol - vk) > VOLUME_EPS:
                res[k] = 'no'
                continue
            try:
                res[k] = 'yes' if E.is_isometric_to(Ek) else 'no'
            except Exception:
                res[k] = 'undecided'
        elif geo:
            res[k] = 'no'  # hyperbolic diagram, non-hyperbolic target
        else:
            if name is None:
                name = (knotinfo_name(S) if len(S.crossings) <= 13 else None) or snappy_name(S) or ''
            if name in ('', 'non-hyperbolic'):
                res[k] = 'undecided'
            else:
                res[k] = 'yes' if name == k else 'no'
    return res


def check_chunk(task):
    """task = [n, path, offset, count, knots]: compares the diagrams of the chunk with the knots."""
    n, path, offset, count, knots = task
    found, undecided, compared = {}, {}, 0
    with open(path) as f:
        f.seek(offset)
        for _ in range(count):
            line = f.readline()
            if not line:
                break
            fields = line.rstrip('\n').split('\t')
            top, bottom = fields[1], fields[2]
            pd = json.loads(fields[3]) if len(fields) > 3 else None
            live = [k for k in knots if k not in found]
            if not live:
                break
            compared += 1
            try:
                res = _compare(top, bottom, pd, live)
            except Exception as e:
                res = {k: 'undecided' for k in live}
                top = top + ' (%s)' % str(e)[:60]
            for k, r in res.items():
                if r == 'yes':
                    found[k] = (top, bottom)
                elif r == 'undecided':
                    undecided.setdefault(k, []).append((top, bottom))
    return {'n': n, 'path': path, 'offset': offset, 'compared': compared, 'found': found,
            'undecided': {k: (len(v), v[:3]) for k, v in undecided.items()}}


def split_classes(d, keys):
    """Splits d/*.all by HOMFLY key into d/classes/<i>.tsv; returns {key: [(path, offset, count)]}."""
    index_file = os.path.join(d, 'classes', 'index.json')
    if os.path.exists(index_file):
        return json.load(open(index_file))
    os.makedirs(os.path.join(d, 'classes'), exist_ok=True)
    ids = {k: i for i, k in enumerate(sorted(keys))}
    paths = {k: os.path.join(d, 'classes', '%d.tsv' % i) for k, i in ids.items()}
    for p in paths.values():
        open(p, 'w').close()
    buf, size = {}, 0

    def flush():
        for k, lines in buf.items():
            with open(paths[k], 'a') as f:
                f.writelines(lines)
        buf.clear()

    for name in sorted(glob.glob(os.path.join(d, '*.all'))):
        with open(name) as f:
            for line in f:
                k = line.split('\t', 1)[0]
                buf.setdefault(k, []).append(line)
                size += 1
                if size >= 2000000:
                    flush()
                    size = 0
    flush()
    index = {}
    for k, p in paths.items():
        chunks, offset, count = [], 0, 0
        with open(p, 'rb') as f:
            for line in f:
                if count == 0:
                    start = offset
                count += 1
                offset += len(line)
                if count == CHUNK:
                    chunks.append((p, start, count))
                    count = 0
        if count:
            chunks.append((p, start, count))
        if chunks:
            index[k] = chunks
    json.dump(index, open(index_file, 'w'))
    return index


RAW = {'F': 'raw', 'Fvec': 'raw_Fvec', 'F3': 'raw_F3', 'F3vec': 'raw_F3vec'}


def write_targets(group, path):
    from sage.all import KnotInfo
    from oriented_index import homfly_key
    col = group + '_index'
    with open(path + '.part', 'w') as out:
        for r in csv.DictReader(open(os.path.join(HERE, 'results', '%s_index.csv' % group))):
            lb, hi = int(r['lower_bound']), r[col]
            if r['status'].startswith('HOMFLY') or (hi and int(hi) > lb):
                pd = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + r['knot']).link().pd_code()]
                out.write('%s\t%d\t%s\t%s\n' % (r['knot'], lb, hi, homfly_key(pd)))
    os.replace(path + '.part', path)


def enumerate_n(group, n, d, keys_file, processes):
    import subprocess
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, 's.tsv')
    if group in ('F', 'Fvec'):
        cmds = [[os.path.join(HERE, 'bin', 'fknots'), str(n), '-1', str(processes), out, '-1',
                 'vec' if group == 'Fvec' else 'all', '@' + keys_file]]
    else:
        cmds = [[os.path.join(HERE, 'bin', 'iota_knots'), group, str(n), str(s), str(processes),
                 '%s.%d' % (out, s), '-1', '@' + keys_file] for s in range(processes)]
    procs = [subprocess.Popen(c) for c in cmds]
    if any(p.wait() for p in procs):
        sys.exit('enumeration failed at n = %d' % n)
    open(os.path.join(d, 'done'), 'w').close()


def main():
    group = sys.argv[1]
    processes = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    from identify_lib import RobustPool
    tdir = os.path.join(HERE, 'tmp_check')
    os.makedirs(tdir, exist_ok=True)
    tfile = os.path.join(tdir, 'targets_%s.tsv' % group)
    if not os.path.exists(tfile):
        write_targets(group, tfile)
    targets = {}  # knot -> (lower bound, old index or None, key)
    for line in open(tfile):
        knot, lb, hi, key = line.rstrip('\n').split('\t')
        targets[knot] = (int(lb), int(hi) if hi else None, key)
    keys_file = os.path.join(tdir, 'keys_%s.txt' % group)
    with open(keys_file, 'w') as f:
        f.writelines(k + '\n' for k in sorted({t[2] for t in targets.values()}))
    nmax = max(int(m) for m in re.findall(r'n(\d+)\.tsv', ' '.join(os.listdir(os.path.join(HERE, 'results', RAW[group])))))
    ns = list(range(min(t[0] for t in targets.values()), nmax + 1))
    if group in ('Fvec', 'F3vec'):
        ns = [n for n in ns if n % 2]  # no knots for even n (results/parity_theorem.md)
    for n in ns:
        d = os.path.join(tdir, '%s_n%d' % (group, n))
        if not os.path.exists(os.path.join(d, 'done')):
            t1 = time.time()
            enumerate_n(group, n, d, keys_file, processes)
            print('n = %d: all diagrams of the target classes written (%.0f s)' % (n, time.time() - t1), flush=True)
    keys = {t[2] for t in targets.values()}
    t0 = time.time()
    index = {n: split_classes(os.path.join(tdir, '%s_n%d' % (group, n)), keys) for n in ns}
    print('classes split by HOMFLY (%.0f s)' % (time.time() - t0), flush=True)

    best = {k: t[1] for k, t in targets.items()}       # current index (None = not found)
    witness = {}
    compared = {k: 0 for k in targets}
    undecided = {k: {} for k in targets}               # knot -> {n: (count, examples)}
    progress_file = os.path.join(tdir, 'progress_%s.jsonl' % group)
    done = set()

    def record(r):
        done.add((r['n'], r['path'], r['offset']))
        for k in r['knots']:
            compared[k] += r['compared']
        for k, (top, bottom) in r['found'].items():
            if best[k] is None or r['n'] < best[k] or (r['n'] == best[k] and k not in witness):
                best[k] = r['n']
                witness[k] = (top, bottom)
        for k, (cnt, ex) in r['undecided'].items():
            c = undecided[k].setdefault(r['n'], [0, []])
            c[0] += cnt
            c[1] = (c[1] + ex)[:3]

    if os.path.exists(progress_file):
        for line in open(progress_file):
            record(json.loads(line))
        print('resumed: %d chunks already done' % len(done), flush=True)

    tasks = []
    by_key = {}
    for k, t in targets.items():
        by_key.setdefault(t[2], []).append(k)
    for n in ns:
        for key, chunks in index[n].items():
            knots = sorted(k for k in by_key.get(key, []) if targets[k][0] <= n)
            for path, offset, count in chunks:
                if knots and (n, path, offset) not in done:
                    tasks.append([n, path, offset, count, knots])
    print('%d chunks to compare (%d diagrams at most)' % (len(tasks), sum(t[3] for t in tasks)), flush=True)

    def skip(t):
        # only the targets not yet found at a smaller or equal n
        t[4] = [k for k in t[4] if best[k] is None or t[0] < best[k]]
        return not t[4]

    with open(progress_file, 'a') as pf, RobustPool(processes) as pool:
        by_id = {(t[0], t[1], t[2]): t for t in tasks}
        ndone = 0
        for r in pool.map(check_chunk, tasks, skip=skip):
            r['knots'] = by_id[(r['n'], r['path'], r['offset'])][4]
            record(r)
            pf.write(json.dumps(r) + '\n')
            pf.flush()
            ndone += 1
            if r['found'] or ndone % 200 == 0:
                print('  %d chunks (n = %d), %.0f s%s' % (ndone, r['n'], time.time() - t0,
                      ''.join('; %s at n = %d' % (k, r['n']) for k in r['found'])), flush=True)
        dropped = list(pool.dropped)
    for t in dropped:
        for k in t[4]:
            undecided[k].setdefault(t[0], [0, []])[0] += t[3]

    rows = []
    for k, (lb, old, key) in targets.items():
        new = best[k]
        unc = sum(c for n, (c, _) in undecided[k].items() if new is None or n < new)
        if new is None:
            verdict = 'not found up to n = %d' % nmax
        elif old is None:
            verdict = 'FOUND'
        elif new < old:
            verdict = 'LOWERED'
        else:
            verdict = 'confirmed'
        if unc:
            verdict += ' (%d undecided diagrams before)' % unc
        top, bottom = witness.get(k, ('', ''))
        rows.append({'knot': k, 'lower_bound': lb, 'old_index': old or '', 'new_index': new or '',
                     'verdict': verdict, 'diagrams_compared': compared[k], 'undecided_before_index': unc,
                     'undecided_examples': json.dumps({n: ex for n, (c, ex) in undecided[k].items() if ex}),
                     'top_tree': top, 'bottom_tree': bottom})

    def ckey(r):
        c, rest = r['knot'].split('_')
        return (int(c.rstrip('an')), rest[0] if not rest[0].isdigit() else '', int(rest.lstrip('an')))

    rows.sort(key=ckey)
    out = os.path.join(HERE, 'results', 'complete_check_%s' % group)
    with open(out + '.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(out + '.md', 'w') as f:
        f.write('# Complete check of the %s-index (all diagrams of the HOMFLY classes)\n\n' % group)
        f.write('Knots whose HOMFLY class appears before they are identified (or that are not identified), with '
                'tree diagrams up to n = %d. Every diagram of their class, from the lower bound to the index, was '
                'compared with the knot (hyperbolic volume, then SnapPy isometry; get_knotinfo / SnapPy census '
                'without a hyperbolic structure). %d diagram chunks crashed SnapPy and count as undecided.\n\n'
                % (nmax, len(dropped)))
        f.write('| knot | lower bound | old index | new index | verdict | diagrams compared | top tree | bottom tree |\n')
        f.write('|---|---|---|---|---|---|---|---|\n')
        for r in rows:
            f.write('| %s | %s | %s | %s | %s | %s | %s | %s |\n' % (
                r['knot'], r['lower_bound'], r['old_index'], r['new_index'], r['verdict'], r['diagrams_compared'],
                '`%s`' % r['top_tree'] if r['top_tree'] else '', '`%s`' % r['bottom_tree'] if r['bottom_tree'] else ''))
    changed = [r for r in rows if not r['verdict'].startswith(('confirmed', 'not found'))]
    print('done in %.0f s: %d targets, changed: %s' % (time.time() - t0, len(rows),
          ', '.join('%s %s->%s' % (r['knot'], r['old_index'] or '?', r['new_index']) for r in changed) or '-'))


if __name__ == '__main__':
    main()
