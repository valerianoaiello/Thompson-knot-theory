# Results

Where to find the values of the indices. G is one of `F`, `F3`, `Fvec`, `F3vec`.

## The indices of the knots: start here

| file | content |
|---|---|
| `<G>_index_table.md` (and `.csv`) | **the final tables**: one row for each knot with known index, sorted by index, with a representative: its **normal form** and its tree diagram |
| `oriented_index_Fvec.md`, `oriented_index_F3vec.md` (and `.csv`) | **oriented indices** of the non-invertible knots: index of K, $`K^r`$, $`K^m`$, $`K^{mr}`$, with witnesses |
| `Fvec_index_upto9.md`, `Fvec_index_upto10.md` | the four indices of the knots with at most 9 (10) crossings, side by side |
| `connected_sums.md` | indices of the granny knot, the square knot and 3_1 # 4_1 |
| `borromean.md` | the Borromean rings |

How to read the tables:
- Knots are unoriented and listed up to mirror image, with KnotInfo names. In `Fvec` and `F3vec` the table gives
  the smallest index of the two orientations; the oriented values are in `oriented_index_<G>.md`.
- A knot that is not listed has index larger than the largest n enumerated (stated at the top of each table), except
  the knots found beyond it by the targeted searches (status "targeted search" in `<G>_index.csv`).
- Normal form: $`x_0^{a_0}\cdots x_k^{a_k}x_k^{-b_k}\cdots x_0^{-b_0}`$, in the generators $`x_i`$ of F for `F` and
  `Fvec`, and in the generators $`y_i`$ of $`F_3`$ for `F3` and `F3vec` ($`y_{2m}=\iota(x_m)`$; the convention is in
  `make_table.py`). Every normal form is checked against the tree diagram.
- Tree diagram: leaf addresses of the top tree and of the bottom tree, from left to right; 0 = left, 1 = right for
  binary trees, and 0 = left, 1 = middle, 2 = right for ternary trees.
- Size n: number of leaves of each binary tree; for ternary trees, number of internal vertices of each tree + 1.

## Working files

| file | content |
|---|---|
| `<G>_index.csv` | one row for every KnotInfo knot, also those not found: index, exact lower bound (first n of the HOMFLY-PT class), status, witness (leaf addresses), HOMFLY-PT polynomial. Read by the other scripts; no normal forms |
| `<G>_index_summary.txt` | number of knots with known index, by crossing number |
| `knots_beyond_table*.csv` | knots with 14 or 15 crossings recognized by SnapPy (upper bounds) |
| `unidentified_classes*.csv` | HOMFLY-PT classes of no prime knot with at most 13 crossings |
| `complete_check_<G>.md` / `.csv` | the complete check (all diagrams of the relevant HOMFLY-PT classes) |
| `certified_<G>.md`, `certified_retry_<G>.md`, `certified_completeness.md` | the certified verification of all the tables |
| `oriented_verified_<G>.md` | the certified verification of the oriented results |
| `jones_span_bound.md` / `.csv`, `index_bounds.md` | comparison with the Jones polynomial, braid index, crossing number, genus |
| `mutants.md`, `mutants_literature.csv`, `mutant_candidates.csv` | mutant knots |
| `reverse_bound_Fvec.csv`, `reverse_bound_F3vec.csv`, `inverse_rule.md`, `parity_theorem.md` | K versus $`K^r`$ in $`\vec{F}`$ and $`\vec{F}_3`$ (value of the unrealized orientation from the reverse moves); the rule for $`g^{-1}`$; the parity theorem |
| `Fvec_n19_classes.csv` | $`\vec{F}`$ at n = 19: number of knot diagrams in the HOMFLY-PT class of every knot not found with n ≤ 17 (0: index ≥ 21) |
| `Fvec_beyond17_witnesses.csv`, `Fvec_beyond17_certified.md` | $`\vec{F}`$: the witnesses with 19 and 21 leaves and their certification |
| `descent_certified.csv` | all the certified diagrams of the targeted searches |
| `sweeney_corrections.md` | comparison with D. Sweeney's table |
| `logs/` | logs of the runs |

The other files are older intermediate results, kept for reference.
