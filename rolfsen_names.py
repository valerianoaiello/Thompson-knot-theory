"""
Translation of SnapPy's names of the knots with at most 10 crossings (Rolfsen's table) into KnotInfo's names.

usage (from F_index/):   sage -python rolfsen_names.py      -> results/rolfsen_to_knotinfo.json

Rolfsen's numbering differs from KnotInfo's (10_83 / 10_86; 10_162-10_166 after the Perko pair), and SnapPy
names these knots as in Rolfsen's table. For every KnotInfo knot with at most 10 crossings, SnapPy identifies
the complement of its KnotInfo diagram: every Rolfsen name it returns is mapped to the KnotInfo name. Knots
SnapPy does not identify (the torus knots) are left out: identify_lib.quick_name names them with get_knotinfo.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    import snappy  # noqa: F401
    import spherogram
    from sage.all import KnotInfo
    out, missing = {}, []
    for K in KnotInfo:
        if not K.is_knot() or not 3 <= K.crossing_number() <= 10:
            continue
        pd = [[x - 1 for x in c] for c in K.link().pd_code()]
        ids = spherogram.Link(pd).exterior().identify()
        names = [str(M).split('(')[0] for M in ids]
        rolf = [nm for nm in names if re.fullmatch(r'(\d+)_\d+', nm) and int(nm.split('_')[0]) <= 10]
        if not rolf:
            missing.append(K.value)
        for nm in rolf:
            if out.get(nm, K.value) != K.value:
                raise ValueError('%s is both %s and %s' % (nm, out[nm], K.value))
            out[nm] = K.value
    path = os.path.join(HERE, 'results', 'rolfsen_to_knotinfo.json')
    json.dump(dict(sorted(out.items())), open(path, 'w'), indent=0)
    diff = {r: k for r, k in out.items() if r != k}
    print('%d Rolfsen names mapped; different names: %s; not identified by SnapPy: %s' % (len(out), diff, missing))


if __name__ == '__main__':
    main()
