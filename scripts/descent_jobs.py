"""
Builds the job files of descent_search.py for the open cases of the tables (tmp_check/descent/jobs_<name>.json):
  F3       knots not found in F_3 (n <= 9) with <= 12 crossings: start from their vec{F}_3 witness (vec{F}_3 is in
           F_3), one step down;
  F        knots not found in F (n <= 13) with <= 11 crossings: start from their vec{F} witness, down to n = 14;
  F3vec    knots not found in vec{F}_3 (n <= 11) with <= 12 crossings and a vec{F} witness: start from iota of it,
           down to n = 13;
  rev3     the knots of results/reverse_bound_F3vec.csv with '13-15': start from the move with four new vertices
           (n = 15, it realizes the other orientation), one step down, looking for the other orientation;
  rev      the same in vec{F} (results/reverse_bound_Fvec.csv, '19-21'): from n = 21 to n = 19.
Every starting diagram built by a move is checked with SnapPy before it is used.
With --more, jobs for the cases still open after a first round, starting from ALL the stored representatives of
the knot (results/raw_<G>/n<n>.tsv, up to 50 per HOMFLY class, those that SnapPy identifies with the knot) and
from the certified diagrams of the first round (results/descent_certified.csv): jobs_more.json.
usage (from F_index/): sage -python scripts/descent_jobs.py [--more | --f3-13 | --f3-13-more]
--f3-13: F_3, the knots with 13 crossings not found with n <= 9, from their vec{F}_3 witness (jobs_F3c13.json).
--f3-13-more: second round for those still open, from all their stored vec{F}_3 representatives (jobs_F3c13more.json).
  Add --max-starts N to leave out the witness (already used by --f3-13) and keep at most N starts per knot
  (N = 5 in the round of 2026-11-05; without it the round would take ~47 h on the Mac).
  --name NAME writes jobs_NAME.json (default F3c13more; it overwrites an existing file); --exclude-jobs F1,F2 leaves
  out the witness and the starts already used in those job files (third round: --name F3c13third
  --exclude-jobs tmp_check/descent/jobs_F3c13more.json).
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root (the scripts are in scripts/)
sys.path.insert(0, os.path.join(HERE, 'scripts'))
csv.field_size_limit(10**9)

REVERSE = {'K': ['reverse', 'mirror'], 'Kr': ['same', 'mirror reverse']}  # the other orientation (inverse rule)


def last_leaf(ws, sub):
    """Leaf words with the last leaf replaced by the subtree with leaf words `sub`."""
    last = max(ws)
    return [w for w in ws if w != last] + [last + s for s in sub]


def move4_ternary(top, bottom):
    t, b = top.split(','), bottom.split(',')
    tp = ['00', '01'] + ['02' + w for w in last_leaf(t, '012')] + ['1', '20', '21', '22']
    tm = ['0', '1'] + ['2' + w for w in last_leaf(b, ['00', '01', '020', '021', '022', '1', '2'])]
    return ','.join(sorted(tp)), ','.join(sorted(tm))


def move4_binary(top, bottom):
    t, b = top.split(','), bottom.split(',')
    tp = ['00'] + ['01' + w for w in last_leaf(t, '01')] + ['10', '11']
    tm = ['0'] + ['1' + w for w in last_leaf(b, ['00', '010', '011', '1'])]
    return ','.join(sorted(tp)), ','.join(sorted(tm))


RAW = {'F': 'raw', 'F3': 'raw_F3', 'Fvec': 'raw_Fvec', 'F3vec': 'raw_F3vec'}


def stored_starts(group, n, knot):
    """The stored representatives of size n in the HOMFLY class of the knot that SnapPy identifies with it."""
    import snappy  # noqa: F401
    import spherogram
    from sage.all import KnotInfo
    from oriented_index import homfly_key
    import complete_check as C
    import descent_search as D
    ref = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + knot).link().pd_code()]
    key = homfly_key(ref).strip()
    Ek = spherogram.Link([[x - 1 for x in c] for c in ref]).exterior()
    out = []
    for line in open(os.path.join(HERE, 'results', RAW[group], 'n%d.tsv' % n)):
        f = line.rstrip('\n').split('\t')
        if line.startswith('#') or f[0].strip() != key:
            continue
        for rep in f[3].split(';'):
            parts = rep.split('|')
            if len(parts) < 2 or not parts[0]:
                continue
            tp, tm = D.tree(group, parts[0]), D.tree(group, parts[1])
            pd = D.pd_code(group, tp, tm)
            if pd is None:
                continue
            E = spherogram.Link([[x - 1 for x in c] for c in pd]).exterior()
            try:
                if C._geometric(E) and E.is_isometric_to(Ek):
                    out.append(parts[0] + ' | ' + parts[1])
            except Exception:
                pass
    return out


def iota_start(d):
    import ftrees as F
    import oriented as O
    t, b = [F.from_leaf_words(x.strip().split(',')) for x in d.split('|')]
    return ','.join(O.ternary_words(O.iota(t))) + ' | ' + ','.join(O.ternary_words(O.iota(b)))


def more():
    """Jobs for the open cases after the first round (see the docstring)."""
    T = {G: {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', '%s_index.csv' % G)))}
         for G in ('F', 'F3', 'Fvec', 'F3vec')}
    cert = list(csv.DictReader(open(os.path.join(HERE, 'results', 'descent_certified.csv'))))

    def certified(G, k):
        """Certified diagrams of the knot of the smallest size found, and that size."""
        rows = [r for r in cert if r['group'] == G and r['knot'] == k and r['certified'] == 'yes' and r['relation'] == 'isometric']
        if not rows:
            return [], None
        m = min(int(r['n']) for r in rows)
        return [r['diagram'] for r in rows if int(r['n']) == m], m

    jobs = []
    for k, r in T['F3'].items():
        if not r['F3_index'] and int(r['crossing_number']) <= 12 and T['F3vec'][k]['F3vec_index'] == '11':
            starts = stored_starts('F3vec', 11, k)
            if starts:
                jobs.append({'name': 'F3more', 'group': 'F3', 'knot': k, 'starts': starts, 'steps': 1})
    for k, r in T['F'].items():
        if not r['F_index'] and int(r['crossing_number']) <= 11:
            starts, m = certified('F', k)
            if not starts and T['Fvec'][k]['Fvec_index']:
                m = int(T['Fvec'][k]['Fvec_index'])
                starts = stored_starts('Fvec', m, k)
            if starts:
                jobs.append({'name': 'Fmore', 'group': 'F', 'knot': k, 'starts': starts, 'steps': m - 14})
    for k, r in T['F3vec'].items():
        if not r['F3vec_index'] and int(r['crossing_number']) <= 12:
            starts, m = certified('F3vec', k)
            if not starts and T['Fvec'][k]['Fvec_index']:
                m = int(T['Fvec'][k]['Fvec_index'])
                starts = [iota_start(d) for d in stored_starts('Fvec', m, k)]
            if starts:
                jobs.append({'name': 'F3vecmore', 'group': 'F3vec', 'knot': k, 'starts': starts, 'steps': (m - 13) // 2})
    json.dump(jobs, open(os.path.join(HERE, 'tmp_check', 'descent', 'jobs_more.json'), 'w'), indent=1)
    for j in jobs:
        print(j['name'], j['knot'], len(j['starts']), 'starts,', j['steps'], 'steps')


def thirteen():
    """F_3, knots with 13 crossings not found with n <= 9 and with a vec{F}_3 witness: one step down from it."""
    T = {G: {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', '%s_index.csv' % G)))}
         for G in ('F3', 'F3vec')}
    jobs = []
    for k, r in T['F3'].items():
        w = T['F3vec'][k]
        if not r['F3_index'] and int(r['crossing_number']) == 13 and w['F3vec_index'] == '11' and int(r['lower_bound']) <= 10:
            jobs.append({'name': 'F3c13', 'group': 'F3', 'knot': k, 'steps': 1,
                         'starts': [w['top_tree'] + ' | ' + w['bottom_tree']]})
    json.dump(jobs, open(os.path.join(HERE, 'tmp_check', 'descent', 'jobs_F3c13.json'), 'w'), indent=1)
    print(len(jobs), 'jobs')


def _check_reps(task):
    """task = [group, knot, reps]: the representatives that SnapPy identifies with the knot."""
    import snappy  # noqa: F401
    import spherogram
    from sage.all import KnotInfo
    import complete_check as C
    import descent_search as D
    group, knot, reps = task
    ref = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + knot).link().pd_code()]
    Ek = spherogram.Link([[x - 1 for x in c] for c in ref]).exterior()
    out = []
    for top, bottom in reps:
        pd = D.pd_code(group, D.tree(group, top), D.tree(group, bottom))
        if pd is None:
            continue
        E = spherogram.Link([[x - 1 for x in c] for c in pd]).exterior()
        try:
            if C._geometric(E) and E.is_isometric_to(Ek):
                out.append(top + ' | ' + bottom)
        except Exception:
            pass
    return knot, out


def thirteen_more(max_starts=None, name='F3c13more', exclude=()):
    """Second round for the F_3 knots with 13 crossings still open: all the stored vec{F}_3 representatives of
    size 11 that are the knot as starts (the representatives file is read once, the checks run in parallel).
    With max_starts: the vec{F}_3 witness (the start of the first round) is left out and at most max_starts
    starts are kept per knot, the first ones in the order of the representatives file; knots left without
    starts are dropped. The round of 2026-11-05 used max_starts = 5 (1032 jobs, 4531 starts).
    exclude: job files of earlier rounds; their starts and the witness are left out (third round of 2026-11-07:
    name 'F3c13third', exclude the second round). The jobs are written to tmp_check/descent/jobs_<name>.json."""
    used = set()
    for f in exclude:
        used.update((j['knot'], d) for j in json.load(open(f)) for d in j['starts'])
    from oriented_index import homfly_key
    from sage.all import KnotInfo
    from identify_lib import RobustPool
    T = {G: {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', '%s_index.csv' % G)))}
         for G in ('F3', 'F3vec')}
    knots = [k for k, r in T['F3'].items() if not r['F3_index'] and int(r['crossing_number']) == 13
             and T['F3vec'][k]['F3vec_index'] == '11' and int(r['lower_bound']) <= 10]
    keys = {}
    for k in knots:
        ref = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + k).link().pd_code()]
        keys.setdefault(homfly_key(ref).strip(), []).append(k)
    reps = {}
    for line in open(os.path.join(HERE, 'results', RAW['F3vec'], 'n11.tsv')):
        if line.startswith('#'):
            continue
        f = line.rstrip('\n').split('\t')
        if f[0].strip() in keys:
            reps[f[0].strip()] = [tuple(r.split('|')[:2]) for r in f[3].split(';') if r.split('|')[0]]
    tasks = [['F3vec', k, reps.get(key, [])] for key, ks in keys.items() for k in ks]
    jobs = []
    with RobustPool(os.cpu_count()) as pool:
        for k, starts in pool.map(_check_reps, tasks):
            if max_starts is not None or exclude:
                w = T['F3vec'][k]
                starts = [d for d in starts if d != w['top_tree'] + ' | ' + w['bottom_tree'] and (k, d) not in used]
                starts = starts[:max_starts]
            if starts:
                jobs.append({'name': name, 'group': 'F3', 'knot': k, 'starts': starts, 'steps': 1})
    jobs.sort(key=lambda j: j['knot'])
    json.dump(jobs, open(os.path.join(HERE, 'tmp_check', 'descent', 'jobs_%s.json' % name), 'w'), indent=1)
    print(len(knots), 'knots,', len(jobs), 'jobs,', sum(len(j['starts']) for j in jobs), 'starts')


def main():
    if '--more' in sys.argv:
        return more()
    if '--f3-13-more' in sys.argv:
        m = sys.argv.index('--max-starts') + 1 if '--max-starts' in sys.argv else None
        a = sys.argv
        return thirteen_more(int(a[m]) if m else None, a[a.index('--name') + 1] if '--name' in a else 'F3c13more',
                             a[a.index('--exclude-jobs') + 1].split(',') if '--exclude-jobs' in a else ())
    if '--f3-13' in sys.argv:
        return thirteen()
    from sage.all import KnotInfo
    import ftrees as F
    import oriented as O
    T = {G: {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', '%s_index.csv' % G)))}
         for G in ('F', 'F3', 'Fvec', 'F3vec')}
    d = os.path.join(HERE, 'tmp_check', 'descent')
    os.makedirs(d, exist_ok=True)

    def witness(G, k):
        return T[G][k]['top_tree'] + ' | ' + T[G][k]['bottom_tree']

    def open_cases(G, maxc):
        return [k for k, r in T[G].items() if not r[G + '_index'] and int(r['crossing_number']) <= maxc]

    def ref(k):
        return [list(map(int, c)) for c in getattr(KnotInfo, 'K' + k).link().pd_code()]

    jobs = {'F3': [], 'F': [], 'F3vec': [], 'rev3': [], 'rev': []}
    for k in open_cases('F3', 12):
        if T['F3vec'][k]['F3vec_index']:
            jobs['F3'].append({'name': 'F3', 'group': 'F3', 'knot': k, 'starts': [witness('F3vec', k)], 'steps': 1})
    for k in open_cases('F', 11):
        if T['Fvec'][k]['Fvec_index']:
            n = int(T['Fvec'][k]['Fvec_index'])
            jobs['F'].append({'name': 'F', 'group': 'F', 'knot': k, 'starts': [witness('Fvec', k)], 'steps': n - 14})
    for k in open_cases('F3vec', 12):
        if T['Fvec'][k]['Fvec_index']:
            n = int(T['Fvec'][k]['Fvec_index'])
            t, b = [F.from_leaf_words(x.strip().split(',')) for x in witness('Fvec', k).split('|')]
            start = ','.join(O.ternary_words(O.iota(t))) + ' | ' + ','.join(O.ternary_words(O.iota(b)))
            jobs['F3vec'].append({'name': 'F3vec', 'group': 'F3vec', 'knot': k, 'starts': [start],
                                  'steps': (n - 13) // 2})
    ori = {G: {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', 'oriented_index_%s.csv' % G)))}
           for G in ('Fvec', 'F3vec')}
    for G, name, move, tree, pd in (('F3vec', 'rev3', move4_ternary, O.ternary_from_words, O.oriented_pd_code3),
                                    ('Fvec', 'rev', move4_binary, F.from_leaf_words, O.oriented_pd_code)):
        for r in csv.DictReader(open(os.path.join(HERE, 'results', 'reverse_bound_%s.csv' % G))):
            if '-' not in r['index_other']:
                continue
            k, want = r['knot'], r['realized']
            t, b = [x.strip() for x in ori[G][k]['witness_' + want].split('|')]
            mt, mb = move(t, b)
            rel = O.relation_to(pd(tree(mt.split(',')), tree(mb.split(','))), ref(k))
            if not rel & set(REVERSE[want]):
                print('move check FAILED', G, k, want, sorted(rel))
                continue
            jobs[name].append({'name': name, 'group': G, 'knot': k, 'starts': [mt + ' | ' + mb], 'steps': 1,
                               'want': REVERSE[want]})
    for name, js in jobs.items():
        json.dump(js, open(os.path.join(d, 'jobs_%s.json' % name), 'w'), indent=1)
        print(name, len(js), 'jobs')


if __name__ == '__main__':
    main()
