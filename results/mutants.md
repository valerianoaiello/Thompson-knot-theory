# Mutant knots: the Conway knot 11n_34 and the Kinoshita–Terasaka knot 11n_42

11n_34 and 11n_42 are mutants. They have the same HOMFLY polynomial, the same hyperbolic volume and the
same knot Floer total rank. They have different Seifert genus: 3 for 11n_34, 2 for 11n_42. Both are
chiral and non-invertible (KnotInfo symmetry type "chiral").

| index | 11n_34 | 11n_42 |
|---|---|---|
| F | 12 | 12 |
| F₃ | 8 | 8 |
| vec{F}₃ | 9 | 9 |
| **vec{F}** | **≥ 19** | **15** |

The F-, F₃- and vec{F}₃-indices are the indices of the knot up to orientation and mirror image. For
vec{F}₃ the oriented values are computed by `oriented_scan.py`.

**The vec{F}-index distinguishes the two mutants**, whatever their orientations:

- **11n_42 has vec{F}-index 15.** A 15-leaf witness is

      000,0010,0011,0100,0101000,01010010,01010011,0101010,0101011,01011,011,100,101,110,111 | 00,0100,010100,0101010,0101011,01011000,010110010,010110011,010110100,0101101010,0101101011,01011011,010111,011,1

  It was identified by `identify.sage`. The orientation it realizes is listed in
  `results/oriented_index_Fvec.md`.

- **11n_34 is not L(g) for any g ∈ vec{F} with n ≤ 17 leaves, so its vec{F}-index is ≥ 19** (knots only
  occur for odd n). The proof:
  1. The common HOMFLY class of 11n_34 and 11n_42 does not occur in vec{F} for n < 15. This is exact,
     because the HOMFLY polynomial is computed for every diagram.
  2. At n = 15 and n = 17 the class contains 39 and 2541 tree diagrams of vec{F}.
  3. All 2580 of them have Seifert genus 2, computed with knot Floer homology (spherogram), whereas 11n_34
     has genus 3. Genus does not depend on orientation or mirror image, so no orientation of 11n_34 or of
     its mirror image is realized.
  4. Independently, `complete_check.py` compared each of these diagrams with 11n_34 using SnapPy
     isometries, and none is 11n_34.
