"""
vec{F} beyond the enumeration (n <= 17): the HOMFLY-PT classes at n = 19 and the certified witnesses with 19 and
21 leaves.

1. classes: results/Fvec_n19_classes.csv, for every knot of results/Fvec_index.csv not realized by the
   enumeration, the number of knot diagrams with 19 leaves in its HOMFLY-PT class (up to mirror image), from the
   summary files DIR/n19.tsv.<s> written by `bin/fknots 19 -1 12 DIR/n19.tsv -1 vec @KEYS` (server/fvec_targeted.sbatch:
   all the classes with their counts, the diagrams only for the keys in KEYS). A knot whose class is absent has
   vec{F}-index >= 21 (no knot diagram with 19 leaves has its polynomial, and knots only occur for odd n).
2. certify: every diagram of results/Fvec_beyond17_witnesses.csv (knot, n, diagram, source: 'n19' = found in
   the diagrams of that enumeration, 'construction' = alexander.py + server/alternate_descent.py) is checked to
   lie in vec{F} (same parity mask of the two trees) and to realize the knot (certify_indices.is_K: verified
   canonical triangulations, or KnotInfo for torus knots). The certified ones are added to
   results/descent_certified.csv (name 'fvec19' or 'construction'), where apply_descent.py reads them; report in
   results/Fvec_beyond17_certified.md.

usage (from F_index/):  sage -python fvec_beyond17.py classes DIR [procs]
                        sage -python fvec_beyond17.py certify
then python3 apply_descent.py (lower bound 20 for the absent classes, index for the certified witnesses).
"""
import csv
import glob
import os
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
csv.field_size_limit(10**9)


def res(name):
    return os.path.join(HERE, 'results', name)


def _key(k):
    import oriented_index as OI
    return k, OI.homfly_key(OI.reference_pd(k))


def classes(d, procs):
    counts = {}
    shards = [f for f in glob.glob(os.path.join(d, 'n19.tsv.*')) if f.rsplit('.', 1)[1].isdigit()]
    assert len(shards) == 12, shards
    for f in shards:
        for line in open(f):
            if not line.startswith('#'):
                k, n = line.split('\t')[:2]
                counts[k] = counts.get(k, 0) + int(n)
    rows = list(csv.DictReader(open(res('Fvec_index.csv'))))
    todo = [r['knot'] for r in rows if not r['Fvec_index'] or 'targeted search' in r['status']]
    with Pool(procs) as p:
        keys = dict(p.map(_key, todo, chunksize=50))
    with open(res('Fvec_n19_classes.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['knot', 'diagrams_at_19'])
        for k in todo:
            w.writerow([k, counts.get(keys[k], 0)])
    absent = sum(counts.get(keys[k], 0) == 0 for k in todo)
    print('%d classes at n = 19, %d knot diagrams; %d knots, class absent for %d'
          % (len(counts), sum(counts.values()), len(todo), absent))


def certify():
    import certify_indices as CI
    wit = list(csv.DictReader(open(res('Fvec_beyond17_witnesses.csv'))))
    old = [r for r in csv.DictReader(open(res('descent_certified.csv'))) if r['name'] not in ('fvec19', 'construction')]
    fields = list(old[0])
    new, lines = [], []
    for r in wit:
        top, bottom = [x.strip() for x in r['diagram'].split('|')]
        a, b = top.split(','), bottom.split(',')
        vec = len(a) == len(b) == int(r['n']) and [x.count('1') % 2 for x in a] == [x.count('1') % 2 for x in b]
        st = CI.is_K(CI.pd_of('Fvec', top, bottom), r['knot']) if vec else ('not in vec{F}', '')
        ok = vec and st[0] == 'ok'
        print(r['knot'], r['n'], st, flush=True)
        lines.append('| %s | %s | %s | %s |' % (r['knot'], r['n'], r['source'], ' '.join(st)))
        if ok:
            new.append(dict(name='fvec19' if r['source'] == 'n19' else 'construction', group='Fvec', knot=r['knot'],
                            n=r['n'], diagram=r['diagram'], relation='isometric', final='yes', certified='yes',
                            certificate='ok ' + st[1]))
    with open(res('descent_certified.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(old + new)
    with open(res('Fvec_beyond17_certified.md'), 'w') as f:
        f.write('# vec{F}: certified witnesses beyond the enumeration\n\n`fvec_beyond17.py certify`: %d of %d '
                'diagrams lie in vec{F} and are certified to realize the knot (verified canonical triangulations; '
                'KnotInfo for torus knots).\n\n| knot | n | source | certificate |\n|---|---|---|---|\n%s\n'
                % (len(new), len(wit), '\n'.join(lines)))
    print('%d / %d certified' % (len(new), len(wit)))


if __name__ == '__main__':
    if sys.argv[1] == 'classes':
        classes(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8)
    else:
        certify()
