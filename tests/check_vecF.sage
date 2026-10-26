# Checks of the vec{F} mode of bin/fknots (Jones' oriented subgroup).
# Run from F_index/:   sage tests/check_vecF.sage
#
# 1) Membership: (T+, T-) is in vec{F} iff the Tait graph is 2-colourable iff every leaf has the same
#    parity of right edges (1's in its address) in T+ and in T-. Checked on all pairs with n <= 7.
#    Also: x0 x1, x1 x2, x2 x3 (the generators of Golan-Sapir) are in vec{F}, x0 and x1 are not.
# 2) The vertical reflection does not preserve vec{F} (so fknots does not use it in vec mode).
# 3) bin/fknots ... vec examines exactly the pairs g in vec{F} with g <= g^-1, and its counts of prime
#    diagrams and knots agree with the reference implementation ftrees.py for n <= 8.
# 4) Every stored representative is in vec{F} and has the HOMFLY polynomial (up to mirror) of its class.
# 5) Knots appear only for odd n (the number of components of L(g), g in vec{F}, has the parity of n).
import os, subprocess, sys, tempfile
sys.path.insert(0, '.')
import ftrees as F

R = LaurentPolynomialRing(ZZ, 'L,M')
Lv, Mv = R.gens()


def key_from_cpp(s):
    p = R(0)
    for term in s.split():
        c, l, m = term.split('*')
        p += int(c) * Lv**int(l[2:]) * Mv**int(m[2:])
    return p


def bipartite(tp, tm):
    n = F.n_leaves(tp)
    adj = [[] for _ in range(n)]
    for a, b, s in F.tait_graph(tp, tm):
        adj[a].append(b)
        adj[b].append(a)
    col = [None] * n
    col[0] = 0
    stack = [0]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if col[w] is None:
                col[w] = 1 - col[u]
                stack.append(w)
            elif col[w] == col[u]:
                return False
    return True


def parity(t):
    return [w.count('1') % 2 for w in F.leaf_words(t)]


def in_vecF(tp, tm):
    return parity(tp) == parity(tm)


# 1) and 2)
flip_preserves = True
for n in range(1, 8):
    T = F.all_trees(n)
    for tp in T:
        for tm in T:
            assert bipartite(tp, tm) == in_vecF(tp, tm), (tp, tm)
            if in_vecF(tp, tm) != in_vecF(F.flip(tp), F.flip(tm)):
                flip_preserves = False
for g, expected in [((0, 1), True), ((1, 2), True), ((2, 3), True), ((0,), False), ((1,), False)]:
    assert in_vecF(*F.word(*g)) == expected, g
assert not flip_preserves
print('1-2) vec{F} membership = 2-colourable Tait graph (n <= 7); the vertical reflection does not preserve it: ok')

# 3), 4), 5)
tmp = tempfile.mkdtemp()
for n in range(2, 9):
    out = os.path.join(tmp, 'n%d.tsv' % n)
    subprocess.run(['./bin/fknots', str(n), '0', '1', out, '1000000', 'vec'], check=True)
    lines = open(out).read().splitlines()
    stats = dict(kv.split('=') for kv in lines[0][2:].split() if '=' in kv)
    T = F.all_trees(n)
    idx = {t: i for i, t in enumerate(T)}
    pairs = [(tp, tm) for tp in T for tm in T if idx[tp] <= idx[tm] and in_vecF(tp, tm)]
    prime = [(tp, tm) for tp, tm in pairs if F.is_prime_diagram(tp, tm)]
    knots = [(tp, tm) for tp, tm in prime if F.number_of_components(tp, tm) == 1]
    assert (int(stats['canonical']), int(stats['prime']), int(stats['knots'])) == \
        (len(pairs), len(prime), len(knots)), (n, stats, len(pairs), len(prime), len(knots))
    assert n % 2 == 1 or not knots, n
    nd = 0
    for line in lines[1:]:
        key, count, mincr, reps = line.split('\t')
        p = key_from_cpp(key)
        for r in reps.split(';'):
            tp, tm = (F.from_leaf_words(w.split(',')) for w in r.split('|')[:2])
            assert in_vecF(tp, tm)
            q = Link(F.pd_code(tp, tm)).homfly_polynomial('L', 'M', 'lm')
            assert q in (p, p.subs(L=Lv**-1)), (n, key, q)
            nd += 1
    assert nd == len(knots)
    print('3-5) n = %d: %d pairs in vec{F}, %d prime, %d knot diagrams, %d HOMFLY classes: ok'
          % (n, len(pairs), len(prime), len(knots), len(lines) - 1))
