# F-index and F_3-index of the Borromean rings (L6a4)

Jones' problem (On the construction of knots and links from Thompson's groups, 2019, Section 7): "calculate the F3 and F2 indices of the Borromean rings". Script `borromean.py`: all the tree diagrams of size n (no reduction), filtered by number of components (3), linking numbers (all 0), HOMFLY-PT polynomial up to mirror image (independent of the orientations when the linking numbers vanish), then a SnapPy isometry with L6a4 taking meridians to meridians (which extends to a homeomorphism of S^3 taking one link to the other). n = number of leaves for F, number of internal vertices + 1 for F_3; Jones counts internal vertices, i.e. n - 1.

## F

- F, n = 2: 1 diagrams, 0 with 3 components, 0 with vanishing linking numbers, 0 with the HOMFLY-PT polynomial of L6a4, **0 Borromean rings**
- F, n = 3: 4 diagrams, 2 with 3 components, 2 with vanishing linking numbers, 0 with the HOMFLY-PT polynomial of L6a4, **0 Borromean rings**
- F, n = 4: 25 diagrams, 0 with 3 components, 0 with vanishing linking numbers, 0 with the HOMFLY-PT polynomial of L6a4, **0 Borromean rings**
- F, n = 5: 196 diagrams, 72 with 3 components, 72 with vanishing linking numbers, 0 with the HOMFLY-PT polynomial of L6a4, **0 Borromean rings**
- F, n = 6: 1764 diagrams, 420 with 3 components, 342 with vanishing linking numbers, 0 with the HOMFLY-PT polynomial of L6a4, **0 Borromean rings**
- F, n = 7: 17424 diagrams, 5158 with 3 components, 4352 with vanishing linking numbers, 0 with the HOMFLY-PT polynomial of L6a4, **0 Borromean rings**
- F, n = 8: 184041 diagrams, 52918 with 3 components, 41872 with vanishing linking numbers, 0 with the HOMFLY-PT polynomial of L6a4, **0 Borromean rings**
- F, n = 9: the 64 diagrams with 9 leaves of D. Sweeney (github.com/sweeneyde/thompson_knots, folder Borromean/) are all certified to be the Borromean rings by the same test (e.g. `(((((oo)(oo))o)(o(oo)))o) / (o(((oo)(o((oo)o)))(oo)))` in Sweeney's notation).

**F-index of the Borromean rings: 9 leaves** (8 internal vertices in Jones' convention), in agreement with Sweeney.

## F_3

- F3, n = 2: 1 diagrams, 0 with 3 components, 0 with vanishing linking numbers, 0 with the HOMFLY-PT polynomial of L6a4, **0 Borromean rings**
- F3, n = 3: 9 diagrams, 3 with 3 components, 3 with vanishing linking numbers, 0 with the HOMFLY-PT polynomial of L6a4, **0 Borromean rings**
- F3, n = 4: 144 diagrams, 4 with 3 components, 2 with vanishing linking numbers, 0 with the HOMFLY-PT polynomial of L6a4, **0 Borromean rings**
- F3, n = 5: 3025 diagrams, 740 with 3 components, 470 with vanishing linking numbers, 0 with the HOMFLY-PT polynomial of L6a4, **0 Borromean rings**
- F3, n = 6: 74529 diagrams, 15660 with 3 components, 8742 with vanishing linking numbers, 14 with the HOMFLY-PT polynomial of L6a4, **14 Borromean rings** (e.g. `0,1,20,21,220,221,2220,22210,22211,22212,2222 | 0,100,101,1020,1021,10220,10221,10222,11,12,2`)

**F_3-index of the Borromean rings: n = 6** (5 internal vertices in Jones' convention); 14 ternary tree diagrams with n = 6 give them.
