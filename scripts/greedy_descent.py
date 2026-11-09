"""
Greedy descent from a large diagram of a knot (e.g. the vec{F}_3 diagram built by alexander.py): at each
step, the pairs (T+', T-') obtained by deleting k internal vertices in each tree (k = 2 in vec{F}_3, the
deletions of descent_search.py) that stay in the group are tried in random order, and the first one that
still gives the knot (determinant, then SnapPy: volume and isometry, after simplifying the diagram) is
kept. Stops when no pair of a step gives the knot (then descent_search.py takes over) or at n_min.

usage (from F_index/): sage -python scripts/greedy_descent.py START.json [processes] [--n-min N] [--seed S]
       [--max-k K] (up to K deletions per tree, default 12) [--skip-first K] (first step: skip k <= K)
START.json: {"knot", "F3vec": "top | bottom"} (as written by alexander.py). Progress (one line per step,
resumable) in START_greedy.jsonl, next to START.json.
"""
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root (the scripts are in scripts/)
sys.path.insert(0, os.path.join(HERE, 'scripts'))
import descent_search as D  # noqa: E402

GROUP = 'F3vec'  # --group Fvec: binary trees of vec{F} (the 'Fvec' diagram of START.json)
BATCH = 64
KS = (2, 4, 6, 8, 10, 12)  # deletions per tree tried at each step (> 2: inside windows)
MAX_SET = 20000  # windows with more candidate trees than this are skipped


def deletions_in(t, lo, hi):
    """Trees obtained from the ternary tree t by deleting one internal vertex (as in descent_search) whose
    leaves are all in [lo, hi] (leaf indices from 0)."""
    def size(s):
        return 1 if s is None else sum(size(c) for c in s)

    def rec(s, off):
        if s is None:
            return []
        res = []
        rest = [c for c in s if c is not None]
        if len(rest) <= 1 and lo <= off and off + size(s) - 1 <= hi:
            res.append(rest[0] if rest else None)
        o = off
        for i, c in enumerate(s):
            for c2 in rec(c, o):
                res.append(s[:i] + (c2,) + s[i + 1:])
            o += size(c)
        return res
    return set(rec(t, 0))


def window_pairs(tp, tm, k, width):
    """Pairs (T+', T-') in the group, k deletions in each tree, all inside one window of `width` consecutive
    leaves (the same window in both trees); the window shrinks by 2 leaves after each deletion."""
    L = len(D.words(GROUP, tp))
    lv = D.ARITY[GROUP] - 1  # leaves removed by one deletion
    out = set()
    for lo in range(0, max(1, L - width + 1), lv):
        P, M = {tp}, {tm}
        hi = lo + width - 1
        for j in range(k):
            P = {u for s in P for u in deletions_in(s, lo, hi - lv * j)}
            M = {u for s in M for u in deletions_in(s, lo, hi - lv * j)}
            if len(P) > MAX_SET or len(M) > MAX_SET:
                break
        if len(P) > MAX_SET or len(M) > MAX_SET or not P or not M:
            continue
        if len(D.words(GROUP, next(iter(P)))) != L - lv * k:
            continue
        kp, km = {}, {}
        for t in P:
            kp.setdefault(D.key(GROUP, t), []).append(','.join(D.words(GROUP, t)))
        for t in M:
            km.setdefault(D.key(GROUP, t), []).append(','.join(D.words(GROUP, t)))
        for kk in kp.keys() & km.keys():
            out.update((a, b) for a in kp[kk] for b in km[kk])
    return list(out)


def test(task):
    """task = (group, knot, det, [(top, bottom), ...]): the first pair giving the knot, or None; and counts."""
    import snappy  # noqa: F401
    import spherogram
    import complete_check as C
    global GROUP
    GROUP, knot, det, pairs = task  # the group travels with the task (worker processes do not see --group)
    ref, vk, Ek, _ = D._ref(knot)
    counts = {'pairs': 0, 'det': 0, 'snappy': 0}
    for top, bottom in pairs:
        counts['pairs'] += 1
        tp, tm = D.tree(GROUP, top), D.tree(GROUP, bottom)
        if D.determinant(*D.tait(GROUP, tp, tm)) != det:
            continue
        counts['det'] += 1
        pd = D.pd_code(GROUP, tp, tm)
        if pd is None:
            continue
        S = spherogram.Link([[x - 1 for x in c] for c in pd])
        if vk is None:  # non-hyperbolic knot (torus knots): KnotInfo recognition
            counts['snappy'] += 1
            if D.same_by_knotinfo(S, knot):
                return (top, bottom), counts
            continue
        S.simplify('global')
        if len(S.crossings) == 0:
            continue
        E = S.exterior()
        counts['snappy'] += 1
        try:
            if C._geometric(E) and abs(float(E.volume()) - vk) < C.VOLUME_EPS and E.is_isometric_to(Ek):
                return (top, bottom), counts
        except Exception:
            continue
    return None, counts


def main():
    global GROUP
    args = sys.argv[1:]
    if '--group' in args:
        GROUP = args[args.index('--group') + 1]
    start = json.load(open(args[0]))
    procs = int(args[1]) if len(args) > 1 and not args[1].startswith('--') else 4
    n_min = int(args[args.index('--n-min') + 1]) if '--n-min' in args else 15
    seed = int(args[args.index('--seed') + 1]) if '--seed' in args else 1
    rnd = random.Random(seed)
    max_k = int(args[args.index('--max-k') + 1]) if '--max-k' in args else KS[-1]
    skip_first = int(args[args.index('--skip-first') + 1]) if '--skip-first' in args else 0
    ks = tuple(range(2, max_k + 1, 2))
    first = True
    knot = start['knot']
    out = os.path.join(os.path.dirname(os.path.abspath(args[0])),
                       os.path.basename(args[0]).replace('.json', '') + '_greedy.jsonl')
    top, bottom = [x.strip() for x in start[GROUP].split('|')]
    if os.path.exists(out):
        last = [json.loads(x) for x in open(out) if x.strip()][-1]
        top, bottom = [x.strip() for x in last['diagram'].split('|')]
    _, _, _, det = D._ref(knot)
    from identify_lib import RobustPool

    def log(msg):
        print(time.strftime('%H:%M:%S'), msg, flush=True)
    with RobustPool(procs) as pool:
        while True:
            tp, tm = D.tree(GROUP, top), D.tree(GROUP, bottom)
            n = (len(top.split(',')) + 1) // 2 if D.ARITY[GROUP] == 3 else len(top.split(','))
            if n <= n_min:
                log('reached n = %d' % n)
                break
            t0 = time.time()
            hit, tot, step = None, {'pairs': 0, 'det': 0, 'snappy': 0}, 0
            # k vertices deleted in each tree: 2 (all the pairs), then more inside windows of leaves
            for k in ks:
                if first and k <= skip_first:
                    continue
                if k == 2:
                    P, M = {}, {}
                    for t in D.neighbours(tp, D.ARITY[GROUP], 2, 0):
                        P.setdefault(D.key(GROUP, t), []).append(','.join(D.words(GROUP, t)))
                    for t in D.neighbours(tm, D.ARITY[GROUP], 2, 0):
                        M.setdefault(D.key(GROUP, t), []).append(','.join(D.words(GROUP, t)))
                    pairs = [(a, b) for kk in P.keys() & M.keys() for a in P[kk] for b in M[kk]]
                else:
                    pairs = window_pairs(tp, tm, k, 4 * k + 8 if D.ARITY[GROUP] == 3 else 2 * k + 6)
                rnd.shuffle(pairs)
                tasks = [(GROUP, knot, det, pairs[i:i + BATCH]) for i in range(0, len(pairs), BATCH)]
                for w in range(0, len(tasks), 2 * procs):  # waves, so that a hit stops the step
                    for h, c in pool.map(test, tasks[w:w + 2 * procs]):
                        for x, v in c.items():
                            tot[x] += v
                        if h is not None and hit is None:
                            hit = h
                    if hit is not None:
                        break
                if hit is not None:
                    step = k
                    break
                log('n = %d: nothing with %d deletions per tree (%d pairs)' % (n, k, len(pairs)))
            log('n = %d -> %d: tried %s, %s (%.0f s)' % (
                n, n - step, tot, 'found' if hit else 'nothing', time.time() - t0))
            first = False
            if hit is None:
                break
            top, bottom = hit
            with open(out, 'a') as f:
                f.write(json.dumps({'n': n - step, 'diagram': top + ' | ' + bottom}) + '\n')


if __name__ == '__main__':
    main()
