# Comparison with D. Sweeney's list of Thompson indices

Source: https://github.com/sweeneyde/thompson_knots, file `unoriented_data/README.md`, commit `508ce32`
(13 July 2021). It gives the Thompson index (F-index, number of leaves) of the prime knots with at most 10
crossings, as exact values up to 11 leaves and as ">= 12" otherwise. Knot names follow KnotInfo (10_1, …,
10_165), like ours.

Compared with `results/F_index.csv`: all tree diagrams up to n = 13 leaves, plus the complete check of
`results/complete_check_F.md`. The complete check compares every diagram of the HOMFLY classes involved,
not only 50 representatives per class.

**Result.** Of the 249 prime knots with at most 10 crossings, 245 have the same value in both tables,
including all 87 entries ">= 12". For two knots our value differs from his. Two knots get no value in his list:
they share a line with another knot with the same HOMFLY polynomial, which the polynomial alone cannot
separate, and only the other knot gets a value. These two are missing values, not errors.

| knot | Sweeney | F-index | kind |
|---|---|---|---|
| 10_45 | 11 | **13** | different value (his diagram is a different knot with the same HOMFLY polynomial) |
| 10_163 | 11 | **10** | different value (a 10-leaf diagram exists) |
| 10_132 | in the line "5_1\|10_132 is 8 leaves. 5_1 is 8." | **9** | missing value |
| 10_156 | in the line "8_16\|10_156 is 10 leaves. 8_16 is 10." | **10** | missing value |

Trees are given as leaf addresses (0 = left, 1 = right) and in Sweeney's notation (o = leaf, (xy) = caret).

## 10_45: 11 → 13

- **Sweeney's 11-leaf witness is not 10_45.** The witness is
  `(((o(((oo)o)o))((o(o(oo)))o))o) / (((oo)(o(((o(oo))o)o)))(o(oo)))`.
  - It has the HOMFLY polynomial of 10_45 and is hyperbolic.
  - Its volume is 16.8704; 10_45 has volume 13.7161.
  - SnapPy's `is_isometric_to` says the two complements are not isometric, so the knots are different.
  - Presumably the value was assigned by HOMFLY polynomial alone. That is not a proof for a diagram with
    more than 10 crossings.
- **No diagram with 11 or 12 leaves gives 10_45.** At n = 11 the HOMFLY class of 10_45 contains 2 diagrams.
  Both were compared with 10_45 and neither is 10_45. No diagram at n = 12 has this HOMFLY polynomial.
  The first appearance of the class is at n = 11, so there is nothing to check below it.
- **13-leaf witness:**
  - leaf addresses `0,10,110,11100,111010,111011,111100,111101000,111101001,111101010,111101011,1111011,11111 | 00000,00001,000100,000101,00011,0010,0011,010,0110,0111,10,110,111`;
  - Sweeney's notation `(o(o(o((o(oo))((o(((oo)(oo))o))o))))) / (((((oo)((oo)o))(oo))(o(oo)))(o(oo)))`;
  - it was identified as 10_45 by `identify.sage` (KnotInfo / SnapPy).

## 10_163: 11 → 10

- **10-leaf witness:**
  - leaf addresses `0,10000,1000100,1000101,100011,10010,10011,1010,1011,11 | 000,001,01,1000,10010,10011,1010,1011,110,111`;
  - Sweeney's notation `(o((((o((oo)o))(oo))(oo))o)) / (((oo)o)(((o(oo))(oo))(oo)))`.
- **Identification:**
  - SnapPy identifies its complement as 10_164 in Rolfsen's numbering, i.e. K10n35, the knot called 10_163
    in KnotInfo (Rolfsen's table counts the Perko pair twice).
  - SnapPy identifies the complement of KnotInfo's 10_163 diagram as the same census manifold.
- **The diagram is in Sweeney's own data.** It appears, up to symmetry, in their file
  `unoriented10_prime_and_first_of_symmetries.txt`, in a class without a label.
- **No smaller witness.** No diagram with fewer than 10 leaves has the HOMFLY polynomial of 10_163, so the
  F-index is exactly 10.

## 10_132: 9 (no value given)

- 10_132 and 5_1 have the same HOMFLY polynomial. Sweeney's line gives 8 for 5_1 and nothing for 10_132.
- **No diagram with 8 leaves gives 10_132.** The class first appears at n = 8. All diagrams of the class at
  n = 8, and those at n = 9 until a match was found, were compared with 10_132 (100 diagrams in all).
  None of the 8-leaf diagrams is 10_132.
- **9-leaf witness:**
  - leaf addresses `0,100,101,1100,11010,110110,1101110,1101111,111 | 00,01,100000,100001,10001,1001,101,110,111`;
  - Sweeney's notation `(o((oo)((o(o(o(oo))))o))) / ((oo)(((((oo)o)o)o)(oo)))`;
  - it is isometric to 10_132 (SnapPy).
- Our first run missed this witness too. It stored only 50 diagrams per HOMFLY class, and the class of 5_1
  is large. The complete check found it.

## 10_156: 10 (no value given)

- 10_156 and 8_16 have the same HOMFLY polynomial. Sweeney's line gives 10 for 8_16 and nothing for 10_156.
- **10-leaf witness:**
  - leaf addresses `0,1000,100100,100101,10011,101,1100,11010,11011,111 | 000,001,01,1000,100100,1001010,1001011,10011,101,11`;
  - Sweeney's notation `(o(((o((oo)o))o)((o(oo))o))) / (((oo)o)(((o((o(oo))o))o)o))`.
- **No smaller witness.** No diagram with fewer than 10 leaves has this HOMFLY polynomial, so the F-index
  of 10_156 is 10 (the same as 8_16).

## Method

1. **Enumeration.** All prime tree diagrams with n ≤ 13 leaves are enumerated by `bin/fknots`, and the
   HOMFLY polynomial of each is computed.
2. **First identification.** `identify.sage` identifies up to 50 representatives per HOMFLY class:
   KnotInfo for diagrams with ≤ 13 crossings after simplification, SnapPy otherwise.
3. **Complete check.** `complete_check.py` covers every knot whose class appears before the knot is found.
   It compares all diagrams of that class, from the first appearance up to the index, with the knot:
   hyperbolic volume, then a SnapPy isometry test.
4. **Lower bounds.** A HOMFLY class that does not appear below n proves index ≥ n. The HOMFLY polynomial is
   computed for every diagram, so these bounds are exact.
