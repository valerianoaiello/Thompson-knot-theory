"""Compare the F- and Fvec-index tables with the Jones span bound.

Theorem (paper, Section 4): ind_Fvec(L) >= ind_F(L) >= span V_L + 1, and the
Fvec-index of a knot is odd. The span is computed from the HOMFLY-PT polynomial
stored in the tables (V(t) = P(v=t, z=t^(1/2)-t^(-1/2)) up to mirror image).

For every knot this script reports the bound, checks that no index in the
tables violates it, and lists the knots whose index equals the bound: for them
the index is proved by the witness alone, without any exclusion.

Usage: sage -python jones_span_bound.py
Output: results/jones_span_bound.csv, results/jones_span_bound.md
"""
import csv
from collections import Counter

from sage.all import QQ, LaurentPolynomialRing, sage_eval

csv.field_size_limit(10**9)

S = LaurentPolynomialRing(QQ, 's')
s = S.gen()


def jones_span(homfly):
    """Span in t of the Jones polynomial, from the HOMFLY-PT polynomial in v, z."""
    P = sage_eval(homfly, locals={'v': s ** 2, 'z': s - 1 / s})
    exps = S(P).exponents()
    return (max(exps) - min(exps)) // 2


def load(group):
    rows = {}
    with open(f'results/{group}_index.csv') as f:
        for r in csv.DictReader(f):
            rows[r['knot']] = r
    return rows


def main():
    F, Fv = load('F'), load('Fvec')
    nmax = {'F': 13, 'Fvec': 17}
    out = []
    for knot, r in F.items():
        if knot == '0_1':
            continue
        span = jones_span(r['homfly_vz'])
        bF = span + 1
        bFv = bF + (1 - bF % 2)          # odd
        iF, iFv = r['F_index'], Fv[knot]['Fvec_index']
        out.append(dict(knot=knot, crossing_number=r['crossing_number'],
                        jones_span=span, bound_F=bF, F_index=iF,
                        bound_Fvec=bFv, Fvec_index=iFv))
    viol, sharpF, sharpFv = [], [], []
    for o in out:
        for g, b, i in (('F', o['bound_F'], o['F_index']),
                        ('Fvec', o['bound_Fvec'], o['Fvec_index'])):
            if i and int(i) < b:
                viol.append((g, o['knot'], i, b))
            if not i and b > nmax[g] + (1 if g == 'F' else 2):
                o[f'new_bound_{g}'] = b
        if o['F_index'] and int(o['F_index']) == o['bound_F']:
            sharpF.append(o['knot'])
        if o['Fvec_index'] and int(o['Fvec_index']) == o['bound_Fvec']:
            sharpFv.append(o['knot'])
    keys = ['knot', 'crossing_number', 'jones_span', 'bound_F', 'F_index',
            'bound_Fvec', 'Fvec_index']
    with open('results/jones_span_bound.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, keys, extrasaction='ignore')
        w.writeheader()
        w.writerows(out)
    gapF = Counter(int(o['F_index']) - o['bound_F'] for o in out if o['F_index'])
    gapFv = Counter(int(o['Fvec_index']) - o['bound_Fvec'] for o in out if o['Fvec_index'])
    newF = [o['knot'] for o in out if 'new_bound_F' in o]
    newFv = [o['knot'] for o in out if 'new_bound_Fvec' in o]
    with open('results/jones_span_bound.md', 'w') as f:
        f.write('# The Jones span bound\n\n')
        f.write('`ind_Fvec(K) >= ind_F(K) >= span V_K + 1` (and the Fvec-index is odd). '
                'Script `jones_span_bound.py`.\n\n')
        f.write(f'- knots: {len(out)}; violations: **{len(viol)}** {viol[:20]}\n')
        f.write(f'- F: index - bound over the known values: {dict(sorted(gapF.items()))}\n')
        f.write(f'- Fvec: index - bound over the known values: {dict(sorted(gapFv.items()))}\n')
        f.write(f'- F-index equal to the bound ({len(sharpF)}): {", ".join(sharpF)}\n')
        f.write(f'- Fvec-index equal to the bound ({len(sharpFv)}): {", ".join(sharpFv)}\n')
        f.write(f'- unknown knots whose bound beats the enumeration (F > 14: {len(newF)}, '
                f'Fvec > 19: {len(newFv)})\n')
    print(open('results/jones_span_bound.md').read())


if __name__ == '__main__':
    main()
