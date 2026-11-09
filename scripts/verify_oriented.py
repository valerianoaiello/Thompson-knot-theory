"""
Certified verification of the oriented results (results/oriented_index_<G>.csv) for the knots K with
index(K) != index(K^r).

usage (from F_index/):   sage -python scripts/verify_oriented.py GROUP [processes]      (GROUP = Fvec or F3vec)

For such a knot, say index(K) = a < index(K^r) = b (b possibly > n_max), the claims are:
  (i)  a witness of K with a leaves (and of K^r with b leaves, when b <= n_max) realizes that orientation;
  (ii) no diagram with n < b realizes K^r, i.e. no diagram of the HOMFLY class of K with n < b is K^r or K^m
       (the enumeration keeps one of g, g^-1, and g^-1 realizes K^m when g realizes K^r).
(ii) is checked on every diagram of the class (all-diagram files of oriented_scan.py) with exact or certified
methods only:
  1. knot Floer homology (exact; spherogram) different from that of K up to mirror image -> not K;
  2. otherwise verified hyperbolic volume (interval arithmetic, SnapPy verified=True) disjoint from that of K
     -> not K;
  3. otherwise verified canonical retriangulation of both complements (SnapPy verified=True) and all their
     combinatorial isomorphisms: their action on (meridian, longitude) gives exactly which of K, K^r, K^m,
     K^mr the diagram is.
A diagram on which none of these succeeds is reported as not certified.
Progress: tmp_check/verify_<G>.jsonl (resumed). Output: results/oriented_verified_<G>.md.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root (the scripts are in scripts/)
sys.path.insert(0, os.path.join(HERE, 'scripts'))
NAME = {(1, 1): 'K', (-1, -1): 'Kr', (-1, 1): 'Km', (1, -1): 'Kmr'}  # (meridian sign, longitude sign)
_REF = {}


def oriented_pd(group, top, bottom):
    import oriented as O
    if group == 'Fvec':
        import ftrees as F
        return O.oriented_pd_code(F.from_leaf_words(top.split(',')), F.from_leaf_words(bottom.split(',')))
    return O.oriented_pd_code3(O.ternary_from_words(top.split(',')), O.ternary_from_words(bottom.split(',')))


def hfk(L):
    r = L.knot_floer_homology()['ranks']
    return frozenset(r.items()), frozenset(((-a, -m), v) for (a, m), v in r.items())


def verified(E, f, tries=20):
    """f(E) for a verified computation; on failure (e.g. a triangulation with a flat or negative shape) retry on
    randomized triangulations of the same manifold. Raises the last error."""
    err = None
    for _ in range(tries):
        try:
            return f(E)
        except Exception as e:  # noqa: PERF203
            err = e
            E.randomize()
    raise err


def canonical(E):
    return verified(E, lambda X: X.canonical_retriangulation(verified=True))


def volume(E):
    return verified(E, lambda X: X.volume(verified=True, bits_prec=100))


def ref(knot):
    """(HFK, verified volume, verified canonical retriangulation) of the KnotInfo diagram of knot."""
    if knot not in _REF:
        import snappy  # noqa: F401
        import spherogram
        from sage.all import KnotInfo
        pd = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + knot).link().pd_code()]
        L = spherogram.Link([[x - 1 for x in c] for c in pd])
        E = L.exterior()
        _REF[knot] = (hfk(L)[0], volume(E), canonical(E))
    return _REF[knot]


def relation(pd, knot, need_volume=True):
    """('not K', method) or ('rel', set of names) or ('uncertified', reason)."""
    import snappy  # noqa: F401
    import spherogram
    h, vol, C = ref(knot)
    L = spherogram.Link([[x - 1 for x in c] for c in pd])
    if need_volume:
        L2 = L.copy()
        L2.simplify('global')
        try:
            if h not in hfk(L2):
                return ('not K', 'hfk')
        except Exception:
            pass
    E = L.exterior()
    try:
        v = volume(E)
        if v.upper() < vol.lower() or v.lower() > vol.upper():
            return ('not K', 'volume')
    except Exception as e:
        if need_volume:
            return ('uncertified', 'volume: %s' % str(e)[:60])
    try:
        D = canonical(E)
    except Exception as e:
        return ('uncertified', 'canonical: %s' % str(e)[:60])
    rels = set()
    for iso in D.isomorphisms_to(C):
        M = iso.cusp_maps()[0]
        if M[0, 1] != 0 or M[1, 0] != 0:
            return ('uncertified', 'non-diagonal cusp map')
        rels.add(NAME[(int(M[0, 0]), int(M[1, 1]))])
    return ('rel', rels) if rels else ('not K', 'no isomorphism')


def check_chunk(task):
    """task = [group, knot, forbidden names, path, offset, count]."""
    group, knot, forbidden, path, offset, count = task
    out = {'task': task[:2] + task[3:5], 'not K': {}, 'other orientation': 0, 'uncertified': [], 'violations': []}
    with open(path) as f:
        f.seek(offset)
        for _ in range(count):
            line = f.readline()
            if not line:
                break
            fl = line.rstrip('\n').split('\t')
            try:
                kind, info = relation(oriented_pd(group, fl[1], fl[2]), knot)
            except Exception as e:
                kind, info = 'uncertified', str(e)[:60]
            if kind == 'not K':
                out['not K'][info] = out['not K'].get(info, 0) + 1
            elif kind == 'rel':
                if info & set(forbidden):
                    out['violations'].append((fl[1], fl[2], sorted(info)))
                else:
                    out['other orientation'] += 1
            else:
                out['uncertified'].append((fl[1], fl[2], info))
    return out


def check_witness(task):
    group, knot, name, top, bottom = task
    try:
        kind, info = relation(oriented_pd(group, top, bottom), knot, need_volume=False)
    except Exception as e:
        kind, info = 'uncertified', str(e)[:60]
    return knot, name, kind == 'rel' and name in info, (kind, sorted(info) if kind == 'rel' else info)


def main():
    from identify_lib import RobustPool
    from oriented_index import homfly_key
    from sage.all import KnotInfo
    group = sys.argv[1]
    processes = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    raw = os.path.join(HERE, 'results', {'Fvec': 'raw_Fvec', 'F3vec': 'raw_F3vec'}[group])
    nmax = max(int(f[1:-4]) for f in os.listdir(raw) if f.startswith('n') and f.endswith('.tsv'))
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, 'results', 'oriented_index_%s.csv' % group)))
            if r['verdict'] == 'DIFFERENT']
    tasks, wtasks = [], []
    for r in rows:
        k = r['knot']
        a, b = r['index_K'], r['index_Kr']
        if a.isdigit() and (not b.isdigit() or int(a) < int(b)):
            missing, hi, forbidden = 'Kr', (int(b) if b.isdigit() else nmax + 2), ['Kr', 'Km']
        else:
            missing, hi, forbidden = 'K', (int(a) if a.isdigit() else nmax + 2), ['K', 'Kmr']
        for name in ('K', 'Kr'):
            if r['witness_' + name]:
                t, bb = [x.strip() for x in r['witness_' + name].split('|')]
                wtasks.append([group, k, name, t, bb])
        ref_pd = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + k).link().pd_code()]
        key = homfly_key(ref_pd)
        for n in range(int(r['first_n_homfly']), hi, 2):
            idx = json.load(open(os.path.join(HERE, 'tmp_check', 'oriented_%s_c13_n%d' % (group, n), 'classes',
                                              'index.json')))
            for path, offset, count in idx.get(key, []):
                for s in range(0, count, 200):
                    # sub-chunks of 200 lines: skip the first s lines
                    tasks.append([group, k, forbidden, path, offset, min(200, count - s), s])
    # convert the sub-chunks into byte offsets
    fixed = []
    for t in tasks:
        group_, k, forbidden, path, offset, cnt, skip = t
        if skip:
            with open(path, 'rb') as f:
                f.seek(offset)
                for _ in range(skip):
                    f.readline()
                offset = f.tell()
        fixed.append([group_, k, forbidden, path, offset, cnt])
    tasks = fixed
    progress = os.path.join(HERE, 'tmp_check', 'verify_%s.jsonl' % group)
    done = {}
    if os.path.exists(progress):
        for line in open(progress):
            r = json.loads(line)
            done[tuple(r['task'])] = r
    todo = [t for t in tasks if tuple(t[:2] + t[3:5]) not in done]
    print('%d knots, %d witnesses, %d chunks (%d already done)' % (len(rows), len(wtasks), len(tasks),
                                                                  len(tasks) - len(todo)), flush=True)
    with RobustPool(processes) as pool:
        witnesses = list(pool.map(check_witness, wtasks))
        with open(progress, 'a') as prog:
            for i, r in enumerate(pool.map(check_chunk, todo), 1):
                prog.write(json.dumps(r) + '\n')
                prog.flush()
                done[tuple(r['task'])] = r
                if i % 100 == 0:
                    print('  %d / %d chunks' % (i, len(todo)), flush=True)
        dropped = list(pool.dropped)
    stats = {'not K': {}, 'other orientation': 0, 'uncertified': 0, 'violations': 0}
    bad_knots = set()
    for r in done.values():
        for m, c in r['not K'].items():
            stats['not K'][m] = stats['not K'].get(m, 0) + c
        stats['other orientation'] += r['other orientation']
        stats['uncertified'] += len(r['uncertified'])
        stats['violations'] += len(r['violations'])
        if r['uncertified'] or r['violations']:
            bad_knots.add(r['task'][1])
    for t in dropped:
        bad_knots.add(t[1])
    wbad = [(k, n, info) for k, n, ok, info in witnesses if not ok]
    certified = sorted({r['knot'] for r in rows} - bad_knots - {k for k, _, _ in wbad})
    lines = ['# Certified verification of the oriented %s-index results' % group, '',
             'Script `verify_oriented.py` (exact or interval-arithmetic methods only, see its docstring).', '',
             '- knots with index(K) != index(K^r): %d' % len(rows),
             '- witnesses certified: %d of %d%s' % (len(witnesses) - len(wbad), len(witnesses),
                                                   (' (not certified: %s)' % wbad[:10]) if wbad else ''),
             '- diagrams excluded as another knot: %s' % stats['not K'],
             '- diagrams of the same knot certified to be an allowed orientation: %d' % stats['other orientation'],
             '- diagrams not certified: %d; contradictions with the scan: %d; crashed chunks: %d' % (
                 stats['uncertified'], stats['violations'], len(dropped)),
             '- **knots whose result is fully certified: %d of %d**' % (len(certified), len(rows)),
             '- knots not fully certified: %s' % (', '.join(sorted(bad_knots | {k for k, _, _ in wbad})) or 'none')]
    open(os.path.join(HERE, 'results', 'oriented_verified_%s.md' % group), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
