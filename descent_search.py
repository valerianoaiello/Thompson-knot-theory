"""
Targeted search for smaller diagrams of single knots ("descent"): starting from known tree diagrams of a knot K
with n leaves (n - 1 internal vertices per tree, ternary: n = internal vertices + 1), delete internal vertices
in both trees and keep the diagrams that are still in the group and still give K. One step lowers n by 1 in F
and F_3, by 2 in vec{F} and vec{F}_3 (knots only occur for odd n there).

Neighbours of a tree: k + extra deletions, then extra insertions (k = 1 in F and F_3, 2 in vec{F} and
vec{F}_3; "extra" in the job, default 1). Deleting a vertex: an internal vertex whose children are leaves
except at most one is replaced by that child (a binary vertex with a leaf child, a ternary vertex with at
least two leaf children). Inserting a vertex: a subtree (a leaf included) is replaced by a new vertex with
the subtree as one of its children and leaves as the others. All the pairs (T+', T-') of neighbours of T+
and of T- are examined, so the leaves of the two trees are re-matched. This is a heuristic: a diagram found is a
proof of an upper bound (it is checked with SnapPy and then certified with the methods of certify_indices.py),
not finding one proves nothing.

Filters, from the cheapest: membership in the group (equal parity vectors of the leaves in vec{F} and vec{F}_3),
the determinant (|det| of the reduced signed Laplacian of the Tait graph), one component, and finally SnapPy:
volume and isometry with K (unoriented: any orientation and mirror), or, with `want`, the oriented type
(relation_to, e.g. {'reverse', 'mirror'} for the reverse of K up to the inverse rule).

usage (from F_index/): sage -python descent_search.py TASKS.json [processes]
Environment variable DESCENT_OUT: write to that file instead (used to split the jobs between machines).
TASKS.json: list of {"name", "group", "knot", "starts": ["top | bottom", ...], "steps", "want" (optional list
of relations), "beam" (optional), "up" (optional), "ks" (optional list: vertices removed at each step, 0 for
a sideways step at the same size)}.
Ascent ("up": m): each step inserts m vertices in each tree instead of deleting (extra deletions, then m + extra
insertions). The starts may lie in a larger group with the same arity: e.g. F_3 diagrams of K as starts of a job
in vec{F}_3, where only the pairs in vec{F}_3 are examined (an upper bound for the vec{F}_3-index from an
F_3 diagram, in the spirit of the substitutions of Aiello, AGT 20 (2020) 429-438). Output: results/descent_search.csv (appended), log on stdout. The jobs done
are recorded in tmp_check/descent/done_<TASKS>.txt and skipped when the same file is run again.
"""
import csv
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

ARITY = {'F': 2, 'Fvec': 2, 'F3': 3, 'F3vec': 3}
STEP = {'F': 1, 'F3': 1, 'Fvec': 2, 'F3vec': 2}
CHUNK_TOPS = 20


# ---------------------------------------------------------------------------------------------
# trees (nested tuples, a leaf is None)
# ---------------------------------------------------------------------------------------------

def words(group, t):
    import ftrees as F
    import oriented as O
    return F.leaf_words(t) if ARITY[group] == 2 else O.ternary_words(t)


def tree(group, ws):
    import ftrees as F
    import oriented as O
    return F.from_leaf_words(ws.split(',')) if ARITY[group] == 2 else O.ternary_from_words(ws.split(','))


def deletions(t, arity):
    """Trees obtained from t by deleting one internal vertex (see the docstring)."""
    out = set()

    def rec(s):
        if s is None:
            return []
        res = []
        rest = [c for c in s if c is not None]
        if len(rest) <= 1:
            res.append(rest[0] if rest else None)
        for i, c in enumerate(s):
            for c2 in rec(c):
                res.append(s[:i] + (c2,) + s[i + 1:])
        return res
    out.update(rec(t))
    return out


def insertions(t, arity):
    """Trees obtained from t by inserting one internal vertex: a subtree s (a leaf included) is replaced by a
    new vertex with s as one of its children and leaves as the others."""
    def rec(s):
        res = [tuple(s if j == i else None for j in range(arity)) for i in range(arity)]
        if s is not None:
            for i, c in enumerate(s):
                for c2 in rec(c):
                    res.append(s[:i] + (c2,) + s[i + 1:])
        return res
    return set(rec(t))


def neighbours(t, arity, k, extra):
    """Trees with k fewer internal vertices (k < 0: -k more): max(k, 0) + extra deletions, then max(-k, 0) + extra
    insertions."""
    level = {t}
    for _ in range(max(k, 0) + extra):
        level = {u for s in level for u in deletions(s, arity)}
    for _ in range(max(-k, 0) + extra):
        level = {u for s in level for u in insertions(s, arity)}
    return level


def key(group, t):
    """Pairs (T+, T-) are in the group iff their keys are equal (None: every pair)."""
    import oriented as O
    if group == 'Fvec':
        return tuple(w.count('1') % 2 for w in words(group, t))
    if group == 'F3vec':
        return tuple(O.weight(w) % 2 for w in words(group, t))
    return None


# ---------------------------------------------------------------------------------------------
# invariants
# ---------------------------------------------------------------------------------------------

def tait(group, tp, tm):
    """(number of Tait vertices, edges (u, w, side, crossing sign))."""
    import ftrees as F
    import oriented as O
    if ARITY[group] == 2:
        return F.n_leaves(tp), [(u, w, s, s) for u, w, s in F.tait_graph(tp, tm)]
    return (O.ternary_leaves(tp) + 1) // 2, O.tait_graph3(tp, tm)


def determinant(n, edges):
    import numpy as np
    L = np.zeros((n, n))
    for u, w, _, s in edges:
        L[u, u] += s
        L[w, w] += s
        L[u, w] -= s
        L[w, u] -= s
    return int(round(abs(np.linalg.det(L[1:, 1:])))) if n > 1 else 1


def pd_code(group, tp, tm):
    """PD code (Sage's convention), oriented as in oriented.py for vec{F} and vec{F}_3; None for a link."""
    import ftrees as F
    import oriented as O
    if group == 'Fvec':
        edges, comps = O.oriented_components(tp, tm)
    elif group == 'F3vec':
        edges, comps = O.oriented_components3(tp, tm)
    else:
        n, te = tait(group, tp, tm)
        medial, comps = F.link_components_of_graph(n, [e[:3] for e in te])
        assert [e[:2] for e in medial] == [e[:2] for e in te]
        edges = [(u, w, x) for u, w, _, x in te]
    if len(comps) != 1:
        return None
    return O._pd_of_components(edges, comps)


# ---------------------------------------------------------------------------------------------
# worker
# ---------------------------------------------------------------------------------------------

_REF = {}


def _ref(knot):
    if knot not in _REF:
        import snappy  # noqa: F401
        import spherogram
        from sage.all import KnotInfo
        import complete_check as C
        K = getattr(KnotInfo, 'K' + knot)
        ref = [list(map(int, c)) for c in K.link().pd_code()]
        E = spherogram.Link([[x - 1 for x in c] for c in ref]).exterior()
        hyp = C._geometric(E)
        _REF[knot] = (ref, float(E.volume()) if hyp else None, E, int(K.determinant()))
    return _REF[knot]


def check(task):
    """task = [group, knot, want, det, tops, bottoms]: the pairs (top, bottom) in the group (equal keys) that
    give the knot (and, with want, an oriented type in want), with their relations; counts of the filters."""
    import snappy  # noqa: F401
    import spherogram
    import complete_check as C
    import oriented as O
    group, knot, want, det, tops, bottoms = task
    ref, vk, Ek, _ = _ref(knot)
    hits, counts = [], {'pairs': 0, 'det': 0, 'knot': 0, 'volume': 0, 'snappy': 0}
    bykey = {}
    for b in bottoms:
        tb = tree(group, b)
        bykey.setdefault(key(group, tb), []).append((b, tb))
    pairs = ((top, tree(group, top), b, tb) for top in tops for b, tb in bykey.get(key(group, tree(group, top)), []))
    for top, tp, bottom, tm in pairs:
        counts['pairs'] += 1
        d = top + ' | ' + bottom
        if determinant(*tait(group, tp, tm)) != det:
            continue
        counts['det'] += 1
        pd = pd_code(group, tp, tm)
        if pd is None:
            continue
        counts['knot'] += 1
        S = spherogram.Link([[x - 1 for x in c] for c in pd])
        E = S.exterior()
        if vk is None or not C._geometric(E) or abs(float(E.volume()) - vk) > C.VOLUME_EPS:
            continue
        counts['volume'] += 1
        try:
            if want:
                rel = O.relation_to(pd, ref)
                if rel & set(want):
                    hits.append((d, sorted(rel)))
            elif E.is_isometric_to(Ek):
                hits.append((d, ['isometric']))
        except Exception:
            continue
        counts['snappy'] += 1
    return hits, counts


# ---------------------------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------------------------

def tasks_for(group, knot, want, det, diagrams, extra, k):
    """Tasks covering all the pairs (T+', T-') one step below (k > 0) or above (k < 0) the given diagrams (T+' a
    neighbour of T+, T-' of T-), CHUNK_TOPS tops per task."""
    ar = ARITY[group]
    out = []
    for d in diagrams:
        top, bottom = [x.strip() for x in d.split('|')]
        if key(group, tree(group, top)) is None:
            P = sorted(','.join(words(group, t)) for t in neighbours(tree(group, top), ar, k, extra))
            M = sorted(','.join(words(group, t)) for t in neighbours(tree(group, bottom), ar, k, extra))
            out += [[group, knot, want, det, P[i:i + CHUNK_TOPS], M] for i in range(0, len(P), CHUNK_TOPS)]
            continue
        # vec{F}, vec{F}_3: each task gets only the bottoms with the key of its tops (same pairs examined)
        P, M = {}, {}
        for t in neighbours(tree(group, top), ar, k, extra):
            P.setdefault(key(group, t), []).append(','.join(words(group, t)))
        for t in neighbours(tree(group, bottom), ar, k, extra):
            M.setdefault(key(group, t), []).append(','.join(words(group, t)))
        for kk in sorted(set(P) & set(M)):
            p, m = sorted(P[kk]), sorted(M[kk])
            step = max(1, CHUNK_TOPS * 20000 // max(len(m), 1))
            out += [[group, knot, want, det, p[i:i + step], m] for i in range(0, len(p), step)]
    return out


def run(job, pool, log):
    group, knot, want = job['group'], job['knot'], job.get('want')
    beam = job.get('beam', 50)
    _, _, _, det = _ref(knot)
    level = job['starts']
    n0 = len(level[0].split('|')[0].split(','))
    if ARITY[group] == 3:
        n0 = (n0 + 1) // 2
    for d in level:  # the starting diagrams must give the knot
        t, b = [x.strip() for x in d.split('|')]
        assert determinant(*tait(group, tree(group, t), tree(group, b))) == det, (knot, d)
    found = []
    for step in range(1, job['steps'] + 1):
        if job.get('ks'):  # explicit vertices removed per step (0: sideways moves at the same size)
            k = job['ks'][step - 1]
        else:
            k = -job['up'] if job.get('up') else STEP[group]
        n = n - k if step > 1 else n0 - k
        t0 = time.time()
        last = step == job['steps']
        tasks = tasks_for(group, knot, want if last else None, det, level, job.get('extra', 1), k)
        hits, counts = {}, {}
        for h, c in pool.map(check, tasks):
            for d, rel in h:
                hits[d] = rel
            for x, v in c.items():
                counts[x] = counts.get(x, 0) + v
        hits = sorted(hits.items())
        log('%s %s n = %d: %s, %d distinct hits (%.0f s)' % (job['name'], knot, n, counts, len(hits), time.time() - t0))
        for d, rel in hits:
            found.append({'name': job['name'], 'group': group, 'knot': knot, 'n': n, 'diagram': d,
                          'relation': ' '.join(rel), 'final': 'yes' if last else 'no'})
        if not hits:
            break
        level = [d for d, _ in hits][:beam]
    return found


def main():
    jobs = json.load(open(sys.argv[1]))
    processes = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    from identify_lib import RobustPool
    # DESCENT_OUT: another output file (e.g. one per machine when the jobs are split; append it to the main file)
    out = os.environ.get('DESCENT_OUT') or os.path.join(HERE, 'results', 'descent_search.csv')
    fields = ['name', 'group', 'knot', 'n', 'diagram', 'relation', 'final']
    new = not os.path.exists(out)

    def log(msg):
        print(time.strftime('%H:%M:%S'), msg, flush=True)
    done_file = os.path.join(HERE, 'tmp_check', 'descent', 'done_%s.txt' % os.path.basename(sys.argv[1]).split('.')[0])
    done = set(open(done_file).read().split()) if os.path.exists(done_file) else set()
    jobs = [j for j in jobs if j['name'] + ':' + j['knot'] not in done]  # resumed after a restart
    with RobustPool(processes) as pool:
        for job in jobs:
            found = run(job, pool, log)
            with open(out, 'a', newline='') as f:
                w = csv.DictWriter(f, fieldnames=fields)
                if new:
                    w.writeheader()
                    new = False
                w.writerows(found)
            with open(done_file, 'a') as f:
                f.write(job['name'] + ':' + job['knot'] + '\n')
            best = [r for r in found if r['final'] == 'yes']
            log('%s %s: %s' % (job['name'], job['knot'], ('FOUND n = %d' % best[0]['n']) if best else
                               'nothing at the last step (deepest n reached: %s)' % (min((r['n'] for r in found), default='-'))))


if __name__ == '__main__':
    main()
