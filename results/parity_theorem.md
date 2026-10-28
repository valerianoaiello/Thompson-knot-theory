# Parity theorem for vec{F}

**Theorem.** If g = (T+, T-) is in vec{F} and has n leaves, the number of components of L(g) is congruent
to n mod 2. In particular every knot L(g), g in vec{F}, comes from an odd number of leaves, and the
vec{F}-index of a knot is odd.

**Proof.**
1. The Tait graph Gamma = Gamma(T+, T-) is a plane graph with n vertices. Each tree gives n - 1 edges forming
   a spanning tree, so Gamma is connected with 2(n - 1) edges, and it has n faces by Euler's formula.
2. L(g) is the medial link of Gamma, so its components are the left-right (straight-ahead) cycles of Gamma.
   For a connected plane graph G their number is dim B(G) + 1, where B(G) is the bicycle space (cycles that
   are also cuts, over GF(2)) (Rosenstiehl-Read; see Godsil-Royle, *Algebraic Graph Theory*, Ch. 17).
   A cut d(S) is a cycle iff L·1_S = 0 over GF(2), L the Laplacian, and d(S) = d(V \ S); so
   dim B(G) + 1 = dim ker (L mod 2). The medial link of G and of its dual G* are the same curves, so
   c(L(g)) = dim ker (L(Gamma*) mod 2).
3. g is in vec{F} iff Gamma is bipartite (the leaf-parity criterion). Then every closed walk of Gamma is even,
   in particular every face boundary, so every vertex of Gamma* has even degree. Hence the Laplacian of Gamma*
   mod 2 is symmetric with zero diagonal, i.e. alternating, and has even rank. Gamma* has n vertices, so
   c(L(g)) = n - rank, which is congruent to n mod 2.  ∎

**Numerical check.** `python3 tests/check_parity.py 9`: for all 2,248,355 tree diagrams of F with n <= 9 it
checks the edge and face counts, c = dim ker L(Gamma) = dim ker L(Gamma*) mod 2, vec{F} iff bipartite, and,
for the 34,409 elements of vec{F}, that Gamma* is Eulerian and c = n mod 2. All pass. The enumeration of
vec{F} (`fknots ... vec`) also found no knot for any even n <= 16.

**Consequence.** Since vec{F} is enumerated up to n = 17, a knot not found has vec{F}-index >= 19.
