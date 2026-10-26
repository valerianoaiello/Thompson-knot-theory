# Cross-check of bin/fknots against the reference implementation ftrees.py and Sage.
# Run from F_index/:   sage tests/check_cpp.sage
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


def mirror(p):
    return p.subs(L=Lv**-1)


def canonical(tp, tm):
    """Python version of the orbit representative test of fknots."""
    T = F.all_trees(F.n_leaves(tp))
    idx = {t: i for i, t in enumerate(T)}
    me = (idx[tp], idx[tm])
    others = [(idx[tm], idx[tp]), (idx[F.flip(tp)], idx[F.flip(tm)]), (idx[F.flip(tm)], idx[F.flip(tp)])]
    return all(me <= o for o in others)


# 1) the 4_1 example of the paper
g = F.word(0, 2, 2, 5, 6, -7, -6, -4)
assert Link(F.pd_code(*g)).homfly_polynomial(normalization='vz') == KnotInfo.K4_1.homfly_polynomial()
print('example 2.3 of the paper gives 4_1: ok')

tmp = tempfile.mkdtemp()
for n in range(3, 8):
    out = os.path.join(tmp, 'n%d.tsv' % n)
    subprocess.run(['./bin/fknots', str(n), '0', '1', out, '1000000'], check=True)
    lines = open(out).read().splitlines()
    stats = dict(kv.split('=') for kv in lines[0][2:].split())
    cpp_classes = {}
    for line in lines[1:]:
        key, count, reps = line.split('\t')
        cpp_classes[key] = [tuple(F.from_leaf_words(w.split(',')) for w in r.split('|')) for r in reps.split(';')]

    # 2) same number of knot diagrams as the reference implementation
    T = F.all_trees(n)
    ref = [(tp, tm) for tp in T for tm in T
           if F.is_prime_diagram(tp, tm) and F.number_of_components(tp, tm) == 1 and canonical(tp, tm)]
    assert int(stats['knots']) == len(ref), (n, stats, len(ref))

    # 3) every diagram has the HOMFLY (up to mirror) that fknots says, computed by Sage from ftrees' PD code
    nd = 0
    for key, reps in cpp_classes.items():
        p = key_from_cpp(key)
        for tp, tm in reps:
            q = Link(F.pd_code(tp, tm)).homfly_polynomial('L', 'M', 'lm')
            assert q in (p, mirror(p)), (n, key, q)
            nd += 1
    assert nd == len(ref)
    print('n = %d: %d knot diagrams, %d HOMFLY classes: ok' % (n, nd, len(cpp_classes)))
