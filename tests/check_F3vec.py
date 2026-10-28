"""
Checks of the vec{F}_3 mode of bin/iota_knots (plain Python + bin/iota_knots eval).

usage (from F_index/):   python3 tests/check_F3vec.py [cmax]      (default 5 = number of internal vertices)

vec{F}_3 = {(T+, T-) in F_3 : Gamma(T+, T-) 2-colourable} (Aiello-Nagnibeda, J. Algebra Appl. 21 (2022)
2250139). Checked here, for all pairs of ternary trees with c <= cmax internal vertices:
  1. the Tait graph built independently from the black regions (vertices at -1/2, 3/2, 7/2, ...; every
     4-valent vertex joins the two black regions around it) is bipartite iff c+(i) = c-(i) mod 2 for all
     leaves i (Prop. 1 of the paper, weights as in its Definition 3), and c(2i) = c(2i-1) (Lemma 2);
  2. the weights of the examples y0, y1^2, y0 y3 of the paper;
  3. iota(F) and vec{F}: for binary pairs (n <= 7 leaves) g in vec{F} (leaf-parity criterion of ftrees)
     iff iota(g) in vec{F}_3;
  4. a non-prime diagram of vec{F}_3 whose common interval starts at an even leaf splits into two elements of
     vec{F}_3 (the inner and the outer diagram), so bin/iota_knots may skip it;
  5. the number of components of L(g), g in vec{F}_3, is congruent to n = c + 1 mod 2 (same proof as
     results/parity_theorem.md: Gamma has c + 1 vertices, 2c edges, c + 1 faces);
  6. the number of pairs (a <= b) of vec{F}_3 equals the one examined by bin/iota_knots F3vec.
"""
import os
import subprocess
import sys
import tempfile
from multiprocessing import Pool

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, HERE)
import ftrees as F  # noqa: E402

BIN = os.path.join(HERE, 'bin', 'iota_knots')


def ternary_trees(c):
    if c == 0:
        return [None]
    out = []
    for c1 in range(c):
        for c2 in range(c - c1):
            for l in ternary_trees(c1):
                for m in ternary_trees(c2):
                    for r in ternary_trees(c - 1 - c1 - c2):
                        out.append((l, m, r))
    return out


def leaves(t):
    return 1 if t is None else sum(leaves(s) for s in t)


def words(t, prefix=''):
    if t is None:
        return [prefix or '0']
    return [w for i, s in enumerate(t) for w in words(s, prefix + str(i))]


def weight(word):
    """Definition 3: word = w1 1 w2 1 ... ; #1's + #2's in odd words + #0's in even words."""
    parts = word.split('1')
    return word.count('1') + sum(p.count('2') if k % 2 == 0 else p.count('0') for k, p in enumerate(parts))


def tait_edges(t):
    """Edges of Gamma_+(t) between black regions; region j = between leaves j-1 and j, black iff j even."""
    out = []

    def rec(s, a):
        if s is None:
            return
        l, m, r = (leaves(x) for x in s)
        regions = [a, a + l, a + l + m, a + l + m + r]
        black = [x // 2 for x in regions if x % 2 == 0]
        assert len(black) == 2
        out.append(tuple(black))
        rec(s[0], a)
        rec(s[1], a + l)
        rec(s[2], a + l + m)

    rec(t, 0)
    return out


def bipartite(nv, edges):
    col = [None] * nv
    col[0] = 0
    changed = True
    while changed:
        changed = False
        for u, w in edges:
            for x, y in ((u, w), (w, u)):
                if col[x] is not None:
                    if col[y] is None:
                        col[y] = 1 - col[x]
                        changed = True
                    elif col[y] == col[x]:
                        return False
    return True


def in_vec(tp, tm):
    return [weight(w) % 2 for w in words(tp)] == [weight(w) % 2 for w in words(tm)]


def intervals(t):
    """{(first leaf, last leaf): subtree} for the non-root internal vertices."""
    out = {}

    def rec(s, a, root):
        if s is None:
            return
        n = leaves(s)
        if not root:
            out[(a, a + n - 1)] = s
        for x in s:
            rec(x, a, False)
            a += leaves(x)

    rec(t, 0, True)
    return out


def collapse(t, iv):
    """Replace the subtree on the leaf interval iv by a leaf."""
    def rec(s, a):
        if s is None:
            return None
        if (a, a + leaves(s) - 1) == iv:
            return None
        kids = []
        for x in s:
            kids.append(rec(x, a))
            a += leaves(x)
        return tuple(kids)
    return rec(t, 0)


def iota(t):
    return None if t is None else (iota(t[0]), None, iota(t[1]))


def check_top(task):
    c, i = task
    trees = ternary_trees(c)
    tp = trees[i]
    st = dict(pairs=0, vec=0, vec_le=0, grafts=0, fail=[], vec_pairs=[])
    for j, tm in enumerate(trees):
        st['pairs'] += 1
        v = in_vec(tp, tm)
        edges = tait_edges(tp) + tait_edges(tm)
        ok = len(edges) == 2 * c and bipartite(c + 1, edges) == v
        for t in (tp, tm):
            wt = [weight(w) for w in words(t)]
            ok &= all(wt[2 * k] == wt[2 * k - 1] for k in range(1, c + 1))
        if v:
            st['vec'] += 1
            if j >= i:
                st['vec_le'] += 1
            st['vec_pairs'].append((','.join(words(tp)), ','.join(words(tm))))
            common = set(intervals(tp)) & set(intervals(tm))
            for iv in common:
                if iv[0] % 2 == 0:
                    st['grafts'] += 1
                    ok &= in_vec(intervals(tp)[iv], intervals(tm)[iv])
                    ok &= in_vec(collapse(tp, iv), collapse(tm, iv))
        if not ok:
            st['fail'].append((words(tp), words(tm)))
    return st


def components(pairs):
    """Number of components from bin/iota_knots eval."""
    with tempfile.TemporaryFile('w+') as f:
        for t, b in pairs:
            f.write('F3 %s %s\n' % (t, b))
        f.seek(0)
        out = subprocess.run([BIN, 'eval'], stdin=f, capture_output=True, text=True, check=True).stdout
    return [int(line.split('\t')[0].split('=')[1]) for line in out.splitlines()]


def main():
    cmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    bad = 0

    # 2) examples of the paper (leaf words of the top and bottom trees, weights c+ and c-)
    ex = {'y0': ('00,01,02,1,2', '0,1,20,21,22', [0, 1, 1, 1, 1], [0, 1, 1, 2, 2], False),
          'y1^2': ('0,100,101,102,11,12,2', '0,1,20,21,220,221,222', [0, 3, 3, 2, 2, 1, 1], [0, 1, 1, 2, 2, 3, 3], True),
          'y0y3': ('00,01,02,10,11,12,2', '0,1,20,21,220,221,222', None, None, True)}
    for name, (t, b, ct, cb, member) in ex.items():
        wt, wb = [weight(w) for w in t.split(',')], [weight(w) for w in b.split(',')]
        ok = (ct is None or wt == ct) and (cb is None or wb == cb) and \
            ([x % 2 for x in wt] == [x % 2 for x in wb]) == member
        bad += not ok
        print('example %s: weights %s / %s, in vec{F}_3: %s: %s' % (name, wt, wb, member, 'ok' if ok else 'FAILED'))

    # 3) iota(F) and vec{F}
    for n in range(2, 8):
        nb = 0
        for tp in F.all_trees(n):
            for tm in F.all_trees(n):
                a = [w.count('1') % 2 for w in F.leaf_words(tp)] == [w.count('1') % 2 for w in F.leaf_words(tm)]
                nb += a != in_vec(iota(tp), iota(tm))
        bad += nb
        print('iota: n = %d binary leaves: %s' % (n, 'ok' if not nb else '%d FAILURES' % nb))

    with Pool(os.cpu_count()) as pool:
        for c in range(1, cmax + 1):
            tot = dict(pairs=0, vec=0, vec_le=0, grafts=0, fail=[], vec_pairs=[])
            for st in pool.imap_unordered(check_top, [(c, i) for i in range(len(ternary_trees(c)))]):
                for k in tot:
                    tot[k] += st[k]
            comps = components(tot['vec_pairs'])
            parity_ok = all(x % 2 == (c + 1) % 2 for x in comps)
            # 6) pairs examined by the engine
            with tempfile.TemporaryDirectory() as d:
                out = os.path.join(d, 'o.tsv')
                subprocess.run([BIN, 'F3vec', str(c + 1), '0', '1', out, '0'], check=True)
                head = open(out).readline()
            examined = int(dict(kv.split('=') for kv in head[2:].split() if '=' in kv)['examined'])
            ok = not tot['fail'] and parity_ok and examined == tot['vec_le']
            bad += not ok
            print('c = %d (n = %d): %d pairs of F_3, %d in vec{F}_3 (engine: %d with a <= b, python: %d), '
                  '%d even grafts, components %s, knots %d: %s' % (
                      c, c + 1, tot['pairs'], tot['vec'], examined, tot['vec_le'], tot['grafts'],
                      sorted(set(comps)), comps.count(1),
                      'ok' if ok else 'FAILED %s' % tot['fail'][:3]), flush=True)
    print('all checks passed' if not bad else '%d FAILURES' % bad)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
