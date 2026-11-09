# Oriented vec{F}-index of the non-invertible knots

Non-invertible knots of KnotInfo with <= 10 crossings whose HOMFLY class appears at n <= 17; every tree diagram of vec{F} of those classes with n <= 17 was compared with the oriented KnotInfo diagram K (oriented_scan.py). K = KnotInfo orientation, Kr = reverse, Km = mirror image, Kmr = both. index(K) = index(Kmr) and index(Kr) = index(Km) (L(g^-1) is the mirror image of the reverse of L(g)); for invertible knots all four values equal the index of results/Fvec_index.csv.

Rule for g^-1 checked directly on 60 diagrams: ok. Chunks skipped because they crash SnapPy: 0. min(index K, index Kr) differs from the unoriented table for: none.

| knot | symmetry | first n of HOMFLY | table (unoriented) | K | Kr | Km | Kmr | verdict |
|---|---|---|---|---|---|---|---|---|
| 8_17 | negative amphicheiral | 13 | 13 | 13 | 13 | 13 | 13 | equal |
| 9_32 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 9_33 | chiral | 13 | 13 | 13 | 13 | 13 | 13 | equal |
| 10_81 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_82 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_83 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_84 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_86 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_87 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 10_88 | negative amphicheiral | 13 | 13 | 15 | 13 | 13 | 15 | DIFFERENT |
| 10_90 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_91 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_93 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 10_94 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_95 | chiral | 17 | 17 | 17 | > 17 | > 17 | 17 | DIFFERENT |
| 10_102 | chiral | 15 | 15 | 15 | 17 | 17 | 15 | DIFFERENT |
| 10_106 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_107 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 10_110 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 10_115 | negative amphicheiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_117 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_118 | negative amphicheiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 10_119 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_147 | chiral | 15 | 15 | 15 | 15 | 15 | 15 | equal |
| 10_148 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_150 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
| 10_151 | chiral | 13 | 13 | 13 | 13 | 13 | 13 | equal |
| 10_153 | chiral | 17 | 17 | 17 | 17 | 17 | 17 | equal |
