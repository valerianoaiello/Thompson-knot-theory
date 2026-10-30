"""
Oriented vec{F}-index and vec{F}_3-index of the non-invertible knots: the four values for K, Kr (reverse),
Km (mirror image) and Kmr.

usage (from F_index/):   sage -python oriented_scan.py GROUP [processes] [max_crossings]
                         (GROUP = Fvec or F3vec; max_crossings 13 by default)

The vec{F}-index and the vec{F}_3-index are indices of oriented knots: L(g) is oriented by the colouring of
the Tait graph (oriented.py). Since L(g^-1) is the mirror image of the reverse of L(g) (Aiello-Conti, CAOT 13
(2019) Remark 3.8 for vec{F}; checked for vec{F}_3 by tests/check_oriented3.py), index(K) = index(Kmr) and
index(Kr) = index(Km). For an invertible knot (K = Kr) the four values coincide with the index of the
unoriented knot up to mirror image in results/<G>_index.csv. For a non-invertible knot that table gives
min(index(K), index(Kr)); this script computes both.

Targets: the non-invertible knots of KnotInfo (symmetry type chiral, negative or positive amphicheiral) with
at most max_crossings crossings whose HOMFLY class appears at some n <= n_max (lower bound of
results/<G>_index.csv). Every diagram of their HOMFLY classes is enumerated (all-diagram mode of the
enumerators, in tmp_check/, as complete_check.py) and n by n every diagram g is compared with the oriented
KnotInfo diagram of K: hyperbolic volume, then SnapPy isometries and their action on (meridian, longitude)
(oriented.relation_to). g realizes K, Kr, Km or Kmr, and g^-1 the corresponding Kmr, Km, Kr, K; the rule is
also checked directly on the first diagrams that match in every chunk. A target is done once K and Kr are
both realized. Diagrams without a hyperbolic structure (5 tries) are counted as undecided.
Progress: tmp_check/oriented_<G>_c<max_crossings>.jsonl (resumed after a restart).
Output: results/oriented_index_<G>.csv and .md.
"""
import csv
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import complete_check as C  # noqa: E402

NONINVERTIBLE = ('chiral', 'negative amphicheiral', 'positive amphicheiral')
NAME = {'same': 'K', 'reverse': 'Kr', 'mirror': 'Km', 'mirror reverse': 'Kmr'}
INVERSE = {'K': 'Kmr', 'Kr': 'Km', 'Km': 'Kr', 'Kmr': 'K'}
RAW = {'Fvec': 'raw_Fvec', 'F3vec': 'raw_F3vec'}
CHECK_INVERSE = 2   # matching diagrams per chunk on which the rule for g^-1 is checked directly

_REF = {}           # per process: knot -> (volume, exterior)


def _ref(knot, pd):
    if knot not in _REF:
        import snappy  # noqa: F401
        import spherogram
        E = spherogram.Link([[x - 1 for x in c] for c in pd]).exterior()
        hyp = C._geometric(E)
        _REF[knot] = (float(E.volume()) if hyp else None, E)
    return _REF[knot]


def oriented_pd(group, top, bottom):
    import oriented as O
    if group == 'Fvec':
        import ftrees as F
        return O.oriented_pd_code(F.from_leaf_words(top.split(',')), F.from_leaf_words(bottom.split(',')))
    return O.oriented_pd_code3(O.ternary_from_words(top.split(',')), O.ternary_from_words(bottom.split(',')))


def relations(pd, E, ref_E):
    """Set of names (K, Kr, Km, Kmr) of the oriented knot of exterior E w.r.t. the reference exterior."""
    out = set()
    for iso in E.is_isometric_to(ref_E, return_isometries=True) or []:
        M = iso.cusp_maps()[0]
        assert M[0, 1] == 0 and M[1, 0] == 0, M
        m, l = int(M[0, 0]), int(M[1, 1])
        out.add(NAME['same' if m == 1 else 'reverse'] if m == l else NAME['mirror' if l == 1 else 'mirror reverse'])
    return out


def classify_chunk(task):
    """task = [group, n, path, offset, count, {knot: (ref_pd, already_found)}]."""
    import snappy  # noqa: F401
    import spherogram
    group, n, path, offset, count, knots = task
    found = {k: {} for k in knots}            # knot -> {name: (top, bottom)}
    stats = {k: {'other': 0, 'undecided': 0, 'compared': 0} for k in knots}
    inv_checked, inv_failed = 0, []
    with open(path) as f:
        f.seek(offset)
        for _ in range(count):
            line = f.readline()
            if not line:
                break
            fl = line.rstrip('\n').split('\t')
            top, bottom = fl[1], fl[2]
            live = [k for k in knots if not ({'K', 'Kr'} <= set(found[k]) | set(knots[k][1]))]
            if not live:
                break
            try:
                pd = oriented_pd(group, top, bottom)
                E = spherogram.Link([[x - 1 for x in c] for c in pd]).exterior()
                geo = C._geometric(E)
                vol = float(E.volume()) if geo else None
            except Exception:
                geo = False
            for k in live:
                stats[k]['compared'] += 1
                vk, Ek = _ref(k, knots[k][0])
                if not geo or vk is None:
                    stats[k]['undecided'] += 1
                    continue
                if abs(vol - vk) > C.VOLUME_EPS:
                    stats[k]['other'] += 1
                    continue
                try:
                    rel = relations(pd, E, Ek)
                except Exception:
                    stats[k]['undecided'] += 1
                    continue
                if not rel:
                    stats[k]['other'] += 1
                    continue
                if inv_checked < CHECK_INVERSE:
                    inv_checked += 1
                    Ei = spherogram.Link([[x - 1 for x in c] for c in oriented_pd(group, bottom, top)]).exterior()
                    if C._geometric(Ei):
                        rel_inv = relations(None, Ei, Ek)
                        if rel_inv != {INVERSE[r] for r in rel}:
                            inv_failed.append((k, top, bottom, sorted(rel), sorted(rel_inv)))
                for r in rel:
                    found[k].setdefault(r, (top, bottom))
                    found[k].setdefault(INVERSE[r], (bottom, top))
    return {'n': n, 'path': path, 'offset': offset, 'found': found, 'stats': stats,
            'inverse_checked': inv_checked, 'inverse_failed': inv_failed}


def main():
    group = sys.argv[1]
    assert group in RAW
    processes = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    maxc = int(sys.argv[3]) if len(sys.argv) > 3 else 13
    from sage.all import KnotInfo
    from identify_lib import RobustPool
    from oriented_index import homfly_key
    t0 = time.time()
    tdir = os.path.join(HERE, 'tmp_check')
    nmax = max(int(m) for m in re.findall(r'n(\d+)\.tsv', ' '.join(os.listdir(os.path.join(HERE, 'results', RAW[group])))))
    table = {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', group + '_index.csv')))}

    targets = {}  # knot -> dict(sym, cn, ref, key, lb)
    for K in KnotInfo:
        if not K.is_knot() or not 3 <= K.crossing_number() <= maxc or K.symmetry_type() not in NONINVERTIBLE:
            continue
        r = table.get(K.value)
        if r is None or int(r['lower_bound']) > nmax:
            continue
        ref = [list(map(int, c)) for c in K.link().pd_code()]
        targets[K.value] = dict(sym=K.symmetry_type(), cn=K.crossing_number(), ref=ref, key=homfly_key(ref),
                                lb=int(r['lower_bound']), table=r[group + '_index'])
    tag = '%s_c%d' % (group, maxc)
    keys_file = os.path.join(tdir, 'keys_oriented_%s.txt' % tag)
    with open(keys_file, 'w') as f:
        f.writelines(k + '\n' for k in sorted({t['key'] for t in targets.values()}))
    print('%d non-invertible knots with <= %d crossings and HOMFLY class at n <= %d, %d classes (%.0f s)' % (
        len(targets), maxc, nmax, len({t['key'] for t in targets.values()}), time.time() - t0), flush=True)

    found = {k: {} for k in targets}       # knot -> {name: (n, top, bottom)}
    stats = {k: {} for k in targets}       # knot -> {n: {'other', 'undecided', 'compared'}}
    inv_checked, inv_failed = 0, []
    progress = os.path.join(tdir, 'oriented_%s.jsonl' % tag)
    done_chunks = set()
    if os.path.exists(progress):
        for line in open(progress):
            r = json.loads(line)
            done_chunks.add((r['path'], r['offset']))
            for k, d in r['found'].items():
                for name, tb in d.items():
                    if name not in found[k] or found[k][name][0] > r['n']:
                        found[k][name] = (r['n'], tb[0], tb[1])
            for k, s in r['stats'].items():
                acc = stats[k].setdefault(r['n'], {'other': 0, 'undecided': 0, 'compared': 0})
                for x in acc:
                    acc[x] += s[x]
            inv_checked += r['inverse_checked']
            inv_failed += r['inverse_failed']
        print('resumed: %d chunks already done' % len(done_chunks), flush=True)

    def complete(k, n):
        return all(name in found[k] and found[k][name][0] < n for name in ('K', 'Kr'))

    with RobustPool(processes) as pool, open(progress, 'a') as prog:
        for n in range(min(t['lb'] for t in targets.values()), nmax + 1, 2):
            d = os.path.join(tdir, 'oriented_%s_n%d' % (tag, n))
            live_keys = {t['key'] for k, t in targets.items() if t['lb'] <= n and not complete(k, n)}
            if not live_keys:
                continue
            if not os.path.exists(os.path.join(d, 'done')):
                t1 = time.time()
                C.enumerate_n(group, n, d, keys_file, processes)
                print('n = %d: all diagrams of the target classes written (%.0f s)' % (n, time.time() - t1), flush=True)
            index = C.split_classes(d, [t['key'] for t in targets.values()])
            by_key = {}
            for k, t in targets.items():
                if t['lb'] <= n and not complete(k, n):
                    by_key.setdefault(t['key'], []).append(k)
            tasks = []
            for key, ks in by_key.items():
                for path, offset, count in index.get(key, []):
                    if (path, offset) not in done_chunks:
                        tasks.append([group, n, path, offset, count,
                                      {k: (targets[k]['ref'], sorted(found[k])) for k in ks}])
            print('n = %d: %d chunks for %d targets (%.0f s)' % (
                n, len(tasks), sum(len(v) for v in by_key.values()), time.time() - t0), flush=True)

            def skip(t):
                for k in list(t[5]):
                    if {'K', 'Kr'} <= set(found[k]):
                        del t[5][k]
                    else:
                        t[5][k] = (t[5][k][0], sorted(found[k]))
                return not t[5]

            for i, r in enumerate(pool.map(classify_chunk, tasks, skip=skip), 1):
                prog.write(json.dumps(r) + '\n')
                prog.flush()
                for k, dd in r['found'].items():
                    for name, tb in dd.items():
                        if name not in found[k]:
                            found[k][name] = (n, tb[0], tb[1])
                for k, s in r['stats'].items():
                    acc = stats[k].setdefault(n, {'other': 0, 'undecided': 0, 'compared': 0})
                    for x in acc:
                        acc[x] += s[x]
                inv_checked += r['inverse_checked']
                inv_failed += r['inverse_failed']
                for fail in r['inverse_failed']:
                    print('  inverse rule FAILS: %s' % (fail,), flush=True)
                if i % 200 == 0:
                    print('  %d / %d chunks (n = %d), %.0f s' % (i, len(tasks), n, time.time() - t0), flush=True)
            print('n = %d done: %d targets with K and Kr found (%.0f s)' % (
                n, sum(1 for k in targets if {'K', 'Kr'} <= set(found[k])), time.time() - t0), flush=True)
        dropped = list(pool.dropped)

    # output
    def ckey(k):
        c, rest = k.split('_')
        cr = int(c.rstrip('an'))
        return (cr, c[len(str(cr)):], int(rest))

    rows = []
    for k in sorted(targets, key=ckey):
        t = targets[k]
        v = {name: found[k][name][0] if name in found[k] else None for name in ('K', 'Kr', 'Km', 'Kmr')}

        def fmt(name):
            if v[name] is not None:
                return str(v[name])
            und = sum(s['undecided'] for s in stats[k].values())
            return '> %d' % nmax + (' (%d undecided)' % und if und else '')

        if v['K'] and v['Kr']:
            verdict = 'equal' if v['K'] == v['Kr'] else 'DIFFERENT'
        elif v['K'] or v['Kr']:
            verdict = 'DIFFERENT'
        else:
            verdict = 'both > %d' % nmax
        und_before = sum(s['undecided'] for m, s in stats[k].items()
                         if m < max(x for x in (v['K'], v['Kr'], nmax + 1) if x))
        w = found[k]
        rows.append({'knot': k, 'crossing_number': t['cn'], 'symmetry': t['sym'],
                     'first_n_homfly': t['lb'], 'unoriented_table_index': t['table'],
                     'index_K': fmt('K'), 'index_Kr': fmt('Kr'), 'index_Km': fmt('Km'), 'index_Kmr': fmt('Kmr'),
                     'verdict': verdict, 'undecided_diagrams_before': und_before,
                     'witness_K': '%s | %s' % w['K'][1:] if 'K' in w else '',
                     'witness_Kr': '%s | %s' % w['Kr'][1:] if 'Kr' in w else ''})
    base = os.path.join(HERE, 'results', 'oriented_index_%s' % group + ('' if maxc == 13 else '_c%d' % maxc))
    with open(base + '.csv', 'w', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    gname = {'Fvec': 'vec{F}', 'F3vec': 'vec{F}_3'}[group]
    inconsistent = []
    for r in rows:
        vals = [int(x) for x in (r['index_K'], r['index_Kr']) if x.isdigit()]
        if (str(min(vals)) if vals else '') != r['unoriented_table_index']:
            inconsistent.append(r['knot'])
    with open(base + '.md', 'w') as f:
        f.write('# Oriented %s-index of the non-invertible knots\n\n' % gname)
        f.write('Non-invertible knots of KnotInfo with <= %d crossings whose HOMFLY class appears at n <= %d; every '
                'tree diagram of %s of those classes with n <= %d was compared with the oriented KnotInfo diagram K '
                '(oriented_scan.py). K = KnotInfo orientation, Kr = reverse, Km = mirror image, Kmr = both. '
                'index(K) = index(Kmr) and index(Kr) = index(Km) (L(g^-1) is the mirror image of the reverse '
                'of L(g)); for invertible knots all four values equal the index of results/%s_index.csv.\n\n'
                % (maxc, nmax, gname, nmax, group))
        f.write('Rule for g^-1 checked directly on %d diagrams: %s. Chunks skipped because they crash SnapPy: %d. '
                'min(index K, index Kr) differs from the unoriented table for: %s.\n\n'
                % (inv_checked, 'ok' if not inv_failed else '%d FAILURES' % len(inv_failed), len(dropped),
                   ', '.join(inconsistent) or 'none'))
        f.write('| knot | symmetry | first n of HOMFLY | table (unoriented) | K | Kr | Km | Kmr | verdict |\n')
        f.write('|---|---|---|---|---|---|---|---|---|\n')
        for r in rows:
            f.write('| %s | %s | %s | %s | %s | %s | %s | %s | %s |\n' % (
                r['knot'], r['symmetry'], r['first_n_homfly'], r['unoriented_table_index'] or '-', r['index_K'],
                r['index_Kr'], r['index_Km'], r['index_Kmr'], r['verdict']))
    diff = [r['knot'] for r in rows if r['verdict'] == 'DIFFERENT']
    print('done in %.0f s: %d targets, %d DIFFERENT; rule for g^-1 %s on %d; inconsistent with the table: %s' % (
        time.time() - t0, len(rows), len(diff), 'ok' if not inv_failed else 'FAILED', inv_checked,
        ', '.join(inconsistent) or 'none'), flush=True)


if __name__ == '__main__':
    main()
