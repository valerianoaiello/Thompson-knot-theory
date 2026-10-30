"""
For the non-invertible knots with one orientation realized in vec{F} at n = 17 and the other not: search a
minimal diagram (n = 17) of the realized orientation whose first and last Tait vertices have different colours.
By the second move of Aiello, Rev. Un. Mat. Argentina 69 (2026), Theorem 4.2 (two vertices and four edges added,
removable by Reidemeister moves I and II), such a diagram gives the reverse knot with 19 leaves. When all the
minimal diagrams have ends of the same colour, the corrected first move (4 vertices, 8 edges) gives 21 leaves.
usage (from F_index/): sage -python reverse_bound.py  -> tmp_check/case2_search.json (then results/reverse_bound_Fvec.csv)
"""
import csv, sys, json, os
sys.path.insert(0, '.')
from identify_lib import RobustPool

def find(task):
    """task = [knot, want (K or Kr realized at 17), ref_pd, paths]: a diagram of type (+,-) realizing want or its mr."""
    import ftrees as F, oriented as O, snappy, spherogram
    knot, want, ref, chunks = task
    R = spherogram.Link([[x - 1 for x in c] for c in ref]).exterior()
    vk = float(R.volume())
    ok = {'K': {'same', 'mirror reverse'}, 'Kr': {'reverse', 'mirror'}}[want]
    seen = 0
    for path, off, cnt in chunks:
        with open(path) as f:
            f.seek(off)
            for _ in range(cnt):
                line = f.readline()
                if not line: break
                fl = line.rstrip('\n').split('\t')
                tp, tm = F.from_leaf_words(fl[1].split(',')), F.from_leaf_words(fl[2].split(','))
                col = O.tait_colours(tp, tm)
                if col[0] == col[-1]: continue
                seen += 1
                E = spherogram.Link([[x - 1 for x in c] for c in O.oriented_pd_code(tp, tm)]).exterior()
                for _ in range(5):
                    if E.solution_type() == 'all tetrahedra positively oriented': break
                    E.randomize()
                else:
                    continue
                if abs(float(E.volume()) - vk) > 1e-7: continue
                rel = O.relation_to(O.oriented_pd_code(tp, tm), ref)
                if rel & ok:
                    return knot, fl[1] + ' | ' + fl[2], seen
    return knot, None, seen

if __name__ == '__main__':
    from sage.all import KnotInfo
    from oriented_index import homfly_key
    import ftrees as F, oriented as O
    rows = list(csv.DictReader(open('results/oriented_index_Fvec.csv')))
    idx = json.load(open('tmp_check/oriented_Fvec_c13_n17/classes/index.json'))
    tasks = []
    for r in rows:
        a, b = r['index_K'], r['index_Kr']
        if a.isdigit() == b.isdigit(): continue
        want = 'K' if a.isdigit() else 'Kr'
        t, bb = [x.strip() for x in r['witness_' + want].split('|')]
        col = O.tait_colours(F.from_leaf_words(t.split(',')), F.from_leaf_words(bb.split(',')))
        if col[0] != col[-1]: continue
        ref = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + r['knot']).link().pd_code()]
        tasks.append([r['knot'], want, ref, idx[homfly_key(ref)]])
    print(len(tasks), 'knots to search', flush=True)
    found = {}
    with RobustPool(8) as pool:
        for k, w, seen in pool.map(find, tasks):
            found[k] = (w, seen)
    print(sum(1 for v in found.values() if v[0]), 'with a (+,-) minimal diagram;', [k for k, v in found.items() if not v[0]])
    json.dump(found, open('tmp_check/case2_search.json', 'w'))
