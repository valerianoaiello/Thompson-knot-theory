"""
Numerical check of the parity theorem: for g = (T+, T-) in vec{F} with n leaves, the link L(g) has a number
of components congruent to n mod 2 (so knots only occur for odd n).

usage (from F_index/):   python3 tests/check_parity.py [nmax]      (default 9; plain Python, parallel)

Proof being checked (see results/parity_theorem.md):
  (a) Gamma = Gamma(T+, T-) is a connected plane graph with n vertices and 2(n-1) edges (each tree gives a
      spanning tree), hence n faces by Euler's formula.
  (b) c(L) = dim ker over GF(2) of the Laplacian of Gamma, and also of its dual Gamma* (Rosenstiehl-Read:
      the number of left-right cycles of a connected plane graph is dim(bicycle space) + 1, and the
      bicycle space of a connected graph is ker(Laplacian mod 2) / <all-ones>).
  (c) g in vec{F} iff Gamma is bipartite (Jones; the leaf-parity criterion); then every face of Gamma has even
      length, i.e. Gamma* is Eulerian, so the Laplacian of Gamma* mod 2 has zero diagonal: it is an
      alternating matrix, of even rank. Hence c = (number of faces) - rank = n - even = n mod 2.
Checked here: (a), the face count, both equalities in (b) for every tree diagram of F, (c) for every one.
"""
import os
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ftrees as F  # noqa: E402


def rank_gf2(rows):
    """Rank over GF(2) of a list of row bitmasks."""
    basis = []  # rows with distinct leading bits
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r)
    return len(basis)


def laplacian_nullity(nv, edges):
    """dim ker of the Laplacian mod 2 of a multigraph (loops allowed) with vertices 0..nv-1."""
    rows = [0] * nv
    for u, w in edges:
        if u != w:
            rows[u] ^= (1 << u) ^ (1 << w)
            rows[w] ^= (1 << u) ^ (1 << w)
    return nv - rank_gf2(rows), rows


def faces(n, edges):
    """Faces of the plane embedding of Gamma: list of faces, each a list of edge indices (with repetition)."""
    rot = F._ccw_rotation(n, edges)
    pos = {(v, e): k for v in range(n) for k, e in enumerate(rot[v])}
    seen, out = set(), []
    for v0 in range(n):
        for e0 in rot[v0]:
            if (v0, e0) in seen:
                continue
            face, v, e = [], v0, e0
            while (v, e) not in seen:  # dart leaving v along e
                seen.add((v, e))
                face.append(e)
                w = edges[e][0] + edges[e][1] - v
                d = len(rot[w])
                e = rot[w][(pos[(w, e)] - 1) % d]  # next edge clockwise at w
                v = w
            out.append(face)
    return out


def bipartite(n, edges):
    col = [None] * n
    col[0] = 0
    stack = [0]
    adj = [[] for _ in range(n)]
    for u, w, _ in edges:
        adj[u].append(w)
        adj[w].append(u)
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if col[w] is None:
                col[w] = 1 - col[v]
                stack.append(w)
            elif col[w] == col[v]:
                return False
    return all(c is not None for c in col)


def leaf_parity(t):
    return tuple(w.count('1') % 2 for w in F.leaf_words(t))


def check_top(task):
    """All diagrams (tp, tm) with tp fixed. Returns counters and the failures."""
    n, i = task
    trees = F.all_trees(n)
    tp = trees[i]
    st = dict(pairs=0, vec=0, vec_knots=0, failures=[])
    for tm in trees:
        edges = F.tait_graph(tp, tm)
        c = len(F.link_components_of_graph(n, edges)[1])
        ok = len(edges) == 2 * (n - 1)
        null_g, _ = laplacian_nullity(n, [(u, w) for u, w, _ in edges])
        fs = faces(n, edges)
        ok &= len(fs) == n  # Euler: n - 2(n-1) + n = 2
        side = {}
        for f, face in enumerate(fs):
            for e in face:
                side.setdefault(e, []).append(f)
        dual = [tuple(side[e]) for e in range(len(edges))]
        ok &= all(len(s) == 2 for s in dual)
        null_d, rows_d = laplacian_nullity(len(fs), dual)
        ok &= c == null_g == null_d
        in_vec = leaf_parity(tp) == leaf_parity(tm)
        ok &= in_vec == bipartite(n, edges)
        if in_vec:
            st['vec'] += 1
            st['vec_knots'] += c == 1
            ok &= all(len(face) % 2 == 0 for face in fs)          # Gamma* Eulerian
            ok &= all(not (rows_d[f] >> f) & 1 for f in range(n))  # zero diagonal
            ok &= c % 2 == n % 2
        st['pairs'] += 1
        if not ok:
            st['failures'].append((F.leaf_words(tp), F.leaf_words(tm)))
    return st


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    bad = 0
    with Pool(os.cpu_count()) as pool:
        for n in range(2, nmax + 1):
            tot = dict(pairs=0, vec=0, vec_knots=0, failures=[])
            for st in pool.imap_unordered(check_top, [(n, i) for i in range(len(F.all_trees(n)))]):
                for k in tot:
                    tot[k] += st[k]
            bad += len(tot['failures'])
            print('n = %2d: %8d diagrams of F, %6d in vec{F} (%d knots): %s' % (
                n, tot['pairs'], tot['vec'], tot['vec_knots'],
                'ok' if not tot['failures'] else 'FAILED on %s' % tot['failures'][:3]), flush=True)
    print('all checks passed' if not bad else '%d FAILURES' % bad)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
