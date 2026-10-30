"""
F-index and F_3-index of the Borromean rings (L6a4), Jones' problem in "On the construction of knots and links
from Thompson's groups" (2019), Section 7: "calculate the F3 and F2 indices of the Borromean rings".

usage (from F_index/):   sage -python borromean.py [nmax_F] [nmax_F3]      (defaults 10 and 7)

All the tree diagrams (no reduction) of size n are given to bin/iota_knots eval, which returns the number of
components and a PD code. A diagram can give the Borromean rings only if:
  1. its link has 3 components;
  2. all the pairwise linking numbers vanish (those of the Borromean rings do);
  3. its HOMFLY-PT polynomial equals that of the Borromean rings up to mirror image (with vanishing linking
     numbers the HOMFLY-PT polynomial does not depend on the orientations of the components);
  4. its exterior is isometric to that of L6a4 (SnapPy) by an isometry taking meridians to meridians on every
     cusp; such an isometry extends to a homeomorphism of S^3 taking one link to the other, so the diagram is
     the Borromean rings (up to mirror image).
The first n at which a diagram passes 1-3 is a lower bound, the first n at which one passes 4 is the index.
Output: results/borromean.md.
"""
import itertools
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
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


def main():
    import json
    import snappy
    import spherogram
    from sage.all import Link
    nmax = {'F': int(sys.argv[1]) if len(sys.argv) > 1 else 10, 'F3': int(sys.argv[2]) if len(sys.argv) > 2 else 7}
    ref = spherogram.Link('L6a4')
    ref_E = ref.exterior()
    ref_h = ref.sage_link().homfly_polynomial()
    ref_hm = ref.sage_link().mirror_image().homfly_polynomial()
    lines = ['# F-index and F_3-index of the Borromean rings (L6a4)', '',
             'Script `borromean.py`: all the tree diagrams of size n (no reduction), filtered by number of components '
             '(3), linking numbers (all 0), HOMFLY-PT polynomial up to mirror image, then SnapPy isometry with L6a4. '
             'n = number of leaves for F, number of internal vertices + 1 for F_3 (Jones counts internal vertices, '
             'i.e. n - 1).', '']
    result = {}
    for group in ('F', 'F3'):
        for n in range(2, nmax[group] + 1) if nmax[group] else []:
            total, three, lk0, hom, cands = three_component_diagrams(group, n)
            stats = dict(three=three, lk0=lk0, homfly=hom, borromean=0)
            witness = None
            for a, b, pd in cands:
                L = spherogram.Link([[x - 1 for x in c] for c in pd])
                isos = L.exterior().is_isometric_to(ref_E, return_isometries=True) or []
                if any(all(int(m[1, 0]) == 0 and abs(int(m[0, 0])) == 1 for m in iso.cusp_maps()) for iso in isos):
                    stats['borromean'] += 1
                    witness = witness or (a, b)
            lines.append('- %s, n = %d: %d diagrams, %d with 3 components, %d with vanishing linking numbers, '
                         '%d with the HOMFLY-PT polynomial of L6a4, **%d Borromean rings**%s' % (
                             group, n, total, stats['three'], stats['lk0'], stats['homfly'], stats['borromean'],
                             (' (e.g. `%s | %s`)' % witness) if witness else ''))
            print(lines[-1], flush=True)
            if stats['borromean']:
                result[group] = (n, witness)
                break
    lines += ['', 'F-index of the Borromean rings: %s leaves (Jones: %s internal vertices).' % (
        result['F'][0], result['F'][0] - 1) if 'F' in result else 'F: not found',
              'F_3-index of the Borromean rings: n = %s (Jones: %s internal vertices).' % (
        result['F3'][0], result['F3'][0] - 1) if 'F3' in result else 'F_3: not found']
    open(os.path.join(HERE, 'results', 'borromean.md'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[-2:]))


if __name__ == '__main__':
    main()
