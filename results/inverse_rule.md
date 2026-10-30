# The inverse rule: L(g⁻¹) is the mirror image of the reverse of L(g)

**Proposition.** Let g = (T₊, T₋) be in vec{F} or in vec{F}₃, and let L⃗(g) be its link, oriented by the
colouring of the Tait graph. Then g⁻¹ = (T₋, T₊) is in the same group, and

  L⃗(g⁻¹) = (L⃗(g)ʳ)*,

the mirror image of L⃗(g) with all orientations reversed.

For vec{F} this is Aiello–Conti, *The Jones polynomial and functions of positive type on the oriented
Jones–Thompson groups F⃗ and T⃗*, Complex Anal. Oper. Theory 13 (2019), Remark 3.8. The unoriented statement
L(T₋, T₊) = L(T₊, T₋)* is Aiello–Conti, JKTR (2015), Prop. 2.4. The proof below covers vec{F} and vec{F}₃ at
once.

**Consequence for the indices.** g and g⁻¹ have the same number of leaves. For an oriented knot K, with Kr
its reverse, Km its mirror image and Kmr both:
- index(K) = index(Kmr);
- index(Kr) = index(Km).

This holds for both the vec{F}-index and the vec{F}₃-index. So a knot has at most two oriented values, and
for an invertible knot (K = Kr) all four coincide.

## Setting

Draw the diagram of g = (T₊, T₋) in the plane:
- the leaves are points on the x-axis, T₊ in the upper half plane, T₋ in the lower one;
- the Tait graph Γ(g) has one vertex in each black region; the black regions are the gaps between
  consecutive leaves that lie on the axis with the right parity;
- every internal vertex of T₊ (resp. T₋) gives an edge of Γ, drawn as an arc above (resp. below) the axis,
  and a crossing of the link diagram D(g), the medial graph of Γ;
- over/under at the crossing of a tree vertex is fixed by the local rule: the left–right strand is over, the
  parent–middle strand is under (in the binary case, the rule of Jones' construction).

Let ρ(x, y) = (x, −y) be the reflection of the plane in the x-axis. Let ρ̃(x, y, z) = (x, −y, z) be the
corresponding reflection of R³, where z is the height above the plane of the diagram. ρ̃ reverses the
orientation of R³.

## Proof

**1. Same group.** The membership condition is symmetric in T₊ and T₋:
- vec{F}: the leaf parities agree in the two trees;
- vec{F}₃: c₊(i) ≡ c₋(i) mod 2 for every leaf i.

So g⁻¹ is in the group whenever g is.

**2. The unoriented diagram.** The diagram of g⁻¹ = (T₋, T₊) is ρ(D(g)):
- T₋ now lies above the axis, reflected, and T₊ below it, reflected;
- ρ fixes the x-coordinate, so it preserves the words "left", "middle", "right" and "parent" at every tree
  vertex;
- hence the local rule picks, at every crossing of D(g⁻¹), the image under ρ of the over strand of the
  corresponding crossing of D(g).

ρ̃ preserves heights, so ρ(D(g)) with these crossings is exactly the diagram of the link ρ̃(L(g)). Since ρ̃
reverses the orientation of R³, L(g⁻¹) = L(g)* as unoriented links.

**3. The colouring.** ρ fixes the axis, so it fixes every gap between leaves, every black region and every
vertex of the Tait graph, and Γ(g⁻¹) = ρ(Γ(g)). The colours do not change either:
- **vec{F}₃.** The vertex to the left of leaf 2v gets the parity of c₊(2v), computed on the upper tree. For
  g⁻¹ the upper tree is T₋, so its colour is the parity of c₋(2v) for g, which is the parity of c₊(2v)
  because g ∈ vec{F}₃.
- **vec{F}.** The colouring is the 2-colouring of the bipartite graph Γ with the leftmost vertex coloured
  +. The vertex set and the leftmost vertex are the same for g and g⁻¹, so the colouring is the same.

**4. The orientation.**
- In L⃗(g) every strand runs along the boundary of its black region: counterclockwise if the region is +,
  clockwise if it is −.
- ρ reverses the planar orientation, so the image under ρ̃ of the orientation of L⃗(g) runs clockwise around
  the + regions and counterclockwise around the − regions.
- By step 3 the regions keep their colours in g⁻¹. So the orientation of L⃗(g⁻¹) is the opposite of the
  image of the orientation of L⃗(g).

Hence L⃗(g⁻¹) is ρ̃(L⃗(g)) with every orientation reversed: L⃗(g⁻¹) = (L⃗(g)ʳ)*. ∎

## Numerical checks

The rule was checked by comparing complements with SnapPy, using the isometries and their action on
meridian and longitude:
- vec{F}: on 178 diagrams (`reverse_scan.py`);
- vec{F}₃: on 231 hyperbolic knots of n = 9 and n = 11 (`tests/check_oriented3.py`);
- both groups: again on the first matching diagrams of every chunk of `oriented_scan.py`.
