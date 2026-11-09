"""
Aiello's Alexander theorem for vec{F} (V. Aiello, On the Alexander theorem for the oriented Thompson group
vec{F}, Algebr. Geom. Topol. 20 (2020) 429-438) turned into an algorithm: from an oriented knot K, an element
g = (T+, T-) of vec{F} with L(g) = K, and iota(g) in vec{F}_3. Used to get starting diagrams for
descent_search.py when no diagram of K is known in the group (e.g. 12a_1202 in vec{F}_3).

Steps (all the graphs are signed planar graphs, "semidual graphs" in the paper):
 1. special diagram of K: a diagram whose shaded (black) checkerboard surface is orientable and induces the
    orientation of K, i.e. at every crossing the black corners are the entrance-exit corners (Tait graph
    bipartite). Found by a random walk of Reidemeister moves (spherogram's backtrack/simplify) that
    minimises the number of crossings violating it (special_diagram).
 2. standard form (Jones, Lemma 5.3.6): the black regions on a line (positions 0..N), every crossing an arc
    above or below the line. Here: a closed curve through all the black regions that crosses no edge,
    found by a search over the white regions it passes through (standard_graph).
 3. the substitutions of the paper (Cases 1-4 and the gadget of the Lemma), until the graph is Thompson
    (Jones, Def. 5.3.9): every vertex but the leftmost has exactly one incoming arc above and one below,
    arcs above are positive and arcs below negative. Every substitution keeps the graph bipartite
    (thompson_graph).
 4. the trees (Jones, Lemma 4.1.4) and iota.
Every graph produced can be checked with SnapPy (check=True): the oriented knot must not change.

Conventions (as in ftrees / oriented): a standard graph is (n, edges) with vertices 0..n-1 on a line and
edges (u, w, side, sign), u < w, side = +1 above, -1 below, sign = crossing type (+1: with the black regions
u, w to the West and East of the crossing, the over strand goes SW-NE; Fig. 4 of the paper turned by 90
degrees). Parallel arcs on the same side are nested in the order of the edge list (earlier = inner).
Vertex colours: +1 / -1, the leftmost vertex +1; the knot is oriented as the boundary of the black surface
(counterclockwise around + regions), as in oriented.py.

usage (from F_index/): sage -python alexander.py KNOT [--seed S] [--minutes M]
"""
import random
import sys
import time

import ftrees as F
import oriented as O


# ---------------------------------------------------------------------------------------------
# standard graphs -> oriented PD codes (ftrees.medial_of_graph with nested parallel arcs)
# ---------------------------------------------------------------------------------------------

def relation(pd, ref, knot):
    """oriented.relation_to for hyperbolic knots; for the others (torus knots, invertible) the recognition in
    KnotInfo of descent_search.same_by_knotinfo, as {'same', 'reverse', 'mirror', 'mirror reverse'}."""
    import snappy  # noqa: F401
    import spherogram
    import complete_check as C
    import descent_search as D
    if C._geometric(spherogram.Link([[x - 1 for x in c] for c in ref]).exterior()):
        return O.relation_to(pd, ref)
    S = spherogram.Link([[int(x) - 1 for x in c] for c in pd])
    return {'same', 'reverse', 'mirror', 'mirror reverse'} if D.same_by_knotinfo(S, knot) else set()


def rotation(n, edges):
    """Counterclockwise order of the edges at each vertex, starting from East (see ftrees._ccw_rotation);
    ties (parallel arcs on the same side) by nesting, earlier edges inner."""
    rot = [[] for _ in range(n)]
    for v in range(n):
        keys = []
        for i, (a, b, side, _) in enumerate(edges):
            if v not in (a, b):
                continue
            o = a + b - v
            if side > 0:
                keys.append(((0, o, i) if o > v else (1, o, -i), i))
            else:
                keys.append(((2, -o, i) if o < v else (3, -o, -i), i))
        rot[v] = [i for _, i in sorted(keys)]
    return rot


def oriented_pd(n, edges, col):
    """PD code (Sage's convention) of the oriented link of the standard graph with vertex colours col."""
    rot = rotation(n, edges)
    corners, vert = [], []
    for v, order in enumerate(rot):
        d = len(order)
        for k in range(d):
            a, b = order[k], order[(k + 1) % d]
            corners.append(((a, 3 if edges[a][0] == v else 1), (b, 0 if edges[b][0] == v else 2)))
            vert.append(v)
    at = {}
    for c, (e1, e2) in enumerate(corners):
        at[e1] = (c, 0)
        at[e2] = (c, 1)
    seen = [False] * len(corners)
    comps = []
    for c0 in range(len(corners)):
        if seen[c0]:
            continue
        comp, c = [], c0
        end = 1 if col[vert[c0]] > 0 else 0
        while not seen[c]:
            assert (end == 1) == (col[vert[c]] > 0), 'incoherent orientation'
            seen[c] = True
            x, s = corners[c][end]
            comp.append((x, s, c))
            c, other = at[(x, (s + 2) % 4)]
            end = 1 - other
        comps.append(comp)
    return O._pd_of_components([(u, w, x) for u, w, _, x in edges], comps)


def colours(n, edges):
    return O.tait_colours_of_graph(n, [e[:3] for e in edges])


# ---------------------------------------------------------------------------------------------
# step 1: special diagram
# ---------------------------------------------------------------------------------------------

def checkerboard(L):
    """(faces, fid, col, io) for a spherogram link: col[face] in {0, 1} a checkerboard colouring, io[k] the
    colour of the entrance-exit corners of crossing k (corner j lies between the slots j and j + 1)."""
    faces = L.faces()
    fid = {}
    for i, f in enumerate(faces):
        for cs in f:
            fid[(id(cs.crossing), cs.strand_index)] = i
    adj = {i: [] for i in range(len(faces))}
    for c in L.crossings:
        for j in range(4):
            a, b = fid[(id(c), j)], fid[(id(c), (j + 1) % 4)]
            adj[a].append(b)
            adj[b].append(a)
    col, stack = {0: 0}, [0]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in col:
                col[w] = 1 - col[u]
                stack.append(w)
            else:
                assert col[w] != col[u]
    io = []
    for c in L.crossings:
        ins = {a for a, b in c.directions}
        cs = {col[fid[(id(c), j)]] for j in range(4) if (j in ins) != ((j + 1) % 4 in ins)}
        assert len(cs) == 1
        io.append(cs.pop())
    return faces, fid, col, io


def badness(L):
    io = checkerboard(L)[3]
    return min(io.count(0), io.count(1))


def special_diagram(L0, seed=1, seconds=300, cap=24, log=print):
    """A special diagram of the oriented link L0 (spherogram), by a random walk (simulated annealing on
    10 * badness + 0.3 * crossings); None if not found in time."""
    import math
    rnd = random.Random(seed)
    random.seed(seed)  # spherogram's moves use the global generator
    cur = L0.copy()
    score = lambda L: 10 * badness(L) + 0.3 * len(L.crossings)
    sc, t0, it = score(cur), time.time(), 0
    if badness(cur) == 0:
        return cur
    while time.time() - t0 < seconds:
        it += 1
        L = cur.copy()
        if rnd.random() < 0.15:
            L.simplify('basic')
        else:
            L.backtrack(steps=1, prob_type_1=0.15, prob_type_2=0.25)
        if not 0 < len(L.crossings) <= cap:
            continue
        s = score(L)
        if s <= sc or rnd.random() < math.exp((sc - s) / 2.0):
            cur, sc = L, s
            if badness(L) == 0:
                log('special diagram with %d crossings after %d steps' % (len(L.crossings), it))
                return L
    return None


# ---------------------------------------------------------------------------------------------
# step 2: standard form
# ---------------------------------------------------------------------------------------------

def _face_cycles(L, faces):
    """For each face, the cyclic (clockwise) list of (corner, knot edge after it)."""
    def ekey(c, j):
        cs = c.crossing_strands()[j]
        o = cs.opposite()
        return frozenset([(id(c), j), (id(o.crossing), o.strand_index)])
    out = []
    for f in faces:
        m = len(f)
        cyc = []
        for k in range(m):
            # the edge from corner h to the next corner h2 leaves h's crossing through slot j + 1 and
            # reaches h2's crossing through slot j (spherogram's clockwise faces)
            h, h2 = f[k], f[(k + 1) % m]
            j1 = (h.strand_index + 1) % 4
            o = h.crossing.crossing_strands()[j1].opposite()
            assert o.crossing is h2.crossing and o.strand_index == h2.strand_index
            cyc.append((h, ekey(h.crossing, j1)))
        out.append(cyc)
    return out


def standard_graph(L):
    """Standard graph (n, edges, col) of the special diagram L: black regions on a line, crossings as arcs.
    Raises ValueError if no curve without crossings through the black regions is found."""
    faces, fid, col, io = checkerboard(L)
    black = io[0]
    assert all(x == black for x in io), 'not special'
    cyc = _face_cycles(L, faces)
    B = [i for i in range(len(faces)) if col[i] == black]
    Wf = [i for i in range(len(faces)) if col[i] != black]
    # black vertex rotation (counterclockwise = reversed clockwise face order): items ('d', crossing id,
    # corner) and ('g', knot edge)
    rot = {}
    for f in B:
        items = []
        for h, e in cyc[f]:
            items += [('d', id(h.crossing), h.strand_index), ('g', e)]
        rot[f] = items[::-1]
    gap_vertex = {it[1]: f for f in B for it in rot[f] if it[0] == 'g'}
    white_of = {}
    wpos = {}
    for w in Wf:
        for k, (h, e) in enumerate(cyc[w]):
            white_of[e] = w
            wpos[(w, e)] = k
    gaps = {f: [it[1] for it in rot[f] if it[0] == 'g'] for f in B}

    def crosses(ch, chords):
        w, a, b = ch
        a, b = min(a, b), max(a, b)
        for w2, c, d in chords:
            if w2 != w:
                continue
            c, d = min(c, d), max(c, d)
            if (a < c < b < d) or (c < a < d < b):
                return True
        return False

    N = len(B)
    f0 = B[0]
    best = None

    def dfs(path, chords, visited):
        # path: list of (vertex, entry gap, exit gap); the last one has exit gap set
        nonlocal best
        if best is not None:
            return
        f, gin, gout = path[-1]
        w = white_of[gout]
        if len(path) == N:
            # close the curve: enter f0 through a gap of f0 in w, different from its exit gap
            for g in gaps[f0]:
                if g != path[0][2] and white_of[g] == w:
                    ch = (w, wpos[(w, gout)], wpos[(w, g)])
                    if not crosses(ch, chords):
                        best = [(path[0][0], g, path[0][2])] + path[1:]
                        return
            return
        for g in [e for (h, e) in cyc[w]]:
            f2 = gap_vertex[g]
            if f2 in visited or g == gout:
                continue
            ch = (w, wpos[(w, gout)], wpos[(w, g)])
            if crosses(ch, chords):
                continue
            for g2 in gaps[f2]:
                if g2 != g:
                    dfs(path + [(f2, g, g2)], chords + [ch], visited | {f2})
                    if best is not None:
                        return

    for g0 in gaps[f0]:
        dfs([(f0, None, g0)], [], {f0})
        if best is not None:
            break
    if best is None:
        raise ValueError('no standard drawing without crossings found')
    pos = {f: k for k, (f, _, _) in enumerate(best)}
    side = {}
    for f, gin, gout in best:
        items = rot[f]
        i0 = items.index(('g', gout))
        k, up = (i0 + 1) % len(items), True
        while True:
            it = items[k]
            if it == ('g', gin):
                up = False
            elif it[0] == 'd':
                side[(it[1], it[2])] = +1 if up else -1
            if k == i0:
                break
            k = (k + 1) % len(items)
    edges = []
    for c in L.crossings:
        js = [j for j in range(4) if col[fid[(id(c), j)]] == black]
        a, b = fid[(id(c), js[0])], fid[(id(c), js[1])]
        assert a != b, 'nugatory crossing'
        s1, s2 = side[(id(c), js[0])], side[(id(c), js[1])]
        assert s1 == s2, 'inconsistent sides'
        sign = +1 if js[0] % 2 == 0 else -1
        u, w = sorted((pos[a], pos[b]))
        edges.append((u, w, s1, sign))
    # nesting of parallel arcs on the same side: order them by their rotation at the left endpoint
    rot_pos = {}
    for f, gin, gout in best:
        items = rot[f]
        i0 = items.index(('g', gout))
        order = [items[(i0 + 1 + k) % len(items)] for k in range(len(items))]
        rot_pos.update({(it[1], it[2]): k for k, it in enumerate(order) if it[0] == 'd'})
    keyed = []
    for c, e in zip(L.crossings, edges):
        js = [j for j in range(4) if col[fid[(id(c), j)]] == black]
        a = fid[(id(c), js[0])] if pos[fid[(id(c), js[0])]] == e[0] else fid[(id(c), js[1])]
        j = js[0] if fid[(id(c), js[0])] == a else js[1]
        r = rot_pos[(id(c), j)]
        # at the left endpoint, counterclockwise from East: upper arcs inner first, lower arcs outer first
        keyed.append(((e[0], e[1], e[2], r if e[2] > 0 else -r), e))
    edges = [e for _, e in sorted(keyed)]
    n = N
    col_v = colours(n, edges)
    assert col_v is not None
    return n, edges, col_v


# ---------------------------------------------------------------------------------------------
# step 3: the substitutions of the paper
# ---------------------------------------------------------------------------------------------

class Graph:
    """Standard graph with named vertices (order = left to right) for the substitutions."""

    def __init__(self, n, edges, col):
        self.order = list(range(n))
        self.col = {v: col[v] for v in range(n)}
        self.edges = [[u, w, s, x] for u, w, s, x in edges]
        self.next = n

    def new(self, c):
        v = self.next
        self.next += 1
        self.col[v] = c
        return v

    def insert_before(self, w, vs):
        k = self.order.index(w)
        self.order[k:k] = vs

    def insert_after(self, v, vs):
        k = self.order.index(v) + 1
        self.order[k:k] = vs

    def add(self, u, w, side):
        """New arc (u left of w), sign by side; added innermost among its parallels."""
        self.edges.insert(0, [u, w, side, side])

    def lemma(self, v, w, flip=1):
        """The gadget of the Lemma between v and w (same colour, adjacent; four new vertices between them).
        flip = -1: reflected (arcs above <-> below)."""
        c = self.col[v]
        x = [self.new(-c), self.new(c), self.new(-c), self.new(c)]
        self.insert_after(v, x)
        U, D = flip, -flip
        for a, b in ((v, x[0]), (x[0], x[1]), (v, x[2]), (x[2], x[3]), (x[2], w)):
            self.add(a, b, U)
        for a, b in ((v, x[0]), (x[0], x[1]), (x[1], x[2]), (x[0], x[3]), (x[0], w)):
            self.add(a, b, D)

    def standard(self):
        """(n, edges, col) with positions."""
        p = {v: k for k, v in enumerate(self.order)}
        edges = []
        for u, w, s, x in self.edges:
            a, b = sorted((p[u], p[w]))
            edges.append((a, b, s, x))
        return len(self.order), edges, [self.col[v] for v in self.order]

    def incoming(self, w):
        p = {v: k for k, v in enumerate(self.order)}
        return [e for e in self.edges if (e[1] == w and p[e[0]] < p[w]) or (e[0] == w and p[e[1]] < p[w])]

    def left(self, w):
        return self.order[self.order.index(w) - 1]

    def source(self, e, w):
        return e[0] if e[1] == w else e[1]


def thompson_graph(n, edges, col, check=None, log=print):
    """Applies the substitutions until the graph is Thompson; check(n, edges, col) is called after each
    one (e.g. a SnapPy comparison). Returns (n, edges, col)."""
    G = Graph(n, edges, col)
    if G.col[G.order[0]] < 0:
        for v in G.col:
            G.col[v] = -G.col[v]
    steps = 0
    while True:
        done = True
        for w in G.order[1:]:
            ins = G.incoming(w)
            up = [e for e in ins if e[2] > 0]
            down = [e for e in ins if e[2] < 0]
            v = G.left(w)
            if not ins:  # Case 1
                if G.col[v] != G.col[w]:
                    G.add(v, w, +1)
                    G.add(v, w, -1)
                else:
                    G.lemma(v, w)
                case = 1
            elif len(ins) == 1:  # Case 2
                f = 1 if up else -1  # the missing incoming arc is on side -f
                if G.col[v] != G.col[w]:
                    y = G.new(G.col[v])
                    G.insert_before(w, [y])
                    G.lemma(v, y, f)
                else:
                    y = G.new(-G.col[v])
                    G.insert_before(w, [y])
                    G.add(v, y, +1)
                    G.add(v, y, -1)
                G.add(y, w, -f)
                case = 2
            elif len(up) > 1 or len(down) > 1:  # Case 3
                f = 1 if len(up) > 1 else -1
                same = up if f > 0 else down
                p = {u: k for k, u in enumerate(G.order)}
                e = min(same, key=lambda e: p[G.source(e, w)])  # the outermost one
                c = G.col[w]
                v2 = G.new(c)  # takes e and all the outgoing arcs of w
                G.insert_after(w, [v2])
                for e2 in G.edges:
                    if e2 is e or (w in e2[:2] and p[G.source(e2, w)] > p[w]):
                        if e2[0] == w:
                            e2[0] = v2
                        else:
                            e2[1] = v2
                y, z = G.new(c), G.new(-c)
                G.insert_before(v2, [y, z])
                G.lemma(w, y, f)
                G.add(w, z, f)
                G.add(y, z, -f)
                G.add(z, v2, -f)
                case = 3
            else:
                bad = [e for e in ins if e[2] != e[3]]
                if not bad:
                    continue
                e = bad[0]
                f = e[2]  # side of the bad arc
                c = G.col[v]
                if G.col[w] != c:  # first subcase
                    b, u1 = G.new(c), G.new(-c)
                    cc, u2 = G.new(-c), G.new(c)
                    d, u3 = G.new(c), G.new(-c)
                    e2, ff = G.new(-c), G.new(c)
                    G.insert_before(w, [b, u1, cc, u2, d, u3, e2, ff])
                    G.lemma(v, b, f)
                    G.lemma(u1, cc, f)
                    G.lemma(u2, d, f)
                    G.lemma(u3, e2, f)
                    for a, bb in ((b, u1), (u1, u2), (u2, u3), (u3, ff)):
                        G.add(a, bb, -f)
                    for a, bb in ((cc, u2), (d, u3), (e2, ff), (ff, w)):
                        G.add(a, bb, f)
                else:  # second subcase
                    pp, u1 = G.new(-c), G.new(c)
                    q, u2 = G.new(c), G.new(-c)
                    r, u3 = G.new(-c), G.new(c)
                    s, t = G.new(c), G.new(-c)
                    G.insert_before(w, [pp, u1, q, u2, r, u3, s, t])
                    G.add(v, pp, +1)
                    G.add(v, pp, -1)
                    G.lemma(u1, q, f)
                    G.lemma(u2, r, f)
                    G.lemma(u3, s, f)
                    for a, bb in ((pp, u1), (u1, u2), (u2, u3), (u3, t)):
                        G.add(a, bb, -f)
                    for a, bb in ((q, u2), (r, u3), (s, t), (t, w)):
                        G.add(a, bb, f)
                    u1 = u1
                # the bad arc now ends at u1 with the sign of its side
                if e[0] == w:
                    e[0] = u1
                else:
                    e[1] = u1
                e[3] = e[2]
                case = 4
            steps += 1
            done = False
            if check:
                check(*G.standard(), case)
            break
        if done:
            break
    n2, e2, c2 = G.standard()
    log('Thompson graph: %d vertices after %d substitutions' % (n2, steps))
    return n2, e2, c2


# ---------------------------------------------------------------------------------------------
# step 4: trees
# ---------------------------------------------------------------------------------------------

def trees(n, edges):
    """(T+, T-) of a Thompson graph (Jones, Lemma 4.1.4)."""
    pp, pm = [None] * n, [None] * n
    for u, w, s, x in edges:
        assert s == x
        par = pp if s > 0 else pm
        assert par[w] is None
        par[w] = u

    def build(par, off, m):
        if m == 1:
            return None
        k = max(j - off for j in range(off + 1, off + m) if par[j] == off)
        return (build(par, off, k), build(par, off + k, m - k))

    tp, tm = build(pp, 0, n), build(pm, 0, n)
    assert F.gamma_parents(tp)[1:] == pp[1:] and F.gamma_parents(tm)[1:] == pm[1:]
    return tp, tm


def main():
    import snappy  # noqa: F401
    import spherogram
    from sage.all import KnotInfo
    args = sys.argv[1:]
    knot = args[0]
    seed = int(args[args.index('--seed') + 1]) if '--seed' in args else 1
    minutes = float(args[args.index('--minutes') + 1]) if '--minutes' in args else 5
    ref = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + knot).link().pd_code()]
    L0 = spherogram.Link([[x - 1 for x in c] for c in ref])
    tries = int(args[args.index('--tries') + 1]) if '--tries' in args else 1
    best = None
    for k in range(tries):
        S = special_diagram(L0, seed + k, 60 * minutes)
        if S is None:
            print('seed %d: no special diagram found' % (seed + k))
            continue
        try:
            n, edges, col = standard_graph(S)
        except ValueError as e:
            print('seed %d: %s' % (seed + k, e))
            continue
        # the reflection in the line (sides swapped, signs kept: the same knot) changes which arcs need Case 4
        for flip in (1, -1):
            E = sorted(((u, w, flip * s, x) for u, w, s, x in edges), key=lambda t: (t[0], t[1], t[2]))
            C = colours(n, E)
            rel = relation(oriented_pd(n, E, C), ref, knot)
            if not rel:
                continue
            res = thompson_graph(n, E, C, log=lambda m: None)
            print('seed %d, flip %+d: special diagram %d crossings, standard graph %d vertices, %d arcs needing '
                  'Case 4 -> %d leaves' % (seed + k, flip, len(S.crossings), n, sum(1 for e in E if e[2] != e[3]),
                                           res[0]), flush=True)
            if best is None or res[0] < best[0][0]:
                best = (res, S, (n, E, C), rel)
                save(knot, ref, best, '--check' in args,
                     args[args.index('--out') + 1] if '--out' in args else knot)
    print('best: %d leaves' % best[0][0])


def save(knot, ref, best, check=False, stem=None):
    """Trees of the best construction, checked with SnapPy, written to tmp_check/alexander/<stem>.json
    (stem = knot by default; --out STEM keeps an earlier construction of the same knot)."""
    stem = stem or knot
    import json
    import os
    (n, edges, col), S, (n0, edges0, col0), rel = best
    if check:
        def chk(n, edges, col, case):
            r = relation(oriented_pd(n, edges, col), ref, knot)
            assert r == rel, (case, r)
        thompson_graph(n0, edges0, col0, chk, log=lambda m: None)
    tp, tm = trees(n, edges)
    assert O.tait_colours(tp, tm) is not None
    r = relation(O.oriented_pd_code(tp, tm), ref, knot)
    t3, b3 = O.iota(tp), O.iota(tm)
    r3 = relation(O.oriented_pd_code3(t3, b3), ref, knot)
    assert r and r3
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp_check', 'alexander')
    os.makedirs(out, exist_ok=True)
    json.dump({'knot': knot, 'special_pd': S.PD_code(), 'standard': [n0, edges0, col0], 'leaves': n,
               'Fvec': ','.join(F.leaf_words(tp)) + ' | ' + ','.join(F.leaf_words(tm)),
               'F3vec': ','.join(O.ternary_words(t3)) + ' | ' + ','.join(O.ternary_words(b3)),
               'relation': sorted(r), 'relation_F3vec': sorted(r3)},
              open(os.path.join(out, stem + '.json'), 'w'))
    print('  saved: vec{F} element with %d leaves (relation %s; in vec{F}_3: %s) -> tmp_check/alexander/%s.json'
          % (n, sorted(r), sorted(r3), stem), flush=True)

if __name__ == '__main__':
    main()
