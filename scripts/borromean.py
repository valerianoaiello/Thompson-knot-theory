"""
F-index and F_3-index of the Borromean rings (L6a4), Jones' problem in "On the construction of knots and links
from Thompson's groups" (2019), Section 7: "calculate the F3 and F2 indices of the Borromean rings".

usage (from F_index/):   sage -python scripts/borromean.py [nmax_F] [nmax_F3]      (defaults 8 and 6)

All the tree diagrams (no reduction) of size n are given to bin/iota_knots eval, which returns the number of
components and a PD code. A diagram can give the Borromean rings only if:
  1. its link has 3 components;
  2. all the pairwise linking numbers vanish (those of the Borromean rings do);
  3. its HOMFLY-PT polynomial, for the orientation of the PD code, equals that of the Borromean rings up to
     mirror image. This is a necessary condition for any orientation, because the HOMFLY-PT polynomial of the
     Borromean rings does not depend on the orientations of the components: it is invariant under the reversal
     of all the components, and a symmetry of the rings (three ellipses in the coordinate planes, rotation by pi
     about a coordinate axis) reverses two of them (for a general link with vanishing linking numbers the
     polynomial does depend on the orientations, e.g. L9a38 and L9a42);
  4. its exterior is isometric to that of L6a4 (SnapPy) by an isometry taking meridians to meridians on every
     cusp; such an isometry extends to a homeomorphism of S^3 taking one link to the other, so the diagram is
     the Borromean rings (up to mirror image).
The first n at which a diagram passes 1-3 is a lower bound, the first n at which one passes 4 is the index.
Output: results/borromean.md. With the defaults F is enumerated up to n = 8, where no diagram passes 1-3; the line
for n = 9 and the F-index are a fixed text (SWEENEY below), not computed here: the diagrams with 9 leaves are
those of D. Sweeney, and certify_borromean.py enumerates and certifies n = 9. With nmax_F >= 9 the script
enumerates n = 9 itself (about 2 million pairs of trees) and writes its own counts instead.
"""
import itertools
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root (the scripts are in scripts/)
sys.path.insert(0, os.path.join(HERE, 'scripts'))
import ftrees as F  # noqa: E402
import oriented as O  # noqa: E402

BIN = os.path.join(HERE, 'bin', 'iota_knots')


def ternary_trees(c):
    if c == 0:
        return [None]
    return [(l, m, r) for c1 in range(c) for c2 in range(c - c1)
            for l in ternary_trees(c1) for m in ternary_trees(c2) for r in ternary_trees(c - 1 - c1 - c2)]


def pd_from_tait(n, draw, signs):
    """PD code (Sage's convention) of the link with Tait graph `draw` (edges (u, w, side), drawn as in ftrees)
    and crossing types `signs` (+1: over strand SW-NE), for any number of components."""
    edges, comps = F.link_components_of_graph(n, draw)
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
    for x in range(len(edges)):
        s = entry[(x, 1 if signs[x] > 0 else 0)]
        pd.append([slot_label[(x, (s + k) % 4)] for k in range(4)])
    return len(comps), pd


_TREES = {}
_REF = []


def _filter(pd):
    """Steps 2 and 3: vanishing linking numbers and HOMFLY-PT polynomial of L6a4 up to mirror image."""
    import spherogram
    from sage.all import Link
    if not _REF:
        ref = spherogram.Link('L6a4').sage_link()
        _REF.extend([ref.homfly_polynomial(), ref.mirror_image().homfly_polynomial()])
    L = spherogram.Link([[x - 1 for x in c] for c in pd])
    M = L.linking_matrix()
    if any(M[i][j] for i in range(3) for j in range(3) if i != j):
        _STATS[0] += 1
        return False
    if Link(pd).homfly_polynomial() not in _REF:
        _STATS[1] += 1
        return False
    return True


_STATS = [0, 0]  # per process: diagrams rejected by the linking numbers, by the HOMFLY-PT polynomial


def _trees(group, n):
    if (group, n) not in _TREES:
        _TREES[(group, n)] = F.all_trees(n) if group == 'F' else ternary_trees(n - 1)
    return _TREES[(group, n)]


def _scan_top(task):
    """All diagrams (T_i, T) of size n: those whose link has 3 components, with their PD codes."""
    group, n, i = task
    trees = _trees(group, n)
    tp = trees[i]
    out, n3 = [], [0, 0, 0]
    _STATS[0] = _STATS[1] = 0
    for tm in trees:
        if group == 'F':
            E = F.tait_graph(tp, tm)
            draw, signs, nv = E, [e[2] for e in E], n
        else:
            E = O.tait_graph3(tp, tm)
            draw, signs, nv = [e[:3] for e in E], [e[3] for e in E], n
        if len(F.link_components_of_graph(nv, draw)[1]) != 3:
            continue
        n3[0] += 1
        _, pd = pd_from_tait(nv, draw, signs)
        ok = _filter(pd)
        n3[1], n3[2] = _STATS[0], _STATS[1]
        if not ok:
            continue
        if group == 'F':
            words = (','.join(F.leaf_words(tp)), ','.join(F.leaf_words(tm)))
        else:
            words = (','.join(O.ternary_words(tp)), ','.join(O.ternary_words(tm)))
        out.append((words[0], words[1], pd))
    return out, n3


def three_component_diagrams(group, n):
    """(top words, bottom words, pd) of the diagrams of size n whose link has 3 components."""
    from multiprocessing import Pool
    m = len(_trees(group, n))
    with Pool(os.cpu_count()) as pool:
        res = pool.map(_scan_top, [(group, n, i) for i in range(m)], chunksize=4)
    three = sum(r[1][0] for r in res)
    lk = sum(r[1][1] for r in res)
    hom = sum(r[1][2] for r in res)
    return m * m, three, three - lk, three - lk - hom, [x for r in res for x in r[0]]


INTRO = ('Jones\' problem (On the construction of knots and links from Thompson\'s groups, 2019, Section 7): '
         '"calculate the F3 and F2 indices of the Borromean rings". Script `borromean.py`: all the tree diagrams of '
         'size n (no reduction), filtered by number of components (3), linking numbers (all 0), HOMFLY-PT polynomial '
         'up to mirror image (for the Borromean rings it does not depend on the orientations of the components: it '
         'is invariant under the reversal of all of them, and a rotation by pi about a coordinate axis, for the '
         'rings drawn as three ellipses in the coordinate planes, reverses two of them), then a SnapPy isometry with '
         'L6a4 taking meridians to meridians (which extends to a homeomorphism of S^3 taking one link to the other). '
         'n = number of leaves for F, number of internal vertices + 1 for F_3; Jones counts internal vertices, '
         'i.e. n - 1.')
# Not computed by this script: with the default nmax_F = 8 the enumeration of F stops before the index, and the
# diagrams with 9 leaves are those of Sweeney's list, checked by the same test (and certified, together with the
# enumeration of n = 9, by certify_borromean.py: results/borromean_certified.md).
SWEENEY = ('- F, n = 9: the 64 diagrams with 9 leaves of D. Sweeney (github.com/sweeneyde/thompson_knots, folder '
           'Borromean/) are all certified to be the Borromean rings by the same test (e.g. '
           '`(((((oo)(oo))o)(o(oo)))o) / (o(((oo)(o((oo)o)))(oo)))` in Sweeney\'s notation).')
SWEENEY_INDEX = ('**F-index of the Borromean rings: 9 leaves** (8 internal vertices in Jones\' convention), in '
                 'agreement with Sweeney.')


def row_line(group, row):
    n, total, three, lk0, hom, borromean, witness = row
    return ('- %s, n = %d: %d diagrams, %d with 3 components, %d with vanishing linking numbers, '
            '%d with the HOMFLY-PT polynomial of L6a4, **%d Borromean rings**%s' % (
                group, n, total, three, lk0, hom, borromean, (' (e.g. `%s | %s`)' % witness) if witness else ''))


def report(rows):
    """The text of results/borromean.md. rows[group] = list of (n, diagrams, with 3 components, with vanishing
    linking numbers, with the HOMFLY-PT polynomial of L6a4, Borromean rings, witness or None), for increasing n,
    the last one being the first n with Borromean rings, if any."""
    lines = ['# F-index and F_3-index of the Borromean rings (L6a4)', '', INTRO, '', '## F', '']
    lines += [row_line('F', r) for r in rows['F']]
    last = rows['F'][-1] if rows['F'] else None
    if last and last[5]:
        lines += ['', '**F-index of the Borromean rings: %d leaves** (%d internal vertices in Jones\' convention); '
                  '%d binary tree diagrams with %d leaves give them.' % (last[0], last[0] - 1, last[5], last[0])]
    elif last and last[0] == 8:
        lines += [SWEENEY, '', SWEENEY_INDEX]
    else:
        lines += ['', 'F: not found up to n = %s.' % (last[0] if last else 1)]
    lines += ['', '## F_3', '']
    lines += [row_line('F3', r) for r in rows['F3']]
    last = rows['F3'][-1] if rows['F3'] else None
    if last and last[5]:
        lines += ['', '**F_3-index of the Borromean rings: n = %d** (%d internal vertices in Jones\' convention); '
                  '%d ternary tree diagrams with n = %d give them.' % (last[0], last[0] - 1, last[5], last[0])]
    else:
        lines += ['', 'F_3: not found up to n = %s.' % (last[0] if last else 1)]
    return '\n'.join(lines) + '\n'


def main():
    import snappy  # noqa: F401
    import spherogram
    nmax = {'F': int(sys.argv[1]) if len(sys.argv) > 1 else 8, 'F3': int(sys.argv[2]) if len(sys.argv) > 2 else 6}
    ref_E = spherogram.Link('L6a4').exterior()
    rows = {'F': [], 'F3': []}
    for group in ('F', 'F3'):
        for n in range(2, nmax[group] + 1):
            total, three, lk0, hom, cands = three_component_diagrams(group, n)
            borromean, witness = 0, None
            for a, b, pd in cands:
                L = spherogram.Link([[x - 1 for x in c] for c in pd])
                isos = L.exterior().is_isometric_to(ref_E, return_isometries=True) or []
                if any(all(int(m[1, 0]) == 0 and abs(int(m[0, 0])) == 1 for m in iso.cusp_maps()) for iso in isos):
                    borromean += 1
                    witness = witness or (a, b)
            rows[group].append((n, total, three, lk0, hom, borromean, witness))
            print(row_line(group, rows[group][-1]), flush=True)
            if borromean:
                break
    text = report(rows)
    open(os.path.join(HERE, 'results', 'borromean.md'), 'w').write(text)
    print('\n'.join(text.splitlines()[-1:]))


if __name__ == '__main__':
    main()
