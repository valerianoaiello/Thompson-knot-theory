# Thompson knot theory: the F-, F₃-, $\vec{F}$- and $\vec{F}_3$-indices of knots

Jones' construction associates a knot or link L(g) with every element g of Thompson's group F, given as a
pair of binary trees (T₊, T₋), and also with every element of the Brown–Thompson group F₃ (pairs of
ternary trees). Every knot arises in this way. This repository computes, for the knots of the KnotInfo
table (prime knots with ≤ 13 crossings), four indices:

| index | group | n = | knot type |
|---|---|---|---|
| **F-index** | F | number of leaves of each tree | unoriented, up to mirror image |
| **F₃-index** | F₃ | number of internal vertices of each tree + 1 | unoriented, up to mirror image |
| **$\vec{F}$-index** | binary oriented subgroup ${\vec{F}\le F}$ | number of leaves | **oriented** |
| **$\vec{F}_3$-index** | ternary oriented subgroup ${\vec{F}_3\le F_3}$ | internal vertices + 1 | **oriented** |

The index of K is the smallest n such that K = L(g) for a tree diagram g with that n.

## The groups

**Thompson's group F** is the group of piecewise linear homeomorphisms of [0, 1] whose breakpoints are
dyadic rationals and whose slopes are powers of 2 [1, 2]. It has the presentation

$$F = \langle x_0, x_1, x_2, \dots \mid x_n x_k = x_k x_{n+1} \text{ for } k < n \rangle .$$

Its elements are described by *tree diagrams* $(T_+, T_-)$: pairs of rooted binary trees with the same number
of leaves, up to adding or cancelling pairs of opposite carets.

**The Brown–Thompson group $F_3$** is defined in the same way with triadic breakpoints and slopes powers of
3 [3]; it has the presentation $\langle y_0, y_1, \dots \mid y_n y_k = y_k y_{n+2} \text{ for } k < n \rangle$,
and its elements are pairs of rooted ternary trees. Jones' map $\iota\colon F \to F_3$, $x_n \mapsto y_{2n}$,
replaces every binary caret by a ternary caret whose middle edge ends in a leaf.

**Jones' construction** [4, 5, 6]. Given $(T_+, T_-)$, draw $T_+$ above and $T_-$ below a horizontal line,
with the leaves on the line, and join the two roots by an edge around the left side. For ternary trees every
internal vertex becomes a crossing, the strand joining the left and right children passing over the strand
joining the parent and the middle child; for $F$ the trees are first sent to $F_3$ by $\iota$. The result is a
knot or link $L(T_+, T_-)$, and every knot and link arises in this way from $F$ and from $F_3$.
Equivalently, the regions between consecutive leaves are coloured alternately black and white, and $L(g)$ is
the link whose *Tait graph* $\Gamma(g)$ has the black regions as vertices and one edge for every internal vertex
of the two trees.

**The oriented subgroups.** Jones' *oriented subgroup* $\vec{F}$ (resp. $\vec{F}_3$) consists of the elements
of $F$ (resp. $F_3$) whose Tait graph is 2-colourable [4, 5, 7]. The colouring, with the leftmost vertex
coloured +, orients $L(g)$: the boundary of a + region runs counterclockwise, that of a − region clockwise.
Every oriented link arises from $\vec{F}$ [8]. $\vec{F}$ is isomorphic to $F_3$ [9]. Concretely:
- $g \in \vec{F}$ iff every leaf has the same parity of right edges on its path from the root in $T_+$ and
  in $T_-$;
- $g \in \vec{F}_3$ iff $c_+(i) \equiv c_-(i) \pmod 2$ for every leaf $i$, where the weight $c$ of a leaf
  counts the middle edges of its path, plus the right edges in the odd words and the left edges in the
  even words, the words being the pieces of the path between middle edges [7, Prop. 1]. The colour of the
  Tait vertex to the left of leaf $2v$ is the parity of $c_\pm(2v)$, even = +.

**The indices.** The F-index (resp. F₃-, $\vec{F}$-, $\vec{F}_3$-index) of a knot K is the smallest n such that
K = L(g) for a tree diagram g of size n in the corresponding group (table above). The F- and F₃-indices are
indices of unoriented knots, the $\vec{F}$- and $\vec{F}_3$-indices of oriented knots. A survey is [5].

## Main results

### Computed ranges

| index | all tree diagrams up to | known for |
|---|---|---|
| F | n = 13 | all knots with ≤ 10 crossings; 550 of 552 with 11; 1348 of 2176 with 12; 3902 of 9988 with 13 |
| F₃ | n = 8 | all knots with ≤ 10 crossings; 513 of 552 with 11; 1052 of 2176 with 12; 1563 of 9988 with 13 |
| $\vec{F}$ | n = 17 | 4 of 7 knots with 7 crossings, 19 of 21 with 8, 30 of 49 with 9, 103 of 165 with 10, 278 of 552 with 11 |
| $\vec{F}_3$ | n = 11 | all knots with ≤ 11 crossings; 2173 of 2176 with 12; 9734 of 9988 with 13 |

Tables:
- `results/F_index_table.md`, `results/F3_index_table.md`, `results/Fvec_index_table.md`,
  `results/F3vec_index_table.md`;
- knots with ≤ 9 crossings, all four indices side by side: `results/Fvec_index_upto9.md`.

Checked on the final tables (`tests/check_index_inequalities.py`), for every knot:
- F₃-index ≤ F-index;
- F₃-index ≤ $\vec{F}_3$-index ≤ $\vec{F}$-index;
- F-index ≤ $\vec{F}$-index.

### Oriented indices

For an oriented knot K write Kr for its reverse, Km for its mirror image and Kmr for both.
- **The inverse rule.** L(g⁻¹) is the mirror image of the reverse of L(g), in $\vec{F}$ and in
  $\vec{F}_3$ (`results/inverse_rule.md`; for $\vec{F}$ this is Aiello–Conti, CAOT 13 (2019), Remark 3.8).
  Hence index(K) = index(Kmr) and index(Kr) = index(Km).
- **Invertible knots** (K = Kr): the four values coincide.
- **Non-invertible knots**: `oriented_scan.py` computes index(K) and index(Kr) from all the diagrams.

**K and Kr can have different indices:**
- $\vec{F}$, non-invertible knots with ≤ 13 crossings, n ≤ 17 (`results/oriented_index_Fvec.md`), 1308 knots:
  - 85 have both orientations realized with different indices: 13/15 for 10_88, 12n_18, 12n_49, …;
    15/17 for 10_93, 10_102, 11a_26, …;
  - 226 have one orientation ≤ 17 and the other > 17, e.g. 10_95;
  - 8_17, 9_32 and 9_33 have equal indices.
- $\vec{F}_3$, n ≤ 11 (`results/oriented_index_F3vec.md`), 8121 knots:
  - 710 have both orientations realized with different indices;
  - 236 have one orientation > 11;
  - the smallest example is **8_17**: $\vec{F}_3$-index 7 for K = Kmr and 9 for Kr = Km. Its
    $\vec{F}$-index is 13 for both.

### Mutants

The $\vec{F}$-index distinguishes the Conway knot 11n_34 (≥ 19) from its mutant, the Kinoshita–Terasaka
knot 11n_42 (15), whatever the orientations (`results/mutants.md`).
- The proof is certified by the Seifert genus (knot Floer homology): all 2580 diagrams of their HOMFLY
  class with n ≤ 17 have genus 2, while 11n_34 has genus 3.
- The F-, F₃- and $\vec{F}_3$-indices of the two knots coincide.

### Comparison with classical invariants

`results/index_bounds.md` (script `index_bounds.py`):
- **Braid index.** Luo–Wan (arXiv:2408.10875, Theorem 1.15) prove braid ≤ F-index. On the data, braid < index
  holds for all four indices, with no equality for any non-trivial knot; for F₃ six knots have index = braid + 1.
- **Crossing number.** Golan–Sapir (arXiv:1501.00724, Lemma 6.11) prove F-index ≤ 12c; on the data F-index ≤ c + 3.
  The trivial bound c ≤ 2(index − 1) is attained by 105 knots for F₃ and 3 for $\vec{F}_3$, never for F or $\vec{F}$.

### Other results

- **Parity theorem.** For g in $\vec{F}$ or $\vec{F}_3$ the number of components of L(g) is ≡ n mod 2, so
  knots only occur for odd n. This is Aiello–Conti, CAOT 13 (2019), Prop. 3.11; a second proof is in
  `results/parity_theorem.md`, checked by `tests/check_parity.py`.
- **Corrections to D. Sweeney's table** of F-indices
  ([sweeneyde/thompson_knots](https://github.com/sweeneyde/thompson_knots)), in
  `results/sweeney_corrections.md`. 245 of his 249 knot entries agree with ours, including all 87 entries
  "≥ 12". The other four:

  | knot | Sweeney | correct F-index | reason |
  |---|---|---|---|
  | 10_45 | 11 | **13** | his 11-leaf diagram is a different knot with the same HOMFLY polynomial (volume 16.8704 vs 13.7161, complements not isometric); no diagram with 11 or 12 leaves gives 10_45 |
  | 10_163 | 11 | **10** | a 10-leaf diagram exists (its complement is K10n35 = 10_163 in KnotInfo); it is also in his own data, in an unlabelled class |
  | 10_132 | no value (listed with 5_1 at 8) | **9** | none of the 8-leaf diagrams of the class is 10_132; a 9-leaf diagram is |
  | 10_156 | no value (listed with 8_16 at 10) | **10** | a 10-leaf diagram exists; its class does not occur with fewer leaves |

  His oriented data (all diagrams of $\vec{F}$ up to 11 leaves, unlabelled) agree with ours.

## Installation

Requirements: a C++17 compiler, [SageMath](https://www.sagemath.org) (≥ 10, which provides libhomfly) and,
in Sage's Python, the packages `database_knotinfo` and `snappy`:

```bash
sage -pip install database_knotinfo snappy
make                                    # builds bin/fknots and bin/iota_knots
make SAGE_LOCAL=/path/to/sage/local     # if Sage is not in the default location (see the Makefile)
```

`SAGE_LOCAL` is the directory containing `include/homfly.h` and `lib/libhomfly`. The figures of knot diagrams
in the paper are drawn with [Thompson_utilities](https://github.com/valerianoaiello/Thompson_utilities).

## Usage

Run everything from the repository root. `sage` is SageMath's executable.

```bash
make                                  # bin/fknots, bin/iota_knots (link SageMath's libhomfly; set SAGE_LOCAL)
python3 run.py 13                     # F: enumerate n = 2..13 in parallel  -> results/raw/n<n>.tsv
python3 run.py 8  --group F3          # F₃                                   -> results/raw_F3/
python3 run.py 17 --group Fvec        # vec{F}                               -> results/raw_Fvec/
python3 run.py 11 --group F3vec       # vec{F}₃                              -> results/raw_F3vec/
sage identify.sage 13 [F|F3|Fvec|F3vec]                # identify the knots  -> results/<G>_index.csv
sage -python complete_check.py <G>                     # all diagrams of the classes found late / not found
sage -python resolve_undecided.py <G>                  # second pass on the undecided diagrams
sage -python apply_complete_check.py <G>               # apply the complete check to <G>_index.csv
python3 make_table.py <G>                              # final table -> results/<G>_index_table.md
python3 small_knots_table.py                           # all four indices, knots with <= 9 crossings
sage -python oriented_scan.py Fvec|F3vec [procs] [maxc]  # oriented indices of the non-invertible knots
```

Notes:
- `run.py` skips the values of n already computed, so a run can be resumed or extended.
- `complete_check.py`, `resolve_undecided.py` and `oriented_scan.py` keep their progress in `tmp_check/` and
  resume after an interruption.
- `identify.sage` needs `sage -pip install database_knotinfo snappy`.
- The raw data (`results/raw*/`, several GB) and `tmp_check/` are not in git.

Tests:

```bash
python3 tests/check_parity.py                    # parity theorem, every step of the proof, n <= 9
python3 tests/check_F3vec.py                     # vec{F}₃: weights, Tait graph, grafts, pair counts
sage -python tests/check_oriented3.py            # orientation in vec{F}₃: engine, ι, inverse rule
sage -python tests/check_index_inequalities.py   # inequalities between the four indices, ι of every witness
sage tests/check_cpp.sage                        # C++ vs Python vs Sage, Example 2.3 of the paper (4₁)
sage tests/check_vecF.sage                       # vec{F}
sage tests/check_iota_engine.sage                # iota_knots vs fknots, Sage
```

## Method

### Construction

`ftrees.py` builds the Tait graph Γ(T₊, T₋):
- its vertices are 0, …, n−1: vertex 0 is the region to the left of leaf 0, vertex j the gap between
  leaves j−1 and j;
- every internal vertex of a tree whose left subtree covers the leaves [a, j−1] gives an edge (a, j),
  positive in T₊ and negative in T₋;
- the link is the one whose Tait graph is Γ.

For F₃ (`src/iota_knots.cpp`):
- every internal vertex of a ternary tree is a crossing, with the left–right strand over;
- the map ι (a caret becomes a ternary caret with an empty middle leaf) sends F into F₃ and $\vec{F}$ into
  $\vec{F}_3$, preserving the oriented knot, so the index for F₃ is at most the one for F.

The oriented diagrams are built by `oriented.py` (`oriented_pd_code`, `oriented_pd_code3`).

### Reductions of the enumeration

The reductions are not the same in the four groups:

| reduction | F | F₃ | $\vec{F}$ | $\vec{F}_3$ |
|---|---|---|---|---|
| (T₊, T₋) ↦ (T₋, T₊), i.e. g ↦ g⁻¹ (mirror image; for the oriented groups the mirror reverse) | yes | yes | yes | yes |
| (T₊, T₋) ↦ (σT₊, σT₋), the vertical reflection (mirror image) | yes | yes | **no** (does not preserve $\vec{F}$) | **no** (does not preserve $\vec{F}_3$: it swaps black and white regions) |
| skip non-prime diagrams (a non-root subtree of T₊ and one of T₋ cover the same leaves) | yes | yes | yes | only if the common interval starts at an even leaf |
| keep only knots (one component) | yes | yes | yes (odd n only) | yes (odd n only) |

- **Symmetries.** One representative per orbit is kept. The oriented scan accounts for g⁻¹ through the
  inverse rule, and checks that rule directly on thousands of diagrams.
- **Primality.**
  - A non-prime diagram is a graft, i.e. a connected sum, so a prime knot is already realized with fewer
    leaves.
  - In $\vec{F}_3$ a graft below a middle edge (common interval starting at an odd leaf) can have pieces
    outside $\vec{F}_3$, so it is kept.
  - Composite knots can still arise from prime diagrams, e.g. the granny and square knots at n = 9 in F.
- **HOMFLY.** It is computed after a Reidemeister I and II simplification, with a cache on the simplified
  Gauss codes.

### Identification and complete check

1. **Raw data.** For every n the enumerator gives one line per HOMFLY class (up to mirror image), with the
   number of diagrams and up to 50 representatives.
2. **First identification.** `identify.sage` identifies the stored representatives.
   - A diagram with ≤ 13 crossings after simplification goes to Sage's `get_knotinfo()`. Then the knot has
     crossing number ≤ 13, so a HOMFLY match is a proof.
   - Larger diagrams go to SnapPy: complement identification, census up to 15 crossings, and Gordon–Luecke.
     A HOMFLY match alone is not enough there: at n = 10 a class has the HOMFLY of 13n_2638, but its knot
     is 14n_2554.
3. **Complete check.** Only 50 representatives per class are stored, so a knot can hide in a large class:
   10_132 was missed at n = 9, and 13n_2290 was found at 13 instead of 11. `complete_check.py` therefore
   enumerates **every** diagram of the classes of the knots found after their class first appears, or not
   found at all. Each diagram is compared with the knot: hyperbolic volume first, then a SnapPy isometry.
4. **Undecided diagrams.** Diagrams without a hyperbolic structure go to `resolve_undecided.py`. A
   different knot Floer homology, or an essential torus (a satellite knot), proves the diagram is not the
   target. No diagram is left undecided in the current results (`results/complete_check_<G>.md`).
5. **Lower bounds.** `lower_bound` is the first n at which the knot's HOMFLY class appears, and it is
   exact, because the HOMFLY polynomial is computed for every diagram. A knot that never appears gets
   n_max + 1, also exact after the complete check.

### Output files

- `results/<G>_index.csv`, one row per KnotInfo knot, with columns:
  - the index;
  - `lower_bound`;
  - `status` (identified / not found);
  - a witness `top_tree`, `bottom_tree`: leaf addresses, 0 = left, 1 = right, and 2 = right for ternary
    trees, where 1 = middle;
  - the number of crossings after simplification and the HOMFLY polynomial.
- `results/<G>_index_table.md`: index, KnotInfo name and a representative (for F also in normal form
  x₀^a₀ ⋯ x_k^a_k x_k^-b_k ⋯ x₀^-b₀, checked by multiplying the generators).
- `results/knots_beyond_table*.csv`: knots with 14–15 crossings recognized by SnapPy (upper bounds).
- `results/unidentified_classes*.csv`: HOMFLY classes of no prime knot with ≤ 13 crossings.

## Files

| file | content |
|---|---|
| `ftrees.py` | reference implementation in Python: trees, Tait graph, PD code, product in F |
| `oriented.py` | oriented links for $\vec{F}$ and $\vec{F}_3$, oriented comparison of knots (SnapPy isometries on meridian and longitude) |
| `src/fknots.cpp` | fast enumerator for F and $\vec{F}$ (`vec`): symmetries, primality, components, HOMFLY (libhomfly); `-1` = all diagrams of given classes |
| `src/iota_knots.cpp` | enumerator for F₃ and $\vec{F}_3$ (`F3vec`); with `F` it maps binary trees by ι (an independent cross-check of `fknots`) |
| `run.py` | parallel enumeration |
| `identify.sage`, `identify_lib.py` | identification with KnotInfo and SnapPy (crash-tolerant process pool `RobustPool`) |
| `complete_check.py`, `resolve_undecided.py`, `apply_complete_check.py` | complete check over all diagrams of the relevant HOMFLY classes |
| `make_table.py`, `small_knots_table.py` | final tables |
| `oriented_scan.py` | oriented indices (K, Kr, Km, Kmr) of the non-invertible knots |
| `reverse_scan.py`, `oriented_index.py`, `verify_reverse.py`, `reverse_examples.py` | earlier tools for K vs Kr in $\vec{F}$ |
| `tests/` | the checks listed above |

## Data

The tables of results are in `results/`. The raw enumeration data (`results/raw*/`, about 2.3 GB) and the
lists of all the diagrams of the HOMFLY-PT classes examined by the complete check and by the oriented scan
(about 76 GB) are not in this repository: they are regenerated by the commands above. A compressed selection
(all the HOMFLY-PT classes for every n with up to 50 representatives, including the witnesses of every index,
and the outcomes of the complete check and of the certified verification) will be published on Zenodo
together with the paper.

## How to cite

If you use this code or these data, please cite the repository (see `CITATION.cff`) and the paper
*Thompson indices of knots and the invertibility problem* by V. Aiello (in preparation).

## License

MIT License, see [LICENSE](LICENSE).

## History

This repository also contains, in its git history, the earlier Python implementation of the project (up
to commit `c79ea62`, February 2025). It was merged into this history when the current code replaced it;
its files are no longer in the working tree.

## References

1. J. W. Cannon, W. J. Floyd, W. R. Parry, *Introductory notes on Richard Thompson's groups*, Enseign. Math.
   (2) 42 (1996), 215–256.
2. J. Belk, *Thompson's group F*, Ph.D. thesis, Cornell University (2004),
   [arXiv:0708.3609](https://arxiv.org/abs/0708.3609).
3. K. S. Brown, *Finiteness properties of groups*, J. Pure Appl. Algebra 44 (1987), 45–75.
4. V. F. R. Jones, *Some unitary representations of Thompson's groups F and T*, J. Comb. Algebra 1 (2017),
   1–44.
5. V. Aiello, *An introduction to Thompson knot theory and to Jones subgroups*, J. Knot Theory Ramifications
   34 (2025), 2340002.
6. V. F. R. Jones, *On the construction of knots and links from Thompson's groups*, in: Knots,
   low-dimensional topology and applications, Springer Proc. Math. Stat. 284 (2019), 43–66.
7. V. Aiello, T. Nagnibeda, *On the oriented Thompson subgroup $\vec{F}_3$ and its relatives in higher
   Brown–Thompson groups*, J. Algebra Appl. 21 (2022), 2250139.
8. V. Aiello, *On the Alexander theorem for the oriented Thompson group $\vec{F}$*, Algebr. Geom. Topol. 20
   (2020), 429–438.
9. G. Golan, M. Sapir, *On Jones' subgroup of R. Thompson group F*, J. Algebra 470 (2017), 122–159.
