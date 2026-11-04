"""
For the knots of results/reverse_bound_F3vec.csv whose stored minimal diagram has ends of the same colour
('13-15'): search ALL the diagrams of their HOMFLY class at the realized n for one that realizes the realized
orientation (or its mirror reverse, which has the same index) and whose first and last Tait vertices have
different colours. By the move with two new vertices (paper, Theorem 3.2(vii)) such a diagram gives the other
orientation at n + 2, so its index is exactly n + 2; the new diagram is built and checked with SnapPy
(move_checked). The vec{F} analogue is reverse_bound.py.

Input: the all-diagram files of the oriented scan, tmp_check/oriented_F3vec_c13_n<n>/classes/.
usage (from F_index/): sage -python reverse_search_F3vec.py [processes]  -> results/reverse_search_F3vec.csv
(then python3 reverse_bound_F3vec.py uses it).
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

csv.field_size_limit(10**9)


REVERSE = {'same': 'reverse', 'reverse': 'same', 'mirror': 'mirror reverse', 'mirror reverse': 'mirror'}


def move2(top, bottom):
    """The move with two new vertices of Theorem 3.2(vii): T+' = ((., ., T+), ., .), T-' = (., ., T-) with a
    caret on its last leaf (leaf words over 0, 1, 2; the last leaf is the largest word)."""
    t, b = top.split(','), bottom.split(',')
    last = max(b)
    nt = ['00', '01'] + ['02' + w for w in t] + ['1', '2']
    nb = ['0', '1'] + ['2' + w for w in b if w != last] + ['2' + last + c for c in '012']
    return ','.join(nt), ','.join(sorted(nb))


def find(task):
    """task = [knot, want, ref_pd, chunks]: the first diagram realizing want (or its mirror reverse) with ends
    of different colours; also the numbers of diagrams with different ends and of matching ones."""
    import snappy  # noqa: F401
    import spherogram
    import complete_check as C
    import oriented as O
    knot, want, ref, chunks = task
    R = spherogram.Link([[x - 1 for x in c] for c in ref]).exterior()
    vk = float(R.volume())
    ok = {'K': {'same', 'mirror reverse'}, 'Kr': {'reverse', 'mirror'}}[want]
    seen = undecided = 0
    for path, off, cnt in chunks:
        with open(path) as f:
            f.seek(off)
            for _ in range(cnt):
                line = f.readline()
                if not line:
                    break
                fl = line.rstrip('\n').split('\t')
                tp, tm = O.ternary_from_words(fl[1].split(',')), O.ternary_from_words(fl[2].split(','))
                col = O.tait_colours3(tp, tm)
                if col is None or col[0] == col[-1]:
                    continue
                seen += 1
                pd = O.oriented_pd_code3(tp, tm)
                E = spherogram.Link([[x - 1 for x in c] for c in pd]).exterior()
                if not C._geometric(E):
                    undecided += 1
                    continue
                if abs(float(E.volume()) - vk) > C.VOLUME_EPS:
                    continue
                try:
                    rel = O.relation_to(pd, ref)
                except Exception:
                    undecided += 1
                    continue
                if rel & ok:
                    # check the move: the new diagram (n + 2) must realize the reverse
                    mt, mb = move2(fl[1], fl[2])
                    rel2 = O.relation_to(O.oriented_pd_code3(O.ternary_from_words(mt.split(',')),
                                                             O.ternary_from_words(mb.split(','))), ref)
                    checked = rel2 == {REVERSE[x] for x in rel}
                    return knot, fl[1] + ' | ' + fl[2], sorted(rel & ok), seen, undecided, mt + ' | ' + mb, checked
    return knot, None, [], seen, undecided, None, False


def main():
    processes = int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count()
    from sage.all import KnotInfo
    from identify_lib import RobustPool
    from oriented_index import homfly_key
    tasks = []
    for r in csv.DictReader(open(os.path.join(HERE, 'results', 'reverse_bound_F3vec.csv'))):
        if r['witness_ends_different_colours'] == 'yes':
            continue
        n = int(r['index_realized'])
        idx = json.load(open(os.path.join(HERE, 'tmp_check', 'oriented_F3vec_c13_n%d' % n, 'classes', 'index.json')))
        ref = [list(map(int, c)) for c in getattr(KnotInfo, 'K' + r['knot']).link().pd_code()]
        tasks.append([r['knot'], r['realized'], ref, idx[homfly_key(ref)]])
    print(len(tasks), 'knots to search', flush=True)
    rows = []
    with RobustPool(processes) as pool:
        for knot, w, rel, seen, und, moved, checked in pool.map(find, tasks):
            rows.append({'knot': knot, 'diagram': w or '', 'relation': ' '.join(rel),
                         'diagrams_with_ends_of_different_colours': seen, 'undecided': und,
                         'moved_diagram': moved or '', 'move_checked': 'yes' if checked else ('no' if w else '')})
            print(knot, 'found' if w else 'not found', seen, und, flush=True)
    rows.sort(key=lambda r: r['knot'])
    with open(os.path.join(HERE, 'results', 'reverse_search_F3vec.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(sum(1 for r in rows if r['diagram']), 'of', len(rows), 'knots have such a diagram')


if __name__ == '__main__':
    main()
