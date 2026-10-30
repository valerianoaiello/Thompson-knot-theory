# Further checks of the reference implementation ftrees.py (ported from the former nuovo_codice/).
# Run from F_index/:   sage tests/check_graft_and_old_code.sage
#
# 1) Prime test: grafting a tree diagram S (>= 2 leaves) into a pair of corresponding leaves of a
#    tree diagram R (>= 2 leaves) gives a non-prime diagram whose knot is the connected sum, i.e.
#    HOMFLY(graft) = HOMFLY(R) * HOMFLY(S). This justifies skipping non-prime diagrams.
# 2) Agreement (up to mirror image) with the author's earlier ternary code on iota(g) (directory
#    $THOMPSON_OLD_CODE, default ../vecchio codice; skipped if absent).
#    Note: on about 5% of the diagrams the old code returns the mirror image of the knot of the
#    other diagrams (it uses the same crossing rule, but some PD orientations are wrong; checked
#    by hand on top = 0,1,20,21,220,221,222, bottom = 00,010,011,012,02,1,2, a right-handed
#    trefoil). Mirror images do not change the F-index.
import os, random, sys
sys.path.insert(0, '.')
import ftrees as F

random.seed(int(2026))


def random_tree(n):
    """A random binary tree with n leaves."""
    if n == 1:
        return None
    k = random.randint(1, n - 1)
    return (random_tree(k), random_tree(n - k))


def homfly(tp, tm):
    return Link(F.pd_code(tp, tm)).homfly_polynomial('L', 'M', 'lm')


def mirror(p):
    L, M = p.parent().gens()
    return p.subs(L=L**-1)


def graft(R, S, i):
    """Insert the tree diagram S at the i-th pair of leaves of R."""
    (rt, rb), (st, sb) = R, S
    wt, wb = F.leaf_words(rt), F.leaf_words(rb)
    top = wt[:i] + [wt[i] + w for w in F.leaf_words(st)] + wt[i + 1:]
    bottom = wb[:i] + [wb[i] + w for w in F.leaf_words(sb)] + wb[i + 1:]
    return F.from_leaf_words(top), F.from_leaf_words(bottom)


# 1) grafting = connected sum
tested = 0
for _ in range(400):
    a, b = random.randint(2, 6), random.randint(2, 6)
    R = (random_tree(a), random_tree(a))
    S = (random_tree(b), random_tree(b))
    T = graft(R, S, random.randrange(a))
    if any(F.number_of_components(*D) != 1 for D in (R, S, T)):
        continue
    assert not F.is_prime_diagram(*T)
    assert homfly(*T) == homfly(*R) * homfly(*S), (R, S, T)
    tested += 1
print('grafting gives the connected sum on %d random knot diagrams: ok' % tested)


# 2) old code, through Jones' map iota: F -> F_3 (every caret gets a middle leaf)
OLD = os.environ.get('THOMPSON_OLD_CODE', os.path.join('..', 'vecchio codice'))


def iota_words(t, prefix=''):
    if t is None:
        return [prefix or '0']
    return iota_words(t[0], prefix + '0') + [prefix + '1'] + iota_words(t[1], prefix + '2')


if os.path.isdir(OLD):
    sys.path.insert(0, OLD)
    import group_operations as go
    import knot_construction as kc
    same = mirrored = 0
    for _ in range(300):
        n = random.randint(2, 5)
        tp, tm = random_tree(n), random_tree(n)
        if F.number_of_components(tp, tm) != 1:
            continue
        H = homfly(tp, tm)
        pd_old = kc.tree_diagram_to_planar_diagram(go.Ternary_tree_diagrams(iota_words(tp), iota_words(tm)))
        H_old = Link(pd_old).homfly_polynomial('L', 'M', 'lm')
        assert H_old in (H, mirror(H)), (tp, tm)
        same += H_old == H
        mirrored += H_old != H
    print('old code agrees up to mirror on %d knot diagrams (%d identical, %d mirror): ok'
          % (same + mirrored, same, mirrored))
else:
    print('old code not found in %s: skipped' % OLD)
