"""
The elements of vec{F} realizing each orientation of the knots found by reverse_scan.py.

usage (from F_index/):   sage -python reverse_examples.py KNOT N [N2 ...] [KNOT N ...]
e.g.                     sage -python reverse_examples.py 10_88 13 15 11a_256 15

For every KNOT and n: all the elements g in vec{F} with n leaves whose knot is KNOT (both g and g^-1, each
classified directly) with the orientation they realize with respect to the oriented KnotInfo diagram K:
K, Kr (reverse), Km (mirror), Kmr (mirror of the reverse). Written to results/reverse_examples.csv (all of
them) and results/reverse_examples.md (a few per orientation), with tree diagrams and normal forms.
"""
import csv
import multiprocessing as mp
import os
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
NAMES = {'same': 'K', 'reverse': 'Kr', 'mirror': 'Km', 'mirror reverse': 'Kmr'}
SHOWN = 3  # examples per (knot, n, orientation) in the .md file


def classify(task):
    top, bottom, ref = task
    import ftrees as F
    import oriented as O
    tp, tm = F.from_leaf_words(top.split(',')), F.from_leaf_words(bottom.split(','))
    return top, bottom, sorted(NAMES[r] for r in O.relation_to(O.oriented_pd_code(tp, tm), ref))


def main():
    from sage.all import KnotInfo
    from oriented_index import homfly_key, diagrams
    from make_table import normal_form

    jobs, knot = [], None
    for a in sys.argv[1:]:
        if '_' in a:
            knot = a
        else:
            jobs.append((knot, int(a)))
    rows = []
    with ProcessPoolExecutor(os.cpu_count(), mp_context=mp.get_context('spawn')) as ex:
        for knot, n in jobs:
            K = getattr(KnotInfo, 'K' + knot)
            ref = [list(map(int, c)) for c in K.link().pd_code()]
            ds = diagrams(n, homfly_key(ref), os.cpu_count())
            both = [(t, b, ref) for t0, b0 in ds for t, b in ((t0, b0), (b0, t0))]  # g and g^-1
            found = 0
            for top, bottom, orientations in ex.map(classify, both, chunksize=4):
                if not orientations:
                    continue  # another knot with the same HOMFLY
                found += 1
                rows.append({'knot': knot, 'symmetry': K.symmetry_type(), 'n': n,
                             'orientation': ' = '.join(orientations),
                             'normal_form': normal_form(top, bottom), 'top_tree': top, 'bottom_tree': bottom})
            print('%s, n = %d: %d elements of vec{F} realize it' % (knot, n, found), flush=True)

    with open(os.path.join(HERE, 'results', 'reverse_examples.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(HERE, 'results', 'reverse_examples.md'), 'w') as f:
        f.write('# Elements of vec{F} realizing K and its reverse\n\n'
                'K = the oriented knot of KnotInfo, Kr = its reverse, Km = its mirror image, Kmr = the mirror '
                'image of the reverse (for an amphicheiral knot some of them coincide, written e.g. K = Kmr). '
                'Orientation of L(g) from the 2-colouring of the Tait graph (colour + = counterclockwise); '
                'reversing this convention exchanges K with Kr and Km with Kmr. '
                'All the elements are in results/reverse_examples.csv; here at most %d per orientation.\n\n'
                % SHOWN)
        for knot in dict.fromkeys(r['knot'] for r in rows):
            sym = next(r['symmetry'] for r in rows if r['knot'] == knot)
            f.write('## %s (%s)\n\n' % (knot, sym))
            f.write('| n | orientation | elements | normal form | top tree | bottom tree |\n|---|---|---|---|---|---|\n')
            for n in dict.fromkeys(r['n'] for r in rows if r['knot'] == knot):
                for o in dict.fromkeys(r['orientation'] for r in rows if r['knot'] == knot and r['n'] == n):
                    sel = [r for r in rows if r['knot'] == knot and r['n'] == n and r['orientation'] == o]
                    for r in sel[:SHOWN]:
                        f.write('| %d | %s | %d | %s | `%s` | `%s` |\n' % (
                            n, o, len(sel), r['normal_form'], r['top_tree'], r['bottom_tree']))
            f.write('\n')
    print('written results/reverse_examples.csv (%d rows) and results/reverse_examples.md' % len(rows))


if __name__ == '__main__':
    main()
