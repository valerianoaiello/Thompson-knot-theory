"""
Systematic search for a knot K whose vec{F}-index differs from the one of its reverse Kr.

usage (from F_index/):   sage -python scripts/reverse_scan.py [--max-crossings 11] [--nmax 15] [--processes 8]

1. Targets: the non-invertible knots of KnotInfo (symmetry type chiral, negative or positive
   amphicheiral) with at most --max-crossings crossings; all are hyperbolic.
2. For every odd n <= nmax (knots only occur for odd n in vec{F}) one run of bin/fknots in vec mode, in
   parallel shards, stores every diagram whose HOMFLY class is the one of a target.
3. For each target, from the first n at which its class appears, every stored diagram g is compared with
   the oriented KnotInfo diagram of K (oriented.relation_to, in parallel, crash-proof pool): g realizes
   K ('same') or Kr ('reverse'), or Km / Kmr. Since L(g^-1) is the mirror image of the reverse of L(g),
   g^-1 realizes Kmr, Km, Kr, K respectively (checked again here on the first diagrams of each target).
   The vec{F}-index of K (resp. Kr) is the first n at which K (resp. Kr) is realized.
Output: results/reverse_scan.csv and results/reverse_scan.md.
"""
import argparse
import csv
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root (the scripts are in scripts/)
sys.path.insert(0, os.path.join(HERE, 'scripts'))

NONINVERTIBLE = ('chiral', 'negative amphicheiral', 'positive amphicheiral')
INVERSE = {'same': 'mirror reverse', 'reverse': 'mirror', 'mirror': 'reverse', 'mirror reverse': 'same'}
CHECK_INVERSE = 3  # diagrams per (knot, n) on which the rule for g^-1 is checked directly


def classify(task):
    """(knot, n, top, bottom, relations of g, relations of g^-1 or None)."""
    knot, n, top, bottom, ref, check = task
    import ftrees as F
    import oriented as O
    tp, tm = F.from_leaf_words(top.split(',')), F.from_leaf_words(bottom.split(','))
    try:
        rel = O.relation_to(O.oriented_pd_code(tp, tm), ref)
        rel_inv = O.relation_to(O.oriented_pd_code(tm, tp), ref) if check else None
    except Exception:
        return knot, n, top, bottom, ['error'], None
    return knot, n, top, bottom, sorted(rel), None if rel_inv is None else sorted(rel_inv)


def enumerate_n(n, keys_file, processes):
    """{key: [(top, bottom), ...]} for the target classes at n, and the number of knot diagrams."""
    tmp = tempfile.mkdtemp(prefix='reverse_scan_n%d_' % n)
    outs = [os.path.join(tmp, 's.tsv.%d' % s) for s in range(processes)]
    # one fknots process: it builds the trees once and forks the workers, which share them
    procs = [subprocess.Popen([os.path.join(HERE, 'bin', 'fknots'), str(n), '-1', str(processes),
                               os.path.join(tmp, 's.tsv'), '1000000000', 'vec', '@' + keys_file])]
    for p in procs:
        assert p.wait() == 0
    found, knots = {}, 0
    for out in outs:
        with open(out) as f:
            head = f.readline()
            knots += int(dict(kv.split('=') for kv in head[2:].split() if '=' in kv)['knots'])
            for line in f:
                key, count, mincr, reps = line.rstrip('\n').split('\t')
                if reps:
                    found.setdefault(key, []).extend(tuple(r.split('|')[:2]) for r in reps.split(';'))
        os.remove(out)
    os.rmdir(tmp)
    return found, knots


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-crossings', type=int, default=11)
    ap.add_argument('--nmax', type=int, default=15)
    ap.add_argument('--processes', type=int, default=os.cpu_count())
    args = ap.parse_args()

    from sage.all import KnotInfo
    from oriented_index import homfly_key
    from identify_lib import RobustPool

    t0 = time.time()
    targets = {}  # knot -> (symmetry type, crossing number, reference PD)
    for K in KnotInfo:
        if K.is_knot() and 3 <= K.crossing_number() <= args.max_crossings and K.symmetry_type() in NONINVERTIBLE:
            targets[K.value] = (K.symmetry_type(), K.crossing_number(),
                                [list(map(int, c)) for c in K.link().pd_code()])
    by_key = {}
    for knot, (_, _, ref) in targets.items():
        by_key.setdefault(homfly_key(ref), []).append(knot)
    keys_file = os.path.join(tempfile.mkdtemp(prefix='reverse_scan_keys_'), 'keys.txt')
    with open(keys_file, 'w') as f:
        for key in by_key:
            f.write(key + '\n')
    print('%d non-invertible knots with <= %d crossings, %d HOMFLY classes' % (
        len(targets), args.max_crossings, len(by_key)), flush=True)

    # 2) enumeration
    diagrams = {}  # (knot, n) -> [(top, bottom)]
    first_n = {}
    for n in range(5, args.nmax + 1, 2):
        found, nknots = enumerate_n(n, keys_file, args.processes)
        nd = 0
        for key, ds in found.items():
            for knot in by_key.get(key, []):
                diagrams[(knot, n)] = ds
                first_n.setdefault(knot, n)
                nd += len(ds)
        print('n = %2d: %d knot diagrams in vec{F}, %d in the classes of %d targets (%.0f s)' % (
            n, nknots, nd, sum(1 for k in targets if (k, n) in diagrams), time.time() - t0), flush=True)

    # 3) orientations, n by n; a target is done as soon as K and Kr have both been realized
    index = {k: {} for k in targets}      # knot -> {orientation: first n}
    counts = {}                           # (knot, n) -> {orientation: number of elements g, g^-1}
    inverse_rule_ok, inverse_rule_checked = True, 0
    with RobustPool(args.processes) as pool:
        for n in range(5, args.nmax + 1, 2):
            tasks = []
            for knot in targets:
                if (knot, n) not in diagrams or ('K' in index[knot] and 'Kr' in index[knot]):
                    continue
                for i, (top, bottom) in enumerate(diagrams[(knot, n)]):
                    tasks.append((knot, n, top, bottom, targets[knot][2], i < CHECK_INVERSE))
            if not tasks:
                continue
            for knot, m, top, bottom, rel, rel_inv in pool.map(classify, tasks):
                if rel_inv is not None:
                    inverse_rule_checked += 1
                    if sorted(INVERSE[r] for r in rel) != rel_inv:
                        inverse_rule_ok = False
                        print('  inverse rule FAILS on %s %s|%s: %s vs %s' % (knot, top, bottom, rel, rel_inv), flush=True)
                c = counts.setdefault((knot, m), {'K': 0, 'Kr': 0, 'Km': 0, 'Kmr': 0, 'other': 0, 'error': 0})
                if rel == ['error']:
                    c['error'] += 1
                    continue
                if not rel:  # another knot with the same HOMFLY (or an isometry SnapPy did not find)
                    c['other'] += 1
                    continue
                for r in rel:  # g and g^-1
                    for name in ({'same': 'K', 'reverse': 'Kr', 'mirror': 'Km', 'mirror reverse': 'Kmr'}[r],
                                 {'same': 'Kmr', 'reverse': 'Km', 'mirror': 'Kr', 'mirror reverse': 'K'}[r]):
                        c[name] += 1
                        index[knot].setdefault(name, m)
            done = sum(1 for k in targets if 'K' in index[k] and 'Kr' in index[k])
            print('n = %2d: %d diagrams classified; %d targets with both K and Kr found so far (%.0f s)' % (
                n, len(tasks), done, time.time() - t0), flush=True)
        dropped = list(pool.dropped)

    # 4) output
    def ckey(k):
        c, rest = k.split('_')
        return (int(c.rstrip('an')), rest[0] if not rest[0].isdigit() else '', int(rest.lstrip('an')))

    rows = []
    for knot in sorted(targets, key=ckey):
        sym, cn, _ = targets[knot]
        ik, ikr = index[knot].get('K'), index[knot].get('Kr')
        fmt = lambda v: str(v) if v else '> %d' % args.nmax
        if ik and ikr:
            verdict = 'equal' if ik == ikr else 'DIFFERENT'
        elif ik or ikr:
            verdict = 'DIFFERENT'  # one is <= nmax, the other > nmax
        else:
            verdict = 'unknown (class first at n = %s)' % first_n[knot] if knot in first_n else 'unknown'
        c = counts.get((knot, ik or ikr), {})
        rows.append({'knot': knot, 'crossing_number': cn, 'symmetry': sym,
                     'first_n_homfly': first_n.get(knot, '> %d' % args.nmax),
                     'Fvec_index_K': fmt(ik), 'Fvec_index_Kr': fmt(ikr), 'verdict': verdict,
                     'elements_K': c.get('K', ''), 'elements_Kr': c.get('Kr', ''),
                     'diagrams_other_knot': c.get('other', ''), 'diagrams_snappy_error': c.get('error', '')})
    with open(os.path.join(HERE, 'results', 'reverse_scan.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(HERE, 'results', 'reverse_scan.md'), 'w') as f:
        f.write('# vec{F}-index of non-invertible knots K and of their reverse Kr\n\n')
        f.write('Non-invertible knots of KnotInfo with <= %d crossings; all tree diagrams of vec{F} with n <= %d '
                'leaves. K is the orientation of KnotInfo; the convention of the colouring (+ = counterclockwise) '
                'fixes which one is K and which Kr, the question "equal or different" does not depend on it. '
                'Elements = number of g in vec{F} (g and g^-1 counted separately) realizing K / Kr at that n.\n\n'
                % (args.max_crossings, args.nmax))
        f.write('Inverse rule L(g^-1) = mirror of the reverse of L(g): %s on %d diagrams. '
                'Diagrams skipped because they crash SnapPy: %d.\n\n'
                % ('ok' if inverse_rule_ok else 'FAILED', inverse_rule_checked, len(dropped)))
        f.write('Other = diagrams of the same HOMFLY class at that n that are not K, Kr, Km, Kmr (another knot, '
                'or an isometry SnapPy did not find): a DIFFERENT verdict with other > 0 must be checked.\n\n')
        f.write('| knot | symmetry | first n of its HOMFLY | vec{F}-index K | vec{F}-index Kr | verdict | '
                'elements K / Kr | other / errors |\n')
        f.write('|---|---|---|---|---|---|---|---|\n')
        for r in rows:
            f.write('| %s | %s | %s | %s | %s | %s | %s / %s | %s / %s |\n' % (
                r['knot'], r['symmetry'], r['first_n_homfly'], r['Fvec_index_K'], r['Fvec_index_Kr'],
                r['verdict'], r['elements_K'], r['elements_Kr'], r['diagrams_other_knot'],
                r['diagrams_snappy_error']))
    diff = [r for r in rows if r['verdict'] == 'DIFFERENT']
    print('done in %.0f s: %d targets, %d with both indices <= %d, %d DIFFERENT: %s' % (
        time.time() - t0, len(rows), sum(1 for r in rows if r['verdict'] == 'equal') + len(diff), args.nmax,
        len(diff), ', '.join(r['knot'] for r in diff) or '-'), flush=True)


if __name__ == '__main__':
    main()
