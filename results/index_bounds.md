# The indices compared with the braid index, the arc index and the crossing number

**Data.**

- Indices: the final tables `results/<G>_index.csv` (F up to n = 13, F₃ up to n = 9, $\vec{F}$ up to n = 17, $\vec{F}_3$ up to n = 11), knots with a known index only.
- Braid index and arc index: KnotInfo. The braid index is available for 2977 knots, up to 12 crossings.
- For the oriented groups the index of the tables is min(index K, index Kr) (see `results/oriented_index_<G>.md`). The bounds below hold for every orientation, since braid index, arc index and crossing number do not depend on it.
- Script: `index_bounds.py`.

## Braid index and arc index (Luo–Wan)

Y. Luo, S. Wan, *Half grid diagrams and Thompson links*, arXiv:2408.10875, Theorem 1.15: grid(L) ≤ 2·ind_F(L), where ind_F is the F-index (number of leaves) and grid is the arc index. Consequences:

- bridge(L) ≤ braid(L) ≤ grid(L)/2 ≤ ind_F(L);
- braid ≤ $\vec{F}$-index, since F-index ≤ $\vec{F}$-index.

The theorem does not cover F₃ and $\vec{F}_3$.

| index | knots compared | min(index − braid) | knots attaining it (index / braid) | min(2·index − arc) | equality braid = index |
|---|---|---|---|---|---|
| F | 2147 | 3 | 3_1 (5 / 2) | 5 | none |
| F₃ | 2963 | 1 | 6_1 (5 / 4), 10_13 (7 / 6), 10_35 (7 / 6), 10_58 (7 / 6), 10_137 (6 / 5), 10_138 (6 / 5) | 2 | none |
| $\vec{F}$ | 1011 | 4 | 4_1 (7 / 3) | 8 | none |
| $\vec{F}_3$ | 2974 | 2 | 4_1 (5 / 3), 5_2 (5 / 3), 8_12 (7 / 5), 9_15 (7 / 5), 9_25 (7 / 5), 10_55 (7 / 5), 10_137 (7 / 5), 11n_1 (7 / 5), 12n_3 (7 / 5) | 2 | none |

**Observations.**

- Equality braid(K) = index(K) never holds for a non-trivial knot. The unknot has index 1 = braid index 1.
- For F₃ and $\vec{F}_3$ the inequality braid(K) < index(K) holds on all the data, although no theorem covers it. For F₃ six knots have index = braid index + 1.
- *Question*: is braid(K) < F₃-index(K) for every non-trivial knot K?

Distribution of index − braid index (number of knots):

| index | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F |  |  | 1 | 9 | 57 | 259 | 710 | 787 | 283 | 41 |  |  |
| F₃ | 6 | 305 | 1097 | 1100 | 377 | 77 | 1 |  |  |  |  |  |
| $\vec{F}$ |  |  |  | 1 |  | 1 | 10 | 25 | 42 | 146 | 188 | 384 |
| $\vec{F}_3$ |  | 9 | 171 | 807 | 905 | 713 | 279 | 89 | 1 |  |  |  |

## Crossing number (Golan–Sapir)

G. Golan, M. Sapir, *On Jones' subgroup of R. Thompson group F*, arXiv:1501.00724, Lemma 6.11 and Theorem 6.13: a link with a diagram with n crossings, not an unlink, is represented by a reduced diagram with at most 12n + u + 1 vertices, where u is the number of unlinked unknots.

- Their Thompson index counts the vertices of the diagram over ⟨x | x = x²⟩, i.e. the number of leaves + 1. By their Lemma 6.10, x₀, which has 3 leaves, has 4 vertices.
- For a knot (u = 0) this gives F-index ≤ 12c, with c the crossing number.

In the other direction, a tree diagram with n leaves has 2(n − 1) crossings, and so has a ternary diagram with n − 1 internal vertices per tree. So c ≤ 2(index − 1), i.e. index ≥ c/2 + 1, for all four indices.

| index | max(index − c) | knots attaining it | max index / c | min(2(index − 1) − c) | knots with c = 2(index − 1) |
|---|---|---|---|---|---|
| F | 3 | 4_1 (7), 5_1 (8), 6_3 (9), 7_2 (10), 8_3 (11), 8_18 (11), 9_8 (12), 9_41 (12), 10_12 (13), 10_17 (13), 10_45 (13), 10_104 (13), 10_113 (13), 10_123 (13) | 1.75 | 4 | none (closest: 8_19, 10_124, 12n_285, 12n_462) |
| F₃ | 1 | 3_1 (4), 4_1 (5) | 1.33 | 0 | 105 knots (list below) |
| $\vec{F}$ | 10 | 5_1 (15), 7_2 (17), 7_4 (17) | 3.00 | 8 | none (closest: 4_1) |
| $\vec{F}_3$ | 2 | 3_1 (5) | 1.67 | 0 | 3 knots (list below) |

**Observations.**

- **The Golan–Sapir bound is far from sharp.** F-index ≤ 12c, but on the data F-index ≤ c + 3 and F-index ≤ 1.75·c for every knot with a known F-index. No equality.
- **The lower bound index ≥ c/2 + 1 is attained** for F₃ by 105 knots and for $\vec{F}_3$ by 3 knots. For them the minimal ternary tree diagram is a minimal crossing diagram.
- It is never attained for F or for $\vec{F}$.

F₃, c = 2(F₃-index − 1): 8_19, 8_20, 10_124, 10_128, 10_132, 10_133, 10_134, 10_136, 10_137, 10_138, 10_140, 10_141, 10_147, 10_150, 10_165, 12n_1, 12n_2, 12n_3, 12n_6, 12n_10, 12n_20, 12n_38, 12n_39, 12n_40, 12n_45, 12n_68, 12n_71, 12n_73, 12n_80, 12n_84, 12n_97, 12n_119, 12n_120, 12n_121, 12n_130, 12n_142, 12n_146, 12n_150, 12n_152, 12n_153, 12n_154, 12n_156, 12n_157, 12n_159, 12n_160, 12n_162, 12n_172, 12n_176, 12n_182, 12n_188, 12n_196, 12n_198, 12n_218, 12n_271, 12n_275, 12n_286, 12n_288, 12n_293, 12n_300, 12n_301, 12n_310, 12n_312, 12n_323, 12n_326, 12n_327, 12n_333, 12n_338, 12n_342, 12n_358, 12n_362, 12n_368, 12n_370, 12n_379, 12n_381, 12n_388, 12n_399, 12n_407, 12n_408, 12n_420, 12n_427, 12n_428, 12n_438, 12n_443, 12n_444, 12n_449, 12n_451, 12n_452, 12n_459, 12n_462, 12n_485, 12n_491, 12n_502, 12n_512, 12n_568, 12n_590, 12n_591, 12n_592, 12n_597, 12n_603, 12n_625, 12n_634, 12n_705, 12n_706, 12n_742, 12n_838.

$\vec{F}_3$, c = 2($\vec{F}_3$-index − 1): 12n_3, 12n_20, 12n_119.

## Seifert genus (Luo–Wan, Theorem 1.13)

For g in $\vec{F}$ with n leaves the checkerboard surface of L(g) is a Seifert surface with n disks and 2(n − 1) bands, so χ ≥ 2 − n and g(K) ≤ (n − 1)/2 (Luo–Wan, Theorem 1.13). The same argument applies to $\vec{F}_3$ (n vertices, 2(n − 1) edges).

- $\vec{F}$: 2155 knots with known index and genus, min((index − 1)/2 − g) = 2, attained by 3 knots (e.g. 4_1, 8_18, 10_123).
- $\vec{F}_3$: 12708 knots with known index and genus, min((index − 1)/2 − g) = 0, attained by 2571 knots (e.g. 5_1, 7_1, 8_2, 8_5, 8_7, 8_9, 8_10, 8_17, 8_19, 9_1, 9_6, 9_9).

So the genus bound is never sharp for $\vec{F}$ on the data, but it is an equality for many knots in $\vec{F}_3$: for them the checkerboard surface of a minimal ternary diagram is a minimal genus Seifert surface.
