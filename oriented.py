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
    n = F.n_leaves(tp)
    adj = [[] for _ in range(n)]
    for a, b, _ in F.tait_graph(tp, tm):
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
    col = tait_colours(tp, tm)
    if col is None:
        raise ValueError('not in vec{F}')
    n = F.n_leaves(tp)
    edges, corners = F.medial_of_graph(n, F.tait_graph(tp, tm))
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
    edges, comps = oriented_components(tp, tm)
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
