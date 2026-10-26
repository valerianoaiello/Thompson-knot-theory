"""
Independent check of the knots found by reverse_scan.py with different vec{F}-indices for K and Kr.

usage (from F_index/):   sage -python verify_reverse.py KNOT N [KNOT N ...]

For KNOT at n: all the diagrams g in vec{F} with n leaves in its HOMFLY class are listed (both g and
g^-1, computed directly, without using the rule for the inverse). Each one is identified by SnapPy's
census (unoriented knot type, up to mirror), so that diagrams of other knots with the same HOMFLY are
recognized. Then all the diagrams of KNOT are compared with each other (not with the KnotInfo diagram):
the relations 'reverse' or 'mirror' between two of them would mean that both K and Kr (up to mirror
reverse) occur at n. If only 'same' and 'mirror reverse' occur, a single one of the two orientation
classes {K, Kmr}, {Kr, Km} is realized at n.
"""
import multiprocessing as mp
import os
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def census_name(task):
    top, bottom = task
    import snappy  # noqa: F401
    import spherogram
    import ftrees as F
    import oriented as O
    tp, tm = F.from_leaf_words(top.split(',')), F.from_leaf_words(bottom.split(','))
    pd = O.oriented_pd_code(tp, tm)
    S = spherogram.Link([[x - 1 for x in c] for c in pd])
    S.simplify('global')
    try:
        names = sorted(str(M).split('(')[0] for M in S.exterior().identify())
    except Exception as e:
        names = ['error ' + str(e)[:40]]
    return top, bottom, pd, names


def relation(task):
    import oriented as O
    a, b = task
    return sorted(O.relation_to(a, b))


def main():
    from sage.all import KnotInfo
    import snappy  # noqa: F401  (needed by spherogram for exteriors)
    import spherogram
    from oriented_index import homfly_key, diagrams
    args = sys.argv[1:]
    with ProcessPoolExecutor(os.cpu_count(), mp_context=mp.get_context('spawn')) as ex:
        for knot, n in zip(args[::2], map(int, args[1::2])):
            K = getattr(KnotInfo, 'K' + knot)
            ref = [list(map(int, c)) for c in K.link().pd_code()]
            ds = diagrams(n, homfly_key(ref), os.cpu_count())
            both = [d for t, b in ds for d in ((t, b), (b, t))]  # g and g^-1
            named = list(ex.map(census_name, both))
            ref_names = sorted(str(M).split('(')[0] for M in
                               spherogram.Link([[x - 1 for x in c] for c in ref]).exterior().identify())
            mine = [x for x in named if set(x[3]) & set(ref_names)]
            others = {}
            for x in named:
                if not set(x[3]) & set(ref_names):
                    others[' / '.join(x[3])] = others.get(' / '.join(x[3]), 0) + 1
            print('%s at n = %d: %d elements in its HOMFLY class; %d are %s, others: %s' % (
                knot, n, len(both), len(mine), '/'.join(ref_names), others or '-'), flush=True)
            if not mine:
                continue
            base = mine[0][2]
            rels = list(ex.map(relation, [(x[2], base) for x in mine]))
            seen = {}
            for r in rels:
                seen[tuple(r)] = seen.get(tuple(r), 0) + 1
            both_orientations = any(('reverse' in r or 'mirror' in r) for r in rels)
            print('   relations with the first one: %s -> %s' % (
                seen, 'BOTH K and Kr occur' if both_orientations else 'only ONE of K, Kr occurs (up to mirror reverse)'),
                flush=True)


if __name__ == '__main__':
    main()
