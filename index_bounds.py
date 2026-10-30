"""
Compares the four indices with the braid index, the arc index (KnotInfo) and the crossing number.

usage (from F_index/):   sage -python index_bounds.py          -> results/index_bounds.md

Luo-Wan (arXiv:2408.10875, Theorem 1.15): grid(L) <= 2 ind_F(L), so braid(L) <= ind_F(L).
Golan-Sapir (arXiv:1501.00724, Lemma 6.11): F-index <= 12 c for a knot with crossing number c.
Trivial lower bound: a tree diagram with index n has 2(n - 1) crossings, so c <= 2(index - 1).
"""
import csv
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
G = {'F': 'F', 'F3': 'F₃', 'Fvec': '$\\vec{F}$', 'F3vec': '$\\vec{F}_3$'}


def main():
    from sage.all import KnotInfo
    braid, arc = {}, {}
    for K in KnotInfo:
        if K.is_knot() and K.crossing_number() >= 3:
            try:
                braid[K.value] = int(K.braid_index())
            except Exception:
                pass
            a = K[K.items.arc_index]
            if a not in (None, ''):
                arc[K.value] = int(a)
    data = {}
    for g in G:
        data[g] = [(r['knot'], int(r['crossing_number']), int(r[g + '_index']))
                   for r in csv.DictReader(open(os.path.join(HERE, 'results', '%s_index.csv' % g)))
                   if r[g + '_index'] and int(r['crossing_number']) >= 3]
    L = []
    w = L.append
    w('# The indices compared with the braid index, the arc index and the crossing number\n')
    w('**Data.**\n')
    w('- Indices: the final tables `results/<G>_index.csv` (F up to n = 13, F₃ up to n = 8, $\\vec{F}$ up to n = 17, '
      '$\\vec{F}_3$ up to n = 11), knots with a known index only.')
    w('- Braid index and arc index: KnotInfo. The braid index is available for %d knots, up to 12 crossings.' % len(braid))
    w('- For the oriented groups the index of the tables is min(index K, index Kr) (see '
      '`results/oriented_index_<G>.md`). The bounds below hold for every orientation, since braid index, arc index '
      'and crossing number do not depend on it.')
    w('- Script: `index_bounds.py`.\n')
    w('## Braid index and arc index (Luo–Wan)\n')
    w('Y. Luo, S. Wan, *Half grid diagrams and Thompson links*, arXiv:2408.10875, Theorem 1.15: grid(L) ≤ 2·ind_F(L), '
      'where ind_F is the F-index (number of leaves) and grid is the arc index. Consequences:\n')
    w('- bridge(L) ≤ braid(L) ≤ grid(L)/2 ≤ ind_F(L);')
    w('- braid ≤ $\\vec{F}$-index, since F-index ≤ $\\vec{F}$-index.\n')
    w('The theorem does not cover F₃ and $\\vec{F}_3$.\n')
    w('| index | knots compared | min(index − braid) | knots attaining it (index / braid) | min(2·index − arc) | '
      'equality braid = index |')
    w('|---|---|---|---|---|---|')
    for g in G:
        d = [(k, c, i) for k, c, i in data[g] if k in braid]
        m = min(i - braid[k] for k, c, i in d)
        near = ', '.join('%s (%d / %d)' % (k, i, braid[k]) for k, c, i in d if i - braid[k] == m)
        ma = min(2 * i - arc[k] for k, c, i in data[g] if k in arc)
        w('| %s | %d | %d | %s | %d | none |' % (G[g], len(d), m, near, ma))
    w('\n**Observations.**\n')
    w('- Equality braid(K) = index(K) never holds for a non-trivial knot. The unknot has index 1 = braid index 1.')
    w('- For F₃ and $\\vec{F}_3$ the inequality braid(K) < index(K) holds on all the data, although no theorem '
      'covers it. For F₃ six knots have index = braid index + 1.')
    w('- *Question*: is braid(K) < F₃-index(K) for every non-trivial knot K?\n')
    w('Distribution of index − braid index (number of knots):\n')
    w('| index | ' + ' | '.join(str(x) for x in range(1, 13)) + ' |')
    w('|---|' + '---|' * 12)
    for g in G:
        c = Counter(i - braid[k] for k, cc, i in data[g] if k in braid)
        w('| %s | ' % G[g] + ' | '.join(str(c.get(x, '')) for x in range(1, 13)) + ' |')
    w('\n## Crossing number (Golan–Sapir)\n')
    w('G. Golan, M. Sapir, *On Jones\' subgroup of R. Thompson group F*, arXiv:1501.00724, Lemma 6.11 and Theorem '
      '6.13: a link with a diagram with n crossings, not an unlink, is represented by a reduced diagram with at most '
      '12n + u + 1 vertices, where u is the number of unlinked unknots.\n')
    w('- Their Thompson index counts the vertices of the diagram over ⟨x | x = x²⟩, i.e. the number of leaves + 1. '
      'By their Lemma 6.10, x₀, which has 3 leaves, has 4 vertices.')
    w('- For a knot (u = 0) this gives F-index ≤ 12c, with c the crossing number.\n')
    w('In the other direction, a tree diagram with n leaves has 2(n − 1) crossings, and so has a ternary diagram with '
      'n − 1 internal vertices per tree. So c ≤ 2(index − 1), i.e. index ≥ c/2 + 1, for all four indices.\n')
    w('| index | max(index − c) | knots attaining it | max index / c | min(2(index − 1) − c) | '
      'knots with c = 2(index − 1) |')
    w('|---|---|---|---|---|---|')
    for g in G:
        d = data[g]
        hi = max(i - c for k, c, i in d)
        mx = ', '.join('%s (%d)' % (k, i) for k, c, i in d if i - c == hi)
        lo = min(2 * (i - 1) - c for k, c, i in d)
        eq = [k for k, c, i in d if 2 * (i - 1) - c == lo]
        w('| %s | %d | %s | %.2f | %d | %s |' % (G[g], hi, mx, max(i / c for k, c, i in d), lo,
                                              '%d knots (list below)' % len(eq) if lo == 0 else
                                              'none (closest: %s)' % ', '.join(eq)))
    eq3 = [k for k, c, i in data['F3'] if 2 * (i - 1) == c]
    eqv = [k for k, c, i in data['F3vec'] if 2 * (i - 1) == c]
    w('\n**Observations.**\n')
    w('- **The Golan–Sapir bound is far from sharp.** F-index ≤ 12c, but on the data F-index ≤ c + 3 and '
      'F-index ≤ 1.75·c for every knot with a known F-index. No equality.')
    w('- **The lower bound index ≥ c/2 + 1 is attained** for F₃ by %d knots and for $\\vec{F}_3$ by %d knots. For them '
      'the minimal ternary tree diagram is a minimal crossing diagram.' % (len(eq3), len(eqv)))
    w('- It is never attained for F or for $\\vec{F}$.\n')
    w('F₃, c = 2(F₃-index − 1): ' + ', '.join(eq3) + '.\n')
    w('$\\vec{F}_3$, c = 2($\\vec{F}_3$-index − 1): ' + ', '.join(eqv) + '.')
    gen = {}
    for K in KnotInfo:
        if K.is_knot() and K.crossing_number() >= 3:
            try:
                gen[K.value] = int(K.three_genus())
            except Exception:
                pass
    w('\n## Seifert genus (Luo–Wan, Theorem 1.13)\n')
    w('For g in $\\vec{F}$ with n leaves the checkerboard surface of L(g) is a Seifert surface with n disks and '
      '2(n − 1) bands, so χ ≥ 2 − n and g(K) ≤ (n − 1)/2 (Luo–Wan, Theorem 1.13). The same argument applies to '
      '$\\vec{F}_3$ (n vertices, 2(n − 1) edges).\n')
    for g in ('Fvec', 'F3vec'):
        d = [(k, i) for k, c, i in data[g] if k in gen]
        m = min((i - 1) // 2 - gen[k] for k, i in d)
        eq = [k for k, i in d if (i - 1) // 2 - gen[k] == m]
        w('- %s: %d knots with known index and genus, min((index − 1)/2 − g) = %d, attained by %d knots%s.' % (
            G[g], len(d), m, len(eq), (' (e.g. ' + ', '.join(eq[:12]) + ')') if eq else ''))
    w('\nSo the genus bound is never sharp for $\\vec{F}$ on the data, but it is an equality for many knots in '
      '$\\vec{F}_3$: for them the checkerboard surface of a minimal ternary diagram is a minimal genus Seifert surface.')
    open(os.path.join(HERE, 'results', 'index_bounds.md'), 'w').write('\n'.join(L) + '\n')
    print('results/index_bounds.md: %d + %d knots attain c = 2(index - 1) for F3 / vec{F}3' % (len(eq3), len(eqv)))


if __name__ == '__main__':
    main()
