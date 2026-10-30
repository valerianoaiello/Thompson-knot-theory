"""
Oriented knots and links from Jones' oriented subgroup vec{F} (Section 5 of the paper in biblio/).

For g = (T+, T-) in vec{F} the Tait graph Gamma(T+, T-) is 2-colourable; its vertices (the black regions
of the checkerboard colouring of L(g)) get the colours + and -, with the leftmost vertex 0 coloured +
(Convention 4.1). Each strand of the link diagram lies on the boundary of exactly one black region, and
it is oriented as the boundary of that region: counterclockwise (region on the left) if the region is +,
clockwise if it is -.

In ftrees.medial_of_graph every strand ("corner") is created at a vertex v of the Tait graph and goes
from an edge a to the next edge b counterclockwise around v, i.e. with v on its left. So a corner is
walked from its end 0 to its end 1 if v is +, and from 1 to 0 if v is -. The walk checks that these
directions are coherent along every component (this is exactly what 2-colourability guarantees).
"""
import ftrees as F


def tait_colours(tp, tm):
    """Colours (+1/-1) of the vertices of the Tait graph, vertex 0 = +1; None if not 2-colourable."""
    return tait_colours_of_graph(F.n_leaves(tp), F.tait_graph(tp, tm))


def tait_colours_of_graph(n, edges):
    """Colours (+1/-1) of the vertices 0..n-1 of a connected graph, vertex 0 = +1; None if not bipartite."""
    adj = [[] for _ in range(n)]
    for a, b, _ in edges:
        adj[a].append(b)
        adj[b].append(a)
    col = [0] * n
    col[0] = 1
    stack = [0]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if col[w] == 0:
                col[w] = -col[u]
                stack.append(w)
            elif col[w] == col[u]:
                return None
    return col


def corner_vertices(n, edges):
    """Tait vertex at which each corner of ftrees.medial_of_graph is created (same order)."""
    out = []
    for v, order in enumerate(F._ccw_rotation(n, edges)):
        out += [v] * len(order)
    return out


def oriented_components(tp, tm):
    """Like ftrees.link_components, but every component is walked along the orientation given by the
    colouring. Raises ValueError if (T+, T-) is not in vec{F}, AssertionError if the orientation is not
    coherent (it never should be)."""
    return oriented_components_of_graph(F.n_leaves(tp), F.tait_graph(tp, tm), tait_colours(tp, tm))


def oriented_components_of_graph(n, tait_edges, col):
    """oriented_components for a Tait graph drawn as in ftrees (vertices on a line, arcs above for sign +1
    and below for sign -1) with the colours col of its vertices."""
    if col is None:
        raise ValueError('not 2-colourable')
    edges, corners = F.medial_of_graph(n, tait_edges)
    vert = corner_vertices(n, edges)
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
        c = c0
        end = 1 if col[vert[c0]] > 0 else 0  # walk along corner c towards its end `end`
        while not seen[c]:
            assert (end == 1) == (col[vert[c]] > 0), 'incoherent orientation'
            seen[c] = True
            x, s = corners[c][end]
            comp.append((x, s, c))
            c, other = at[(x, (s + 2) % 4)]
            end = 1 - other
        comps.append(comp)
    return edges, comps


def oriented_pd_code(tp, tm):
    """PD code (Sage's convention) of the oriented link L(g), g = (T+, T-) in vec{F}: strands are numbered
    along the orientation given by the colouring."""
    return _pd_of_components(*oriented_components(tp, tm))


def _pd_of_components(edges, comps):
    if not edges:
        return []
    label, nxt = {}, 1
    for comp in comps:
        for (_, _, c) in comp:
            label[c] = nxt
            nxt += 1
    slot_label, entry = {}, {}
    for comp in comps:
        m = len(comp)
        for i, (x, s, c) in enumerate(comp):
            slot_label[(x, s)] = label[c]
            slot_label[(x, (s + 2) % 4)] = label[comp[(i + 1) % m][2]]
            entry[(x, s % 2)] = s
    pd = []
    for x, (_, _, sign) in enumerate(edges):
        under_parity = 1 if sign > 0 else 0  # positive edges: over strand is SW-NE (slots 0, 2)
        s = entry[(x, under_parity)]
        pd.append([slot_label[(x, (s + k) % 4)] for k in range(4)])
    return pd


# ---------------------------------------------------------------------------------------------
# vec{F}_3 (Aiello-Nagnibeda, J. Algebra Appl. 21 (2022) 2250139)
# ---------------------------------------------------------------------------------------------
# Ternary trees are nested 3-tuples (left, middle, right), a leaf is None; leaf addresses use 0, 1, 2 for
# left, middle, right. With 2c + 1 leaves the gaps between consecutive leaves (and the two outer ones) are
# numbered 0..2c + 1; the even gaps are the black regions, i.e. the c + 1 vertices of the Tait graph
# (vertex v = gap 2v). Every internal vertex of T+ (resp. T-) is a crossing, an arc above (resp. below)
# the line between the two black gaps around it, drawn as in ftrees.
# Colours: the vertex to the left of leaf 2v gets the parity of the weight c+(2v) (or c-(2v), the same in
# vec{F}_3): even = +, so the leftmost vertex (leaf 0..0, weight 0) is +. Strands are oriented as for
# vec{F}: counterclockwise around + regions, clockwise around - regions.

def ternary_from_words(words):
    """Ternary tree with the given leaf addresses (digits 0, 1, 2), from left to right."""
    def rec(ws, depth):
        if ws == [''] or (len(ws) == 1 and len(ws[0]) == depth):
            return None
        return tuple(rec([w for w in ws if w[depth] == d], depth + 1) for d in '012')
    words = ['' if w == '0' and len(words) == 1 else w for w in words]
    return rec(words, 0)


def ternary_words(t, prefix=''):
    if t is None:
        return [prefix or '0']
    return [w for i, s in enumerate(t) for w in ternary_words(s, prefix + str(i))]


def ternary_leaves(t):
    return 1 if t is None else sum(ternary_leaves(s) for s in t)


def weight(word):
    """c of Definition 3: middle edges + right edges in odd words + left edges in even words (the words
    being the pieces between middle edges, the first one odd)."""
    parts = word.split('1')
    return word.count('1') + sum(p.count('2') if k % 2 == 0 else p.count('0') for k, p in enumerate(parts))


def tait_graph3(tp, tm):
    """Edges (u, w, side, sign) of the Tait graph of (T+, T-) in F_3, u < w; side = +1 (drawn above the
    line) for T+ and -1 for T-. sign is the crossing type in the convention of oriented_pd_code (over strand
    SW-NE iff +1): equal to side at a vertex starting at an even leaf (always the case in iota(F)), the
    opposite at an odd one."""
    out = []

    def rec(t, a, sign):
        if t is None:
            return
        sizes = [ternary_leaves(x) for x in t]
        gaps = [a, a + sizes[0], a + sizes[0] + sizes[1], a + sum(sizes)]
        u, w = [g // 2 for g in gaps if g % 2 == 0]
        # a vertex starting at an odd leaf has its black regions in the other two quadrants (between left
        # and middle, and outside the right subtree): the crossing has the opposite sign w.r.t. its edge
        out.append((u, w, sign, sign if a % 2 == 0 else -sign))
        for x, b in zip(t, gaps):
            rec(x, b, sign)

    rec(tp, 0, +1)
    rec(tm, 0, -1)
    return out


def tait_colours3(tp, tm):
    """Colours of the c + 1 Tait vertices from the weights c+- (vertex v = left of leaf 2v); None if
    (T+, T-) is not in vec{F}_3."""
    cp = [weight(w) % 2 for w in ternary_words(tp)]
    cm = [weight(w) % 2 for w in ternary_words(tm)]
    if cp != cm:
        return None
    return [1 if cp[2 * v] == 0 else -1 for v in range((len(cp) + 1) // 2)]


def oriented_components3(tp, tm):
    col = tait_colours3(tp, tm)
    if col is None:
        raise ValueError('not in vec{F}_3')
    n = len(col)
    edges = tait_graph3(tp, tm)
    draw = [e[:3] for e in edges]
    assert col == tait_colours_of_graph(n, draw), 'c+- is not the 2-colouring of the Tait graph'
    medial_edges, comps = oriented_components_of_graph(n, draw, col)
    assert [e[:2] for e in medial_edges] == [e[:2] for e in edges]
    return [(u, w, x) for u, w, _, x in edges], comps


def oriented_pd_code3(tp, tm):
    """PD code (Sage's convention) of the oriented link L(g), g = (T+, T-) in vec{F}_3."""
    return _pd_of_components(*oriented_components3(tp, tm))


def iota(t):
    """The embedding of binary trees in ternary trees (a caret becomes a ternary caret with an empty
    middle leaf)."""
    return None if t is None else (iota(t[0]), None, iota(t[1]))


# ---------------------------------------------------------------------------------------------
# oriented knot type relative to a reference knot (needs snappy / spherogram)
# ---------------------------------------------------------------------------------------------

def relation_to(pd, ref_pd):
    """How the oriented knot with PD code `pd` is related to the oriented knot `ref_pd` (both in Sage's
    convention), from the isometries of the complements and their action on (meridian, longitude):
        'same'            orientation-preserving homeomorphism of S^3 preserving the knot orientation
        'reverse'         orientation-preserving, knot orientation reversed
        'mirror'          orientation-reversing, knot orientation preserved
        'mirror reverse'  orientation-reversing, knot orientation reversed
    Returns the set of relations realized (empty if the complements are not isometric). Hyperbolic knots
    only (for them the complement determines the knot up to these four operations)."""
    import snappy  # noqa: F401  (needed by spherogram for exteriors)
    import spherogram
    shift = lambda p: [[int(x) - 1 for x in c] for c in p]  # spherogram is 0-based
    E = spherogram.Link(shift(pd)).exterior()
    R = spherogram.Link(shift(ref_pd)).exterior()
    out = set()
    isos = E.is_isometric_to(R, return_isometries=True)
    for iso in isos or []:
        M = iso.cusp_maps()[0]
        # for knot complements the map is diagonal: meridian -> +-meridian, longitude -> +-longitude
        assert M[0, 1] == 0 and M[1, 0] == 0, M
        m_sign, l_sign = int(M[0, 0]), int(M[1, 1])
        if m_sign == l_sign:
            out.add('same' if m_sign == 1 else 'reverse')
        else:
            out.add('mirror' if l_sign == 1 else 'mirror reverse')
    return out
