"""
Reference (slow, readable) implementation of Jones' construction of
unoriented links from binary tree diagrams (elements of Thompson's group F).

Used to validate the fast C++ enumerator in src/fknots.cpp.

Conventions
-----------
* A binary tree is a nested tuple: a leaf is None, an internal vertex is (left, right).
* A tree diagram is a pair (T_plus, T_minus) with the same number n of leaves;
  T_plus is the top tree, T_minus the (reflected) bottom tree.
* Tait graph Gamma(T_plus, T_minus): vertices 0..n-1, where vertex 0 is the region to the
  left of leaf 0 and vertex j >= 1 is the gap between leaves j-1 and j.
  Every internal vertex of a tree whose left subtree covers leaves [a, j-1] gives an edge (a, j):
  it is the Tait edge crossing the "West-North" (resp. "West-South") edge of the tree.
  Edges coming from T_plus live in the upper half-plane and are positive,
  edges coming from T_minus live in the lower half-plane and are negative (Remark 2.1 of biblio/).
* L(T_plus, T_minus) is the link whose Tait graph is Gamma. Everything here is only defined
  up to mirror image, which is all we need for the F-index.
"""

N = None  # a leaf


# ----------------------------------------------------------------------------------------
# binary trees
# ----------------------------------------------------------------------------------------

def n_leaves(t):
    return 1 if t is None else n_leaves(t[0]) + n_leaves(t[1])


def leaf_words(t, prefix=''):
    """Addresses of the leaves (0 = left, 1 = right), as in the old ternary code."""
    if t is None:
        return [prefix]
    return leaf_words(t[0], prefix + '0') + leaf_words(t[1], prefix + '1')


def from_leaf_words(words):
    """Inverse of leaf_words."""
    if words == ['']:
        return None
    left = [w[1:] for w in words if w[0] == '0']
    right = [w[1:] for w in words if w[0] == '1']
    return (from_leaf_words(left), from_leaf_words(right))


def flip(t):
    """Reflection about a vertical line (the flip automorphism of F)."""
    return None if t is None else (flip(t[1]), flip(t[0]))


def all_trees(n):
    if n == 1:
        return [None]
    return [(l, r) for k in range(1, n) for l in all_trees(k) for r in all_trees(n - k)]


def gamma_parents(t):
    """parent[j] = a for each Tait edge (a, j), j = 1..n-1 (parent[0] is unused)."""
    n = n_leaves(t)
    parent = [None] * n

    def rec(s, off):
        if s is None:
            return
        k = n_leaves(s[0])
        parent[off + k] = off
        rec(s[0], off)
        rec(s[1], off + k)

    rec(t, 0)
    return parent


def internal_intervals(t):
    """Leaf intervals [l, r] spanned by the internal vertices other than the root."""
    out = set()

    def rec(s, off, is_root):
        if s is None:
            return
        k, m = n_leaves(s[0]), n_leaves(s)
        if not is_root:
            out.add((off, off + m - 1))
        rec(s[0], off, False)
        rec(s[1], off + k, False)

    rec(t, 0, True)
    return out


def is_prime_diagram(tp, tm):
    """
    False iff (tp, tm) is obtained by gluing a tree diagram with >= 2 leaves into a pair of
    corresponding leaves of another tree diagram with >= 2 leaves, i.e. iff some non-root
    internal vertex of tp and some non-root internal vertex of tm span the same leaves.
    Non-reduced diagrams (pairs of opposing carets) are in particular not prime.
    """
    return not (internal_intervals(tp) & internal_intervals(tm))


# ----------------------------------------------------------------------------------------
# link diagram
# ----------------------------------------------------------------------------------------

def tait_graph(tp, tm):
    """List of edges (u, w, sign) with u < w; upper edges first."""
    n = n_leaves(tp)
    assert n == n_leaves(tm)
    pp, pm = gamma_parents(tp), gamma_parents(tm)
    return [(pp[j], j, +1) for j in range(1, n)] + [(pm[j], j, -1) for j in range(1, n)]


def _ccw_rotation(n, edges):
    """Counterclockwise cyclic order of the edges around each vertex, starting from East.

    Arcs are nested semicircles, so going counterclockwise from East one meets:
    upper arcs to the right (nearest first), upper arcs to the left (farthest first),
    lower arcs to the left (nearest first), lower arcs to the right (farthest first)."""
    rot = []
    for v in range(n):
        def other(e):
            return edges[e][0] + edges[e][1] - v
        up = sorted((e for e, (a, b, s) in enumerate(edges) if s > 0 and v in (a, b)),
                    key=lambda e: (other(e) < v, other(e)))
        down = sorted((e for e, (a, b, s) in enumerate(edges) if s < 0 and v in (a, b)),
                      key=lambda e: (other(e) > v, -other(e)))
        rot.append(up + down)
    return rot


def medial(tp, tm):
    return medial_of_graph(n_leaves(tp), tait_graph(tp, tm))


def medial_of_graph(n, edges):
    """
    Medial graph of Gamma. Each Tait edge e = (u, w) is a crossing whose four slots, in
    counterclockwise order with e drawn horizontally and u on the West, are
        0 = SW (u side), 1 = SE (w side), 2 = NE (w side), 3 = NW (u side).
    Each corner between consecutive edges a -> b (counterclockwise) at a vertex v is a strand of
    the medial graph, with one end at crossing a and one at crossing b.
    Returns (edges, corners) where corners[c] = ((crossing, slot), (crossing, slot)).
    """
    corners = []
    for v, order in enumerate(_ccw_rotation(n, edges)):
        d = len(order)
        for k in range(d):
            a, b = order[k], order[(k + 1) % d]
            end_a = (a, 3 if edges[a][0] == v else 1)  # counterclockwise side of a at v
            end_b = (b, 0 if edges[b][0] == v else 2)  # clockwise side of b at v
            corners.append((end_a, end_b))
    return edges, corners


def link_components(tp, tm):
    return link_components_of_graph(n_leaves(tp), tait_graph(tp, tm))


def link_components_of_graph(n, edges):
    """List of components; each is the list of (crossing, entry_slot, corner) met along it."""
    edges, corners = medial_of_graph(n, edges)
    at = {}
    for c, (e1, e2) in enumerate(corners):
        at[e1] = (c, 0)
        at[e2] = (c, 1)
    seen = [False] * len(corners)
    comps = []
    for c0 in range(len(corners)):
        if seen[c0]:
            continue
        comp = []
        c, end = c0, 1  # walk along corner c towards its end `end`
        while not seen[c]:
            seen[c] = True
            x, s = corners[c][end]
            comp.append((x, s, c))
            c, other = at[(x, (s + 2) % 4)]
            end = 1 - other
        comps.append(comp)
    return edges, comps


def number_of_components(tp, tm):
    return len(link_components(tp, tm)[1])


def pd_code(tp, tm):
    return pd_code_of_graph(n_leaves(tp), tait_graph(tp, tm))


def pd_code_of_graph(n, edges):
    """
    PD code in Sage's convention (each crossing lists its four strands counterclockwise,
    starting from the incoming under-strand). Strands are numbered along the orientation
    given by the walk, so the result is a valid input for sage's Link().
    """
    edges, comps = link_components_of_graph(n, edges)
    if not edges:
        return []
    label = {}  # corner -> label
    nxt = 1
    for comp in comps:
        for (_, _, c) in comp:
            label[c] = nxt
            nxt += 1
    slot_label = {}
    entry = {}  # (crossing, slot pair parity) -> entry slot
    for comp in comps:
        m = len(comp)
        for i, (x, s, c) in enumerate(comp):
            c_out = comp[(i + 1) % m][2]
            slot_label[(x, s)] = label[c]
            slot_label[(x, (s + 2) % 4)] = label[c_out]
            entry[(x, s % 2)] = s
    pd = []
    for x, (_, _, sign) in enumerate(edges):
        under_parity = 1 if sign > 0 else 0  # positive edges: over strand is SW-NE (slots 0, 2)
        s = entry[(x, under_parity)]
        pd.append([slot_label[(x, (s + k) % 4)] for k in range(4)])
    return pd


# ----------------------------------------------------------------------------------------
# Thompson's group F (only used for tests / examples)
# ----------------------------------------------------------------------------------------

def _union(s, t):
    if s is None:
        return t
    if t is None:
        return s
    return (_union(s[0], t[0]), _union(s[1], t[1]))


def _subtrees_at_leaves(q, u):
    if q is None:
        return [u]
    return _subtrees_at_leaves(q[0], u[0]) + _subtrees_at_leaves(q[1], u[1])


def _graft(p, subs):
    it = iter(subs)

    def rec(s):
        return next(it) if s is None else (rec(s[0]), rec(s[1]))

    return rec(p)


def _carets(t):
    """Indices i such that leaves i, i+1 form a caret."""
    out = []

    def rec(s, off):
        if s is None:
            return
        if s == (None, None):
            out.append(off)
            return
        rec(s[0], off)
        rec(s[1], off + n_leaves(s[0]))

    rec(t, 0)
    return out


def _collapse(t, i):
    def rec(s, off):
        if s is None:
            return s
        if s == (None, None) and off == i:
            return None
        return (rec(s[0], off), rec(s[1], off + n_leaves(s[0])))

    return rec(t, 0)


def reduce_diagram(g):
    tp, tm = g
    while True:
        common = set(_carets(tp)) & set(_carets(tm))
        if not common:
            return (tp, tm)
        i = min(common)
        tp, tm = _collapse(tp, i), _collapse(tm, i)


def multiply(g, h):
    """(T+, T) . (T, T-) = (T+, T-), as in the biblio paper."""
    u = _union(g[1], h[0])
    top = _graft(g[0], _subtrees_at_leaves(g[1], u))
    bottom = _graft(h[1], _subtrees_at_leaves(h[0], u))
    return reduce_diagram((top, bottom))


def inverse(g):
    return (g[1], g[0])


IDENTITY = (None, None)


def x(k):
    """Generator x_k = phi_R^k(x_0)."""
    tp, tm = ((N, N), N), (N, (N, N))
    for _ in range(k):
        tp, tm = (N, tp), (N, tm)
    return (tp, tm)


def word(*letters):
    """word(0, 2, 2, -5) = x_0 x_2 x_2 x_5^{-1}; use '-0' for x_0^{-1}."""
    g = IDENTITY
    for a in letters:
        if isinstance(a, str):
            gen = inverse(x(int(a[1:]))) if a.startswith('-') else x(int(a))
        else:
            gen = inverse(x(-a)) if a < 0 else x(a)
        g = multiply(g, gen)
    return g
