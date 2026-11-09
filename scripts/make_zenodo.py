"""
Builds the data archive published on Zenodo with the paper (a selection of the enumeration data: all the
HOMFLY-PT classes of knot diagrams with their counts and one representative each, not all the diagrams).

usage (from the repository root):  sage -python scripts/make_zenodo.py OUTDIR [N19_DIR]
  N19_DIR: the output directory of server/fvec_targeted.sbatch for vec{F} with n = 19 (files n19.tsv.<s>),
  optional.

OUTDIR/
  README.md                       format of the files
  classes/classes_<G>.tsv.gz      for G = F, F3, Fvec, F3vec and every n enumerated: every HOMFLY-PT class of knot
                                  diagrams (up to mirror image) with its number of diagrams, the smallest number
                                  of crossings after Reidemeister I and II moves, one representative, and the
                                  prime knots with at most 13 crossings whose index is n in that class with
                                  their witnesses (vec{F}, n = 19: classes and counts only, plus the witnesses)
  results.tar.gz                  the directory results/ of the repository (tables, certification, complete
                                  check, oriented indices, targeted searches), without raw data
  unidentified/unidentified_classes_<G>.csv.gz   HOMFLY-PT classes of no prime knot with at most 13 crossings
"""
import csv
import glob
import gzip
import os
import re
import shutil
import subprocess
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root (the scripts are in scripts/)
sys.path.insert(0, os.path.join(HERE, 'scripts'))
csv.field_size_limit(10**9)
RAW = {'F': 'raw', 'F3': 'raw_F3', 'Fvec': 'raw_Fvec', 'F3vec': 'raw_F3vec'}


def _key(k):
    import oriented_index as OI
    try:
        return k, OI.homfly_key(OI.reference_pd(k))
    except Exception:
        return k, None


def witnesses(group, keys):
    """(n, key) -> list of (knot, witness) for the knots whose index in `group` is n."""
    out = {}
    for r in csv.DictReader(open(os.path.join(HERE, 'results', '%s_index.csv' % group))):
        if r[group + '_index'] and r['knot'] in keys and keys[r['knot']]:
            n = int(r[group + '_index'])
            out.setdefault((n, keys[r['knot']]), []).append((r['knot'], '%s|%s' % (r['top_tree'], r['bottom_tree'])))
    return out


def classes(group, keys, outdir, n19=None):
    W = witnesses(group, keys)
    path = os.path.join(outdir, 'classes', 'classes_%s.tsv.gz' % group)
    nclasses = 0
    with gzip.open(path, 'wt') as f:
        f.write('# %s: all the HOMFLY-PT classes of knot diagrams, for every n enumerated\n' % group)
        f.write('n\thomfly_lm_up_to_mirror\tdiagrams\tmin_crossings_after_RI_RII\trepresentative\tknots_with_index_n\twitnesses\n')
        files = glob.glob(os.path.join(HERE, 'results', RAW[group], 'n*.tsv'))
        for p in sorted(files, key=lambda x: int(re.findall(r'n(\d+)\.tsv', x)[0])):
            n = int(re.findall(r'n(\d+)\.tsv', p)[0])
            for line in open(p):
                if line.startswith('#'):
                    continue
                parts = line.rstrip('\n').split('\t')
                rep = '|'.join(parts[3].split(';')[0].split('|')[:2]) if len(parts) > 3 and parts[3] else ''
                w = W.get((n, parts[0]), [])
                f.write('%d\t%s\t%s\t%s\t%s\t%s\t%s\n' % (n, parts[0].strip(), parts[1], parts[2], rep,
                                                       ' '.join(k for k, _ in w), ' '.join(d for _, d in w)))
                nclasses += 1
        if n19:
            counts = {}
            for p in glob.glob(os.path.join(n19, 'n19.tsv.*')):
                if not p.rsplit('.', 1)[1].isdigit():
                    continue
                for line in open(p):
                    if not line.startswith('#'):
                        k, c = line.split('\t')[:2]
                        counts[k] = counts.get(k, 0) + int(c)
            for k in sorted(counts):
                w = W.get((19, k), [])
                f.write('19\t%s\t%d\t\t\t%s\t%s\n' % (k.strip(), counts[k], ' '.join(x for x, _ in w),
                                                       ' '.join(d for _, d in w)))
                nclasses += 1
    print(group, nclasses, 'classes ->', path, '%.1f MB' % (os.path.getsize(path) / 1e6), flush=True)


README = """# Thompson indices of knots: data

DOI: 10.5281/zenodo.24082869

Data of the paper *Thompson indices of knots and the invertibility problem* (V. Aiello), computed with the code of
the repository https://github.com/valerianoaiello/Thompson-knot-theory (file `scripts/make_zenodo.py` builds
this archive). The groups are F, F3 (= F_3), Fvec (= vec F) and F3vec (= vec F_3); the size n of a tree diagram is
the number of leaves of each binary tree, and the number of internal vertices of each ternary tree + 1.

## classes/classes_<G>.tsv.gz

For every n enumerated (F: n <= 13; F3: n <= 9; Fvec: odd n <= 17, and n = 19 for the classes only; F3vec: odd
n <= 11), one line for every HOMFLY-PT class of knot diagrams of size n, up to mirror image:

- `homfly_lm_up_to_mirror`: the HOMFLY-PT polynomial in the variables L, M of libhomfly, as a list of
  `coefficient*L^a*M^b` terms, the smaller of the polynomial and of its mirror image (L -> 1/L);
- `diagrams`: the number of knot diagrams of size n in the class (after the reductions of the paper:
  g ~ g^-1, the vertical reflection for F and F3, prime diagrams only);
- `min_crossings_after_RI_RII`: the smallest number of crossings of a diagram of the class after Reidemeister I
  and II moves;
- `representative`: one diagram of the class, `top|bottom`, each tree given by the addresses of its leaves
  from left to right (0 = left, 1 = right; for ternary trees 0, 1, 2 = left, middle, right); empty at n = 19;
- `knots_with_index_n`, `witnesses`: the prime knots with at most 13 crossings (KnotInfo names) whose index is n
  and whose polynomial is that of the class, with their certified witnesses.
  The knots found beyond the enumeration by targeted searches (F: n = 14; F3: n = 10; Fvec: n = 21; F3vec:
  n = 13) are not in these files: their certified witnesses are in `results/descent_certified.csv`.

The lower bound of a knot K in the tables is the first n at which its HOMFLY-PT class occurs: it can be read
from these files. A witness can be checked by computing its knot, for instance with `ftrees.py` of the
repository and SnapPy.

## results.tar.gz

The directory `results/` of the repository at the time of publication: the tables of the four indices
(`<G>_index.csv`, with lower bounds and witnesses for every KnotInfo knot), the oriented indices of the
non-invertible knots, the outcomes of the complete check and of the certified verification, the targeted
searches (`descent_certified.csv`, `Fvec_beyond17_*`, `Fvec_n19_classes.csv`), the mutant pairs; see its
README.md.

## unidentified/unidentified_classes_<G>.csv.gz

The HOMFLY-PT classes that contain no prime knot with at most 13 crossings, with their first n, number of
diagrams and one representative.
"""


def main():
    outdir = sys.argv[1]
    n19 = sys.argv[2] if len(sys.argv) > 2 else None
    os.makedirs(os.path.join(outdir, 'classes'), exist_ok=True)
    os.makedirs(os.path.join(outdir, 'unidentified'), exist_ok=True)
    knots = [r['knot'] for r in csv.DictReader(open(os.path.join(HERE, 'results', 'F_index.csv'))) if r['knot'] != '0_1']
    with Pool(os.cpu_count()) as p:
        keys = dict(p.map(_key, knots, chunksize=50))
    keys['0_1'] = '1*L^0*M^0 '
    print('HOMFLY-PT keys of %d knots (%d failed)' % (len(keys), sum(v is None for v in keys.values())), flush=True)
    for g in ('F', 'F3', 'Fvec', 'F3vec'):
        classes(g, keys, outdir, n19 if g == 'Fvec' else None)
    for p in glob.glob(os.path.join(HERE, 'results', 'unidentified_classes*.csv')):
        out = os.path.join(outdir, 'unidentified', os.path.basename(p) + '.gz')
        with open(p, 'rb') as fi, gzip.open(out, 'wb') as fo:
            shutil.copyfileobj(fi, fo)
        print(out, '%.1f MB' % (os.path.getsize(out) / 1e6), flush=True)
    tracked = subprocess.run(['git', 'ls-files', 'results'], cwd=HERE, capture_output=True, text=True).stdout.split()
    subprocess.run(['tar', 'czf', os.path.abspath(os.path.join(outdir, 'results.tar.gz'))] + tracked, cwd=HERE, check=True)
    open(os.path.join(outdir, 'README.md'), 'w').write(README)
    print('done:', outdir)


if __name__ == '__main__':
    main()
