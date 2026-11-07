# Thompson knot theory: the F-, F₃-, $`\vec{F}`$- and $`\vec{F}_3`$-indices of knots

Jones' construction associates a knot or link L(g) with every element g of Thompson's group F, given as a
pair of binary trees (T₊, T₋), and also with every element of the Brown–Thompson group F₃ (pairs of
ternary trees). Every knot arises in this way. This repository computes, for the knots of the KnotInfo
table (prime knots with ≤ 13 crossings), four indices, one for each of the following groups:

| group | name | n = | knot type |
|---|---|---|---|
| $`F`$ | Thompson's group | leaves of each tree | unoriented, up to mirror image |
| $`F_3`$ | Brown–Thompson group | internal vertices of each tree + 1 | unoriented, up to mirror image |
| $`\vec{F}`$ | Jones' oriented subgroup of $`F`$ | leaves of each tree | **oriented** |
| $`\vec{F}_3`$ | oriented subgroup of $`F_3`$ | internal vertices of each tree + 1 | **oriented** |

For each of these groups G, the *G-index* of a knot K is the smallest n such that K = L(g) for a tree
diagram g of G of size n.

## The groups

**Thompson's group F** is the group of piecewise linear homeomorphisms of [0, 1] whose breakpoints are
dyadic rationals and whose slopes are powers of 2 [4, 6]. It has the presentation

$$F = \langle x_0, x_1, x_2, \dots \mid x_n x_k = x_k x_{n+1} \text{ for } k < n \rangle .$$

Its elements are described by *tree diagrams* $`(T_+, T_-)`$: pairs of rooted binary trees with the same number
of leaves, up to adding or cancelling pairs of opposite carets.

**The Brown–Thompson group $`F_3`$** is defined in the same way with triadic breakpoints and slopes powers of
3 [5]; it has the presentation $`{\langle y_0, y_1, \dots \mid y_n y_k = y_k y_{n+2} \text{ for } k < n \rangle}`$,
and its elements are pairs of rooted ternary trees. Jones' map $`{\iota\colon F \to F_3}`$, $`{x_n \mapsto y_{2n}}`$,
replaces every binary caret by a ternary caret whose middle edge ends in a leaf.

**Jones' construction** [2, 8, 9]. Given $`(T_+, T_-)`$, draw $`T_+`$ above and $`T_-`$ below a horizontal line,
with the leaves on the line, and join the two roots by an edge around the left side. For ternary trees every
internal vertex becomes a crossing, the strand joining the left and right children passing over the strand
joining the parent and the middle child; for $F$ the trees are first sent to $`F_3`$ by $`\iota`$. The result is a
knot or link $`L(T_+, T_-)`$, and every knot and link arises in this way from $F$ and from $`F_3`$.
Equivalently, the regions between consecutive leaves are coloured alternately black and white, and $L(g)$ is
the link whose *Tait graph* $`\Gamma(g)`$ has the black regions as vertices and one edge for every internal vertex
of the two trees.

**The oriented subgroups.** Jones' *oriented subgroup* $`\vec{F}`$ (resp. $`\vec{F}_3`$) consists of the elements
of $F$ (resp. $`F_3`$) whose Tait graph is 2-colourable [2, 3, 8]. The colouring, with the leftmost vertex
coloured +, orients $L(g)$: the boundary of a + region runs counterclockwise, that of a − region clockwise.
Every oriented link arises from $`\vec{F}`$ [1], and $`\vec{F}`$ is isomorphic to $`F_3`$ [7]. Concretely:
- an element $`g`$ is in $`\vec{F}`$ iff every leaf has the same parity of right edges on its path from the root in $`T_+`$ and in $`T_-`$;
- an element $`g`$ is in $`\vec{F}_3`$ iff, for every leaf $`i`$, $`{c_+(i) \equiv c_-(i) \pmod 2}`$, where the weight $`c`$ of a leaf counts the middle edges of its path, plus the right edges in the odd words and the left edges in the even words, the words being the pieces of the path between middle edges [3, Prop. 1]. The colour of the Tait vertex to the left of leaf $`2v`$ is the parity of $`c_\pm(2v)`$, even = +.

**The indices.** The F-index (resp. F₃-, $`\vec{F}`$-, $`\vec{F}_3`$-index) of a knot K is the smallest n such that
K = L(g) for a tree diagram g of size n in the corresponding group (table above). The F- and F₃-indices are
indices of unoriented knots, the $`\vec{F}`$- and $`\vec{F}_3`$-indices of oriented knots. A survey is [2].

## Main results

### Computed ranges

| index | all tree diagrams up to | known for |
|---|---|---|
| F | n = 13 | all knots with ≤ 10 crossings; 550 of 552 with 11; 1348 of 2176 with 12; 3902 of 9988 with 13 |
| F₃ | n = 9 | all knots with ≤ 11 crossings; 2162 of 2176 with 12; 8357 of 9988 with 13 |
| $`\vec{F}`$ | n = 17 | 4 of 7 knots with 7 crossings, 19 of 21 with 8, 30 of 49 with 9, 103 of 165 with 10, 278 of 552 with 11 |
| $`\vec{F}_3`$ | n = 11 | all knots with ≤ 11 crossings; 2173 of 2176 with 12; 9734 of 9988 with 13 |

**Where to find the values** (a guide to all the files is in [`results/README.md`](results/README.md)):
- the final tables, with a representative of every knot in normal form and as a tree diagram:
  [`results/F_index_table.md`](results/F_index_table.md), [`results/F3_index_table.md`](results/F3_index_table.md),
  [`results/Fvec_index_table.md`](results/Fvec_index_table.md),
  [`results/F3vec_index_table.md`](results/F3vec_index_table.md) (also as `.csv`);
- the oriented indices (K, $`K^r`$, $`K^m`$, $`K^{mr}`$) of the non-invertible knots:
  [`results/oriented_index_Fvec.md`](results/oriented_index_Fvec.md),
  [`results/oriented_index_F3vec.md`](results/oriented_index_F3vec.md);
- knots with ≤ 9 crossings, all four indices side by side: [`results/Fvec_index_upto9.md`](results/Fvec_index_upto9.md).

The files `results/<G>_index.csv` are working files (one row per KnotInfo knot, also those not found, with the
exact lower bound): they have no normal forms.

Checked on the final tables (`tests/check_index_inequalities.py`), for every knot:
- F₃-index ≤ F-index;
- F₃-index ≤ $`\vec{F}_3`$-index ≤ $`\vec{F}`$-index;
- F-index ≤ $`\vec{F}`$-index;
- span V + 1 ≤ F-index ≤ $`\vec{F}`$-index, V the Jones polynomial (a theorem of the paper; `jones_span_bound.py`,
  `results/jones_span_bound.md`). The bound is attained by 1440 knots for F (the first is 7_4, with F-index 8)
  and by 8 knots for $`\vec{F}`$; for them the index is proved by the witness alone.

### Certified verification

**All the values of the four tables are certified** by exact or interval-arithmetic computations, with no
contradiction (`certify_indices.py`, `certify_retry.py`, `certify_completeness.py`; results in
`results/certified_<G>.md`, `results/certified_retry_<G>.md`, `results/certified_completeness_<G>.md`).
- **Witnesses**: the witness diagram of size n is K. We show that the complement of its knot is homeomorphic
  to the complement of K; by the theorem of Gordon and Luecke, the two knots are then equal up to mirror image.
  The homeomorphism is found in one of three ways:
  - *Canonical triangulations* (hyperbolic knots, almost all cases). SnapPy computes, with verified
    arithmetic, the canonical triangulation of each complement, which depends only on the manifold; a
    combinatorial isomorphism between the two triangulations gives the homeomorphism.
  - *Isomorphism signatures* (when the first method is too slow, and for satellite knots). Each
    triangulation is changed at random by moves that do not change the manifold, until the two complements
    reach the same triangulation, i.e. the same isomorphism signature. This proves the homeomorphism; it
    uses no hyperbolic geometry.
  - *KnotInfo* (a few torus knots). The simplified witness has at most 13 crossings, so its knot is in
    KnotInfo, where it is identified.

  Witnesses certified: 6049 (F), 11320 (F₃), 2155 ($`\vec{F}`$) and 12708 ($`\vec{F}_3`$).
- **Exclusions** (no smaller diagram is K): every diagram of the HOMFLY class of K between its first appearance
  and the index is shown not to be K by its crossing number, by being a connected sum of non-trivial knots
  (K is prime), by knot Floer homology, by the verified volume, by the verified canonical triangulation, or
  by an essential torus found by Regina. 27857 (F), 26847 (F₃, with the RIII–RII reduction), 390776
  ($`\vec{F}`$) and 14265 ($`\vec{F}_3`$) diagrams.
- **Completeness**: every knot with a known index has a certified witness, every knot whose index exceeds the
  first appearance of its HOMFLY class is in the complete check, and all the diagrams of these classes in the
  relevant range are excluded. The only non-certified ingredient is the exact enumeration of the diagrams and
  of their HOMFLY polynomials.

### Targeted searches

Single open cases beyond the enumeration (`descent_jobs.py`, `descent_search.py`, `certify_descent.py`,
`apply_descent.py`): from known diagrams of a knot, delete s + 1 internal vertices and insert one in each tree
(s = 1 in F and F₃, 2 in the oriented groups), keep the pairs in the group, filter by determinant, number of
components and volume, and compare with the knot (SnapPy); every diagram found is certified
(`results/descent_certified.csv`, 1934 diagrams, all certified). Results: F₃-index 10 for 12 of the 14 knots
with 12 crossings not found with n ≤ 9 (12a_868, 12a_875, 12a_928, 12a_1019, 12a_1020, 12a_1050, 12a_1113,
12a_1152, 12a_1196, 12a_1209, 12a_1285, 12a_1286; 12a_883 and 12a_975 are 10 or 11, by their
$`\vec{F}_3`$ witness); F₃-index 10 for 644 of the 1467 knots with 13 crossings not found with n ≤ 9 that
have a $`\vec{F}_3`$ witness at 11 (307 starting from the witness, `descent_jobs.py --f3-13`; 337 more in a second
round from at most 5 other stored diagrams, `descent_jobs.py --f3-13-more --max-starts 5`); $`\vec{F}_3`$-index 13 for 12a_1211, 13 or 15 for 12a_1249;
F-index 14 or 15 for 11a_249; the other orientation of the 56 + 24 one-sided knots above. `apply_descent.py`
writes them into the tables (status "targeted search").

### Second computation

All four tables were computed a second time from scratch (2026-11-03/04) with `pipeline.py` and the current
code: faster identification, crossing-number test first, exact tests only in `resolve_undecided.py`, all
non-prime diagrams skipped, and the RIII–RII reduction for F₃. The indices, the lower bounds and the oriented
values (K, Kr, Km, Kmr) agree with the first computation for every knot; some witnesses differ (37 for
$`\vec{F}_3`$, 1 for $`\vec{F}`$, 51 for F₃, 2 for F) and are certified. For F₃ with n ≤ 9 the RIII–RII
reduction gives the same 59076 HOMFLY classes at n = 9. The results in `results/` are those of the second
computation. Running times on an 8-core Mac (2020): F (n ≤ 13) 1 h 18 min, F₃ (n ≤ 9) 1 h 42 min,
$`\vec{F}`$ (n ≤ 17) 4 h 50 min, $`\vec{F}_3`$ (n ≤ 11) 2 h 13 min, certification included.

### Oriented indices

For an oriented knot K write $`K^r`$ for its reverse, $`K^m`$ for its mirror image and $`K^{mr}`$ for both.
- **The inverse rule.** L(g⁻¹) is the mirror image of the reverse of L(g), in $`\vec{F}`$ and in $`\vec{F}_3`$ (`results/inverse_rule.md`; for $`\vec{F}`$ this is Aiello–Conti, CAOT 13 (2019), Remark 3.8).
  Hence index(K) = index($`K^{mr}`$) and index($`K^r`$) = index($`K^m`$).
- **Invertible knots** (K = $`K^r`$): the four values coincide.
- **Non-invertible knots**: `oriented_scan.py` computes index(K) and index($`K^r`$) from all the diagrams.

**K and $`K^r`$ can have different indices:**
- In $`\vec{F}`$, non-invertible knots with ≤ 13 crossings, n ≤ 17 (`results/oriented_index_Fvec.md`), 1308 knots:
  - 85 have both orientations realized with different indices: 13/15 for 10_88, 12n_18, 12n_49, …;
    15/17 for 10_93, 10_102, 11a_26, …;
  - 226 have one orientation with index 17 and the other not realized with n ≤ 17 (e.g. 10_95); by the
    moves in the proof of Theorem 4.2 of Aiello, Rev. Un. Mat. Argentina 69 (2026) (which gives $`{|\mathrm{ind}(K)-\mathrm{ind}(K^r)|\le 4}`$), the other orientation has index exactly 19 for 170 of
    them; for the other 56 a targeted search (`descent_search.py`, see below) found a certified diagram with 19
    leaves of the other orientation, so it is exactly 19 for all 226 (`results/reverse_bound_Fvec.csv`);
  - 8_17, 9_32 and 9_33 have equal indices.
- In $`\vec{F}_3`$, n ≤ 11 (`results/oriented_index_F3vec.md`), 8121 knots:
  - 710 have both orientations realized with different indices;
  - 236 have one orientation > 11; by the ternary reverse moves (paper, Theorem 3.2(vii)) the other
    orientation has index exactly 13 for 212 of them (for 30, through another minimal diagram found by
    `reverse_search_F3vec.py`), and for the other 24 by a certified diagram of size 13 found by a targeted
    search: exactly 13 for all 236 (`results/reverse_bound_F3vec.csv`);
  - the smallest example is **8_17**: $`\vec{F}_3`$-index 7 for K = $`K^{mr}`$ and 9 for $`K^r`$ = $`K^m`$. Its $`\vec{F}`$-index is 13 for both.

All these results are **certified**: every exclusion was checked again with exact or interval-arithmetic
methods (knot Floer homology, verified volumes, verified canonical triangulations), see `verify_oriented.py`
and `results/oriented_verified_Fvec.md`, `results/oriented_verified_F3vec.md`.

### Mutants

The $`\vec{F}`$-index distinguishes the Conway knot 11n_34 (≥ 19) from its mutant, the Kinoshita–Terasaka
knot 11n_42 (15), whatever the orientations (`results/mutants.md`).
- The proof is certified by the Seifert genus (knot Floer homology): all 2580 diagrams of their HOMFLY
  class with n ≤ 17 have genus 2, while 11n_34 has genus 3.
- The F-, F₃- and $`\vec{F}_3`$-indices of the two knots coincide.

### Comparison with classical invariants

`results/index_bounds.md` (script `index_bounds.py`):
- **Braid index.** Luo–Wan (arXiv:2408.10875, Theorem 1.15) prove braid ≤ F-index. On the data, braid < index
  holds for all four indices, with no equality for any non-trivial knot; for F₃ six knots have index = braid + 1.
- **Crossing number.** Golan–Sapir (arXiv:1501.00724, Lemma 6.11) prove F-index ≤ 12c; on the data F-index ≤ c + 3.
  The trivial bound c ≤ 2(index − 1) is attained by 105 knots for F₃ and 3 for $`\vec{F}_3`$, never for F or $`\vec{F}`$.

### The Borromean rings

Jones asked for the F- and F₃-indices of the Borromean rings (On the construction of knots and links from
Thompson's groups, 2019, Section 7). They are **9** (F, as already found by D. Sweeney) and **6** (F₃);
in Jones' normalization, which counts internal vertices, 8 and 5 (`borromean.py`, `results/borromean.md`).

### Other results

- **Parity theorem.** For g in $`\vec{F}`$ or $`\vec{F}_3`$ the number of components of L(g) is ≡ n mod 2, so
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

  His oriented data (all diagrams of $`\vec{F}`$ up to 11 leaves, unlabelled) agree with ours.

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

The whole computation of one index, phase after phase, is run by `pipeline.py`, which times every phase
(`results/logs/pipeline_<G>.log`) and resumes after the last completed phase:

```bash
python3 pipeline.py F3vec 11 --jobs 8      # enumerate, identify, complete check, resolve, apply, table,
                                           # oriented scan, reverse bound, verify, certify (dry run: --dry-run)
```

The scripts write to `results/` and `tmp_check/`: to keep existing results, run the pipeline in a separate
checkout (`git worktree add ../F_index_rerun`, then `make` there); without `--force` it refuses to overwrite
`results/<G>_index.csv`. Long runs: `caffeinate -i python3 pipeline.py ...` keeps the Mac awake.
The progress files of a phase (in `tmp_check/` and `results/raw*/`) are reused only to resume that phase after
an interruption; in every other case (a new run, `--from`, `--only`) they come from an earlier run, possibly
with older code, and the pipeline moves them (never deletes them) to `tmp_check/old_<G>_<date-time>/`.

The single phases:

```bash
make                                  # bin/fknots, bin/iota_knots (link SageMath's libhomfly; set SAGE_LOCAL)
python3 run.py 13                     # F: enumerate n = 2..13 in parallel  -> results/raw/n<n>.tsv
python3 run.py 9  --group F3          # F₃                                   -> results/raw_F3/
python3 run.py 17 --group Fvec        # vec{F}                               -> results/raw_Fvec/
python3 run.py 11 --group F3vec       # vec{F}₃                              -> results/raw_F3vec/
sage identify.sage 13 [F|F3|Fvec|F3vec]                # identify the knots  -> results/<G>_index.csv
sage -python complete_check.py <G>                     # all diagrams of the classes found late / not found
sage -python resolve_undecided.py <G>                  # second pass on the undecided diagrams
sage -python apply_complete_check.py <G>               # apply the complete check to <G>_index.csv
sage -python certify_indices.py <G> [procs]            # certified verification of the table
sage -python certify_retry.py <G> [procs] [timeout]    # second pass on what the first one left open
sage -python certify_completeness.py [<G>]             # every value certified?
sage -python jones_span_bound.py                       # comparison with the Jones span bound
python3 make_table.py <G>                              # final table -> results/<G>_index_table.md
python3 small_knots_table.py                           # all four indices, knots with <= 9 crossings
sage -python oriented_scan.py Fvec|F3vec [procs] [maxc]  # oriented indices of the non-invertible knots
```

Notes:
- `run.py` skips the values of n already computed, so a run can be resumed or extended.
- `complete_check.py`, `resolve_undecided.py` and `oriented_scan.py` keep their progress in `tmp_check/` and
  resume after an interruption.
- `identify.sage` needs `sage -pip install database_knotinfo snappy`.
- `identify.sage` does not name the HOMFLY classes of no table knot (`unidentified_classes*.csv`), which are not
  needed for the tables; `NAME_REPS=1 sage identify.sage ...` names them.
- The raw data (`results/raw*/`, several GB) and `tmp_check/` are not in git.

Running times on an 8-core Mac (2020), $`\vec{F}_3`$ with n ≤ 9: the whole pipeline takes about 31 minutes
(identification 13 min, complete check 2 min, certification 9 min, the rest a few minutes). Before the
identification by SnapPy first (2026-11) the same run took 1 h 28 min. For n = 11 the enumeration takes about
47 min and the identification about one hour.

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
- the map ι (a caret becomes a ternary caret with an empty middle leaf) sends F into F₃ and $`\vec{F}`$ into $`\vec{F}_3`$, preserving the oriented knot, so the index for F₃ is at most the one for F.

The oriented diagrams are built by `oriented.py` (`oriented_pd_code`, `oriented_pd_code3`).

### Reductions of the enumeration

The reductions are not the same in the four groups:

| reduction | F | F₃ | $`\vec{F}`$ | $`\vec{F}_3`$ |
|---|---|---|---|---|
| (T₊, T₋) ↦ (T₋, T₊), i.e. g ↦ g⁻¹ (mirror image; for the oriented groups the mirror reverse) | yes | yes | yes | yes |
| (T₊, T₋) ↦ (σT₊, σT₋), the vertical reflection (mirror image) | yes | yes | **no** (does not preserve $`\vec{F}`$) | **no** (does not preserve $`\vec{F}_3`$: it swaps black and white regions) |
| skip non-prime diagrams (a non-root subtree of T₊ and one of T₋ cover the same leaves) | yes | yes | yes | yes (see below) |
| skip the diagrams with an admissible RIII–RII reduction (paper, Section 3) | – | yes | – | – |
| keep only knots (one component) | yes | yes | yes (odd n only) | yes (odd n only) |

- **Symmetries.** One representative per orbit is kept. The oriented scan accounts for g⁻¹ through the
  inverse rule, and checks that rule directly on thousands of diagrams.
- **Primality.**
  - A non-prime diagram is a graft, i.e. a connected sum, so a prime knot is already realized with fewer
    leaves.
  - In the oriented groups a piece may lie outside the group, or carry the opposite orientation. All the
    non-prime diagrams can nevertheless be skipped: if a non-prime diagram with k leaves realizes a prime
    oriented knot J, then J or its reverse is realized with at most k − 4 leaves, and the reverse moves
    (ind(K^r) ≤ ind(K) + 2 or + 4) bound the other orientation (paper, Section 3, Lemma and Corollary on
    non-prime diagrams).
  - `bin/iota_knots` skips all of them by default. The runs whose results are in `results/` used an older,
    weaker rule in $`\vec{F}_3`$: a non-prime diagram was skipped only if the common interval starts at an
    even leaf (numbering the leaves from 0). To reproduce them exactly, set `THOMPSON_OLD_NONPRIME_RULE=1`.
    The two rules give the same tables: none of the 12,708 witnesses of the $`\vec{F}_3`$-index and of the
    16,006 oriented witnesses is a non-prime diagram. The additional non-prime diagrams are nearly never
    knots (n = 11: 2.9 million of 136.9 million knot diagrams), but building their links takes time:
    skipping them halves the pairs of trees whose link is built and reduces the enumeration for n = 11
    from 47 to 32 minutes, with the same 710,516 HOMFLY-PT classes.
  - Composite knots can still arise from prime diagrams, e.g. the granny and square knots at n = 9 in F.
- **RIII–RII reductions (F₃).** A ternary diagram whose signed Tait trees admit the RIII–RII reduction of the
  paper (Section 3) gives the same link as a diagram of size n − 1, so it is skipped (`THOMPSON_NO_RIII_RII=1`
  disables it). For n = 8 this skips 27% of the knot diagrams; the first n of every HOMFLY class is unchanged.
  It does not apply to $`\vec{F}_3`$ (the reduced Tait graph is not 2-colourable) nor to F.
- **HOMFLY.** It is computed after a Reidemeister I and II simplification, with a cache on the simplified
  Gauss codes.

### Identification and complete check

1. **Raw data.** For every n the enumerator gives one line per HOMFLY class (up to mirror image), with the
   number of diagrams and up to 50 representatives.
2. **First identification.** `identify.sage` identifies the stored representatives.
   - Every representative goes first to SnapPy (complement identification, census up to 15 crossings), with
     a 2 s timeout: it is about 40 times faster than Sage's `get_knotinfo()`. SnapPy names the knots with
     ≤ 10 crossings as in Rolfsen's table, whose numbering differs from KnotInfo's (10_83 / 10_86, and
     10_162–10_166 after the Perko pair); these names are translated with `results/rolfsen_to_knotinfo.json`
     (written by `rolfsen_names.py` from the KnotInfo diagrams).
   - When SnapPy gives no name (torus, satellite or composite knots, or a timeout), a diagram with ≤ 13
     crossings goes to `get_knotinfo()`, and then SnapPy is tried again with a longer timeout.
   - A HOMFLY match alone is not enough on diagrams with more than 13 crossings: at n = 10 a class has the
     HOMFLY of 13n_2638, but its knot is 14n_2554.
   - Every identification is certified afterwards (Certified verification above).
3. **Complete check.** Only 50 representatives per class are stored, so a knot can hide in a large class:
   10_132 was missed at n = 9, and 13n_2290 was found at 13 instead of 11. `complete_check.py` therefore
   enumerates **every** diagram of the classes of the knots found after their class first appears, or not
   found at all. Each diagram is compared with the knot: hyperbolic volume first, then a SnapPy isometry. A
   diagram with no hyperbolic structure after 50 randomizations, compared with a hyperbolic knot, is left
   to step 4 (faster than naming it).
4. **Undecided diagrams.** Some diagrams have no hyperbolic structure (SnapPy finds none), so step 3 cannot
   compare them with the knot K being sought. They are treated by `resolve_undecided.py`: such a diagram is
   not K if its knot Floer homology differs from that of K, or if its complement contains an essential torus
   (it is then a satellite knot, while K is hyperbolic). No diagram is left undecided in the current results
   (`results/complete_check_<G>.md`). All the conclusions of steps 3–4 were checked again with certified
   methods only (see Certified verification above).
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
- `results/<G>_index_table.md`: index, KnotInfo name and a representative, as a tree diagram and in normal
  form x₀^a₀ ⋯ x_k^a_k x_k^-b_k ⋯ x₀^-b₀ (generators x_i of F for F and $`\vec{F}`$, y_i of F₃ for F₃ and
  $`\vec{F}_3`$, with y₂ₘ = ι(xₘ); see `make_table.py`). Every normal form is checked: for F by multiplying
  the generators, for F₃ by comparing the piecewise linear maps of [0, 1] (exact arithmetic).
- `results/knots_beyond_table*.csv`: knots with 14–15 crossings recognized by SnapPy (upper bounds).
- `results/unidentified_classes*.csv`: HOMFLY classes of no prime knot with ≤ 13 crossings.

## Files

| file | content |
|---|---|
| `ftrees.py` | reference implementation in Python: trees, Tait graph, PD code, product in F |
| `oriented.py` | oriented links for $`\vec{F}`$ and $`\vec{F}_3`$, oriented comparison of knots (SnapPy isometries on meridian and longitude) |
| `src/fknots.cpp` | fast enumerator for F and $`\vec{F}`$ (`vec`): symmetries, primality, components, HOMFLY (libhomfly); `-1` = all diagrams of given classes |
| `src/iota_knots.cpp` | enumerator for F₃ and $`\vec{F}_3`$ (`F3vec`); with `F` it maps binary trees by ι (an independent cross-check of `fknots`) |
| `pipeline.py` | all the phases of one index, with timings and resumption |
| `run.py` | parallel enumeration |
| `identify.sage`, `identify_lib.py` | identification with SnapPy and KnotInfo (crash-tolerant process pool `RobustPool`) |
| `rolfsen_names.py` | SnapPy's Rolfsen names → KnotInfo names (`results/rolfsen_to_knotinfo.json`) |
| `complete_check.py`, `resolve_undecided.py`, `apply_complete_check.py` | complete check over all diagrams of the relevant HOMFLY classes |
| `certify_indices.py`, `certify_retry.py`, `certify_completeness.py` | certified verification of all the tables |
| `jones_span_bound.py` | comparison with the bound span V + 1 ≤ F-index ≤ $`\vec{F}`$-index |
| `make_table.py`, `small_knots_table.py` | final tables |
| `oriented_scan.py` | oriented indices (K, $`K^r`$, $`K^m`$, $`K^{mr}`$) of the non-invertible knots |
| `reverse_bound.py`, `reverse_bound_F3vec.py`, `reverse_search_F3vec.py` | index of the unrealized orientation by the reverse moves |
| `reverse_scan.py`, `oriented_index.py`, `verify_reverse.py`, `reverse_examples.py` | earlier tools for K vs $`K^r`$ in $`\vec{F}`$ |
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

1. V. Aiello, *On the Alexander theorem for the oriented Thompson group* $`\vec{F}`$, Algebr. Geom. Topol. 20
   (2020), 429–438.
2. V. Aiello, *An introduction to Thompson knot theory and to Jones subgroups*, J. Knot Theory Ramifications
   34 (2025), 2340002.
3. V. Aiello, T. Nagnibeda, *On the oriented Thompson subgroup* $`\vec{F}_3`$ *and its relatives in higher
   Brown–Thompson groups*, J. Algebra Appl. 21 (2022), 2250139.
4. J. Belk, *Thompson's group F*, Ph.D. thesis, Cornell University (2004),
   [arXiv:0708.3609](https://arxiv.org/abs/0708.3609).
5. K. S. Brown, *Finiteness properties of groups*, J. Pure Appl. Algebra 44 (1987), 45–75.
6. J. W. Cannon, W. J. Floyd, W. R. Parry, *Introductory notes on Richard Thompson's groups*, Enseign. Math.
   (2) 42 (1996), 215–256.
7. G. Golan, M. Sapir, *On Jones' subgroup of R. Thompson group F*, J. Algebra 470 (2017), 122–159.
8. V. F. R. Jones, *Some unitary representations of Thompson's groups F and T*, J. Comb. Algebra 1 (2017),
   1–44.
9. V. F. R. Jones, *On the construction of knots and links from Thompson's groups*, in: Knots,
   low-dimensional topology and applications, Springer Proc. Math. Stat. 284 (2019), 43–66.
