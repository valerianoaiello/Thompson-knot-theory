"""
Certified identification of the Borromean rings in F (n = 9) and F_3 (n = 6) (borromean.py uses SnapPy's
floating-point isometries). Every diagram of that size passing the three necessary conditions of borromean.py
(3 components, vanishing linking numbers, HOMFLY-PT polynomial of L6a4 up to mirror image; all exact) is compared
with L6a4 through the verified canonical retriangulations of the two exteriors (interval arithmetic, SnapPy
verified=True) and their combinatorial isomorphisms: an isomorphism taking meridians to meridians on every cusp
gives a homeomorphism of the exteriors extending to S^3, so the diagram is the Borromean rings (up to mirror image).
The lower bounds (no diagram of F with n <= 8, none of F_3 with n <= 5 satisfies the three conditions) are exact
and are not repeated here.

usage (from F_index/): sage -python certify_borromean.py   -> results/borromean_certified.md
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import borromean as B  # noqa: E402
import certify_indices as CI  # noqa: E402


def main():
    import snappy  # noqa: F401
    import spherogram
    ref_can = CI.canonical(spherogram.Link('L6a4').exterior())
    lines = ['# Certified identification of the Borromean rings', '',
             'Script `certify_borromean.py` (see its docstring): verified canonical retriangulations and their '
             'combinatorial isomorphisms, meridians to meridians on every cusp.', '']
    for group, n in (('F', 9), ('F3', 6)):
        total, three, lk0, hom, cands = B.three_component_diagrams(group, n)
        ok = not_iso = uncertified = 0
        for a, b, pd in cands:
            L = spherogram.Link([[x - 1 for x in c] for c in pd])
            try:
                can = CI.canonical(L.exterior())
            except Exception:
                uncertified += 1
                continue
            isos = can.isomorphisms_to(ref_can) or []
            if any(all(int(m[1, 0]) == 0 and abs(int(m[0, 0])) == 1 for m in iso.cusp_maps()) for iso in isos):
                ok += 1
            else:
                not_iso += 1
        lines.append('- %s, n = %d: %d diagrams with the three necessary conditions; **%d certified to be the '
                     'Borromean rings**, %d certified not to be, %d not certified' % (group, n, hom, ok, not_iso,
                                                                                      uncertified))
        print(lines[-1], flush=True)
    open(os.path.join(HERE, 'results', 'borromean_certified.md'), 'w').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
