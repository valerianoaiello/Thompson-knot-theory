# F-index of knots (Jones' construction, unoriented case)

For every n = 2, 3, … we enumerate all binary tree diagrams (T₊, T₋) with n leaves, build the knot
L(T₊, T₋) and compute its HOMFLY polynomial; the knots are then recognized in the KnotInfo table
(prime knots up to 13 crossings). The F-index of K is the first n at which K appears.

## Usage

```bash
make                      # builds bin/fknots and bin/iota_knots (uses SageMath's libhomfly)
python3 run.py 13         # enumerates n = 2..13 in parallel  -> results/raw/n<n>.tsv
sage identify.sage 13     # recognizes the knots              -> results/F_index.csv
sage tests/check_cpp.sage # checks the C++ code against the reference implementation
python3 make_table.py      # final table: F-index, KnotInfo name, representative -> results/F_index_table.md
```

`run.py` skips the values of n already computed, so a run can be resumed or extended
(`python3 run.py 14`).
`sage` is `/Applications/SageMath-10-8.app/Contents/Frameworks/Sage.framework/Versions/Current/venv/bin/sage`.
`identify.sage` needs the packages `database_knotinfo` and `snappy` in Sage's Python
(`sage -pip install database_knotinfo snappy`).

**$\vec{F}$-index (oriented subgroup).** Jones' oriented subgroup $\vec{F} \le F$ consists of the tree diagrams whose
Tait graph is 2-colourable. Equivalently, every leaf has the same parity of right edges on the path from
the root in T₊ and in T₋ (checked in `tests/check_vecF.sage`). The colouring orients the knot.

```bash
python3 run.py 13 --group Fvec       # -> results/raw_Fvec/n<n>.tsv   (bin/fknots ... vec)
sage identify.sage 13 Fvec           # -> results/Fvec_index.csv, ...
python3 make_table.py Fvec           # -> results/Fvec_index_table.md
```

The vertical reflection does not preserve $\vec{F}$, so in this mode the only symmetry used is g ↔ g⁻¹
(which gives the mirror image). Knots only arise for odd n: for $g \in \vec{F}$ the number of components of L(g)
has the parity of n. The $\vec{F}$-index is an index of oriented knots. `results/Fvec_index.csv` lists
the knots up to mirror image and reversal, i.e. min(index K, index Kr), which is the oriented index of
every invertible knot; for the non-invertible knots `oriented_scan.py` gives the values for K, Kr, Km and
Kmr (`results/oriented_index_Fvec.md`). The same holds for the $\vec{F}_3$-index (`--group F3vec`,
`results/oriented_index_F3vec.md`).

**F₃-index.** The same pipeline works for the Brown–Thompson group F₃, with ternary tree diagrams:

```bash
python3 run.py 9 --group F3          # -> results/raw_F3/n<n>.tsv   (bin/iota_knots)
sage identify.sage 13 F3             # -> results/F3_index.csv, F3_index_summary.txt, unidentified_classes_F3.csv
```

Here n is the number of internal vertices of each ternary tree plus one, as in the definition of
the F₃-index: a binary tree diagram with n leaves is mapped by ι to a ternary one with the same n,
so F₃-index ≤ F-index.

## Files

| file | content |
|---|---|
| `ftrees.py` | reference implementation in Python (slow but readable): trees, Tait graph, PD code, product in F |
| `src/fknots.cpp` | fast enumerator: symmetries, primality, components, simplification, HOMFLY (libhomfly) |
| `src/iota_knots.cpp` | enumerator for F₃ (ternary trees; each internal vertex is a crossing, left–right strand over); with `F` it maps binary trees by ι and gives an independent cross-check of `fknots` |
| `run.py` | runs `fknots` (or `iota_knots` with `--group F3`) on several processes and merges the results |
| `identify.sage`, `identify_lib.py` | comparison with KnotInfo / SnapPy and computation of the F-index (or F₃-index), in parallel on all the cores (optional 3rd argument: number of processes); worker processes that crash inside SnapPy are restarted |
| `tests/check_cpp.sage` | checks: Example 2.3 of the paper (4₁) and C++ / Python / Sage agreement for n ≤ 7 |
| `tests/check_graft_and_old_code.sage` | grafting = connected sum, agreement with `../vecchio codice` up to mirror |
| `tests/check_iota_engine.sage` | checks of `iota_knots`: Sage agreement on random F and F₃ diagrams, old code, Example 2.3, and same counts and HOMFLY classes as `fknots` for n ≤ 8 |
| `results/cross_check_iota_construction/` | results of the independent implementation via ι into F₃ (n ≤ 10), same HOMFLY classes |

Construction (see `ftrees.py`): the Tait graph Γ(T₊, T₋) has vertices 0, …, n−1 (0 = the region to the
left of leaf 0, j = the gap between leaves j−1 and j); every internal vertex of a tree whose left
subtree covers the leaves [a, j−1] gives an edge (a, j), positive in T₊ and negative in T₋. The knot is
the link whose Tait graph is Γ. Everything is defined up to mirror image.

Reductions of the enumeration:

* **symmetries**: (T₊, T₋) ↦ (T₋, T₊) and (T₊, T₋) ↦ (σT₊, σT₋) (horizontal and vertical reflections)
  give the mirror image; one representative per orbit is kept;
* **primality**: diagrams obtained by gluing a tree diagram with ≥ 2 leaves in place of a pair of
  leaves of another tree diagram with ≥ 2 leaves are skipped, i.e. those where a non-root subtree of
  T₊ and one of T₋ cover the same leaves (this includes non-reduced diagrams). Such a knot is a
  connected sum, so a prime knot is already realized with fewer leaves. Note that composite knots can
  still arise from prime diagrams (e.g. granny and square knots at n = 9);
* **one component**: only knots are kept;
* HOMFLY is computed after a Reidemeister I and II simplification, with a cache on the simplified
  Gauss codes.

## Output

`results/raw/n<n>.tsv`: one line per class of HOMFLY polynomials (up to mirror) with the number of
diagrams, the minimal number of crossings after simplification and up to 50 representatives
`T₊|T₋|simplified Gauss code` (trees are given by the addresses of their leaves, 0 = left, 1 = right,
as in the old code).

`results/F_index.csv`, for every knot of the table:

* `F_index`: exact value, when a representative with that number of leaves is recognized as that knot.
  The diagram is first simplified further with spherogram (SnapPy) and then given to Sage's
  `Link.get_knotinfo()` (if it has ≤ 13 crossings). If that fails or is ambiguous, because several
  knots of the table share the HOMFLY polynomial (e.g. 4₁ # 4₁ and 12n₄₆₂), SnapPy identifies the knot
  complement. The SnapPy census covers knots up to 15 crossings, and by Gordon–Luecke the complement
  determines the knot up to mirror image. All the stored representatives of the class are tried,
  since one HOMFLY class can contain several knots (e.g. 10₁₅₆ and 13n₂₆₃₈ at n = 10);
* `lower_bound`: the first n at which a diagram with the same HOMFLY appears (no diagram with fewer
  leaves can give the knot); if the knot never appeared it is max(n_max + 1, ⌈c/2⌉ + 1), since a tree
  diagram with n leaves has 2n − 2 crossings;
* `top_tree`, `bottom_tree`: a tree diagram realizing it.

`results/unidentified_classes.csv`: HOMFLY classes of no prime knot with ≤ 13 crossings (composite
knots, or knots with more than 13 crossings). The column `knots` names them from up to 5
representatives: KnotInfo for composite knots (e.g. `3_1 # 3_1`), SnapPy for prime knots with 14–15
crossings (e.g. `14n_6950`), `non-hyperbolic` or `?` otherwise. Composite names are up to mirror of
each factor, so they do not distinguish the granny knot from the square knot.

`results/F_index_table.md` / `.csv` (from `make_table.py`): one row per knot with its F-index, its
KnotInfo name and a representative realizing the index, both as an element of F in normal form
(x₀^a₀ ⋯ x_k^a_k x_k^-b_k ⋯ x₀^-b₀, checked by multiplying the generators with `ftrees.py`) and as a
tree diagram. `results/table_n10/` holds the same table for n ≤ 10.

`results/knots_beyond_table.csv`: knots with 14 or 15 crossings recognized by SnapPy (outside KnotInfo),
with the first n at which one of the stored representatives realizes them. Since only up to 50
representatives per class are stored, this n is an upper bound for their F-index; the lower bound is
the first n at which their HOMFLY appears.

Note on the identification: `get_knotinfo` is only used on diagrams with ≤ 13 crossings. Then the knot
has crossing number ≤ 13, so it is in KnotInfo and a HOMFLY match is a proof. On larger diagrams a
HOMFLY match is not enough: at n = 10 a class has the HOMFLY of 13n₂₆₃₈, but SnapPy shows that its
knot is 14n₂₅₅₄.

## History

This repository (`Thompson-knot-theory`) also contains, in its git history, the earlier Python implementation
of the project (up to commit `c79ea62`, February 2025). It was merged into this history when the current
code (C++ enumerators, identification with KnotInfo and SnapPy, complete checks, oriented indices)
replaced it; its files are no longer in the working tree.
