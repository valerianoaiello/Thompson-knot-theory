/*
 * Enumeration of the knots produced by the tree diagrams of F_3 (and, as an independent
 * cross-check of bin/fknots, of F through Jones' map iota), with their HOMFLY polynomials.
 * Output format: the same as bin/fknots, so that run.py and identify.sage can be used for both.
 *
 * usage: iota_knots F|F3|F3vec n shard nshards out.tsv [max_reps] [only_key|@file]
 *        (with max_reps < 0 and only_key, every diagram of the selected HOMFLY classes is written at once
 *        to out.tsv.all as "key \t top_words \t bottom_words \t PD code"; used by complete_check.py)
 *        iota_knots eval   (reads lines 'F|F3 top_words bottom_words' from stdin; used by the tests)
 *
 * Model.  Every element of F is turned into an element of F_3 by Jones' map iota
 * (each binary caret gets a middle leaf), so we always work with pairs of ternary
 * trees (T+, T-) with c internal vertices each.  The 4-valent planar graph is:
 *   - every internal vertex of T+ and T- is a crossing (2c crossings);
 *   - top leaf j is joined to bottom leaf j;
 *   - the root of T+ is joined to the root of T-.
 * At every crossing the strands go straight: parent <-> middle child and
 * left child <-> right child; the left-right strand is the OVER strand
 * (same rule as `find_under_over_strand` in the old code).
 *
 * Index.  The parameter n is the index: c = n - 1 internal vertices per tree.
 *   F  : n = number of leaves of each binary tree      (F-index)
 *   F3 : n = number of internal vertices + 1           (F_3-index)
 *
 * Pruning.
 *   - Symmetries: (T+,T-), (T-,T+), (sT+,sT-), (sT-,sT+) where s = vertical
 *     reflection.  The first two non-trivial ones give the mirror image, the last
 *     one gives the same knot.  We keep only the lexicographically smallest pair.
 *   - Non-prime diagrams: if a non-root internal vertex of T+ and an internal
 *     vertex of T- cover exactly the same interval of leaves, the diagram is
 *     obtained by grafting a smaller tree diagram into a pair of leaves of another
 *     one, so it is a connected sum and can be skipped.
 *   - Only diagrams with a single component are kept.
 *
 * Each kept knot diagram is simplified with Reidemeister I and (generalised)
 * Reidemeister II moves on its Gauss code, and then its HOMFLY polynomial is
 * computed with libhomfly (the same library used by Sage).
 *
 * F3vec: only the elements of the oriented subgroup vec{F}_3 (Gamma 2-colourable), i.e. by Prop. 1 of
 * Aiello-Nagnibeda (J. Algebra Appl. 21 (2022) 2250139) c+(2i) = c-(2i) mod 2 for every leaf 2i, where c is
 * the weight of a leaf (see leaf_weight_mask). Pairs are taken in buckets with the same mask. The vertical
 * reflection does not preserve vec{F}_3 (it swaps the black and white regions), so the only symmetry is
 * (T+,T-) <-> (T-,T+) (the mirror image). A non-prime diagram is skipped only if the common interval starts at
 * an even leaf: then both the grafted diagram and the outer one are in vec{F}_3 (checked in
 * tests/check_F3vec.py); a graft at an odd leaf (below a middle edge) is kept.
 */

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <fstream>
#include <unordered_map>
#include <unordered_set>
#include <vector>

extern "C" {
#include "homfly.h"
}

/* ---------------------------------------------------------------------------
 * Trees
 * ------------------------------------------------------------------------- */

/* A planar ternary tree. Node 0 is the root. A child >= 0 is an internal node,
 * a child < 0 is the leaf -(child+1). Leaves are numbered left to right. */
struct Tree {
  int c = 0;                                 // internal nodes
  int m = 0;                                 // leaves (= 2c+1)
  std::vector<std::array<int, 3>> ch;        // children
  std::vector<std::pair<int, int>> iv;       // interval of leaves below node
  std::vector<int> leaf_port;                // leaf j -> port 4*node + slot
  std::vector<std::pair<int, int>> links;    // internal edges (child port, parent port)
  std::vector<uint16_t> intervals;           // sorted intervals of non-root nodes
};

/* Shapes are preorder strings: 'L' = leaf, 'N' followed by its children. */
static void gen_shapes(int k, int arity, std::vector<std::string> &out) {
  if (k == 0) {
    out.push_back("L");
    return;
  }
  if (arity == 2) {
    for (int k1 = 0; k1 < k; ++k1) {
      std::vector<std::string> a, b;
      gen_shapes(k1, 2, a);
      gen_shapes(k - 1 - k1, 2, b);
      for (auto &x : a)
        for (auto &y : b) out.push_back("N" + x + y);
    }
  } else {
    for (int k1 = 0; k1 < k; ++k1)
      for (int k2 = 0; k1 + k2 < k; ++k2) {
        std::vector<std::string> a, b, d;
        gen_shapes(k1, 3, a);
        gen_shapes(k2, 3, b);
        gen_shapes(k - 1 - k1 - k2, 3, d);
        for (auto &x : a)
          for (auto &y : b)
            for (auto &z : d) out.push_back("N" + x + y + z);
      }
  }
}

/* Jones' map iota on shapes: every binary caret gets a middle leaf. */
static std::string iota_shape(const std::string &s, size_t &pos) {
  if (s[pos] == 'L') {
    ++pos;
    return "L";
  }
  ++pos;
  std::string l = iota_shape(s, pos);
  std::string r = iota_shape(s, pos);
  return "N" + l + "L" + r;
}

static std::string iota_shape(const std::string &s) {
  size_t pos = 0;
  return iota_shape(s, pos);
}

/* Mirror image (vertical reflection) of a shape with given arity. */
static std::string mirror_shape(const std::string &s, size_t &pos, int arity) {
  if (s[pos] == 'L') {
    ++pos;
    return "L";
  }
  ++pos;
  std::vector<std::string> kids;
  for (int i = 0; i < arity; ++i) kids.push_back(mirror_shape(s, pos, arity));
  std::string r = "N";
  for (int i = arity - 1; i >= 0; --i) r += kids[i];
  return r;
}

static std::string mirror_shape(const std::string &s, int arity) {
  size_t pos = 0;
  return mirror_shape(s, pos, arity);
}

/* Leaf words (as in the old code: letters 0,1,2 = left, middle, right). */
static void shape_words(const std::string &s, size_t &pos, int arity, const std::string &prefix,
                        std::vector<std::string> &out) {
  if (s[pos] == 'L') {
    ++pos;
    out.push_back(prefix.empty() ? "0" : prefix);
    return;
  }
  ++pos;
  for (int i = 0; i < arity; ++i) shape_words(s, pos, arity, prefix + char('0' + i), out);
}

static std::string shape_words(const std::string &s, int arity) {
  size_t pos = 0;
  std::vector<std::string> w;
  shape_words(s, pos, arity, "", w);
  std::string r;
  for (size_t i = 0; i < w.size(); ++i) r += (i ? "," : "") + w[i];
  return r;
}

/* Shape from leaf words (a complete prefix code over {0,..,arity-1}). */
static std::string shape_from_words(std::vector<std::string> words, int arity) {
  if (words.size() == 1) return "L";  // the trivial tree (word "0" or "")
  std::sort(words.begin(), words.end());
  // recursive split on first letter
  std::string r = "N";
  for (int i = 0; i < arity; ++i) {
    std::vector<std::string> sub;
    for (auto &w : words)
      if (!w.empty() && w[0] == char('0' + i)) sub.push_back(w.substr(1));
    if (sub.empty()) {
      std::cerr << "invalid tree words\n";
      std::exit(1);
    }
    if (sub.size() == 1 && sub[0].empty())
      r += "L";
    else
      r += shape_from_words(sub, arity);
  }
  return r;
}

static int build_node(const std::string &s, size_t &pos, Tree &t, int &next_leaf) {
  if (s[pos] == 'L') {
    ++pos;
    return -(next_leaf++ + 1);
  }
  ++pos;
  int id = (int)t.ch.size();
  t.ch.push_back({0, 0, 0});
  t.iv.push_back({next_leaf, 0});
  for (int i = 0; i < 3; ++i) {
    int child = build_node(s, pos, t, next_leaf);
    t.ch[id][i] = child;
  }
  t.iv[id].second = next_leaf - 1;
  return id;
}

/* Build a ternary tree from a ternary shape string. Ports: 4*node + slot,
 * slot 0 = parent, 1 = left, 2 = middle, 3 = right. */
static Tree build_tree(const std::string &ternary_shape) {
  Tree t;
  size_t pos = 0;
  int next_leaf = 0;
  if (ternary_shape == "L") {
    t.m = 1;
    return t;
  }
  build_node(ternary_shape, pos, t, next_leaf);
  t.c = (int)t.ch.size();
  t.m = next_leaf;
  t.leaf_port.assign(t.m, -1);
  for (int v = 0; v < t.c; ++v)
    for (int i = 0; i < 3; ++i) {
      int child = t.ch[v][i];
      int port = 4 * v + i + 1;
      if (child < 0)
        t.leaf_port[-child - 1] = port;
      else
        t.links.push_back({port, 4 * child});
    }
  for (int v = 1; v < t.c; ++v) t.intervals.push_back((uint16_t)(t.iv[v].first * 64 + t.iv[v].second));
  std::sort(t.intervals.begin(), t.intervals.end());
  return t;
}

/* Weight parity (Aiello-Nagnibeda, Definition 3) of the leaves 0, 2, 4, ... of a ternary shape: bit i is
 * c(2i) mod 2. Along the path from the root, a middle edge adds 1 and switches between odd and even words;
 * in an odd word a right edge adds 1, in an even word a left edge adds 1. */
static void leaf_weight_mask(const std::string &s, size_t &pos, int weight, int middles, int &leaf,
                             uint32_t &mask) {
  if (s[pos] == 'L') {
    ++pos;
    if (leaf % 2 == 0 && (weight & 1)) mask |= 1u << (leaf / 2);
    ++leaf;
    return;
  }
  ++pos;
  bool odd_word = (middles & 1) == 0;
  leaf_weight_mask(s, pos, weight + (odd_word ? 0 : 1), middles, leaf, mask);  // left
  leaf_weight_mask(s, pos, weight + 1, middles + 1, leaf, mask);               // middle
  leaf_weight_mask(s, pos, weight + (odd_word ? 1 : 0), middles, leaf, mask);  // right
}

static uint32_t leaf_weight_mask(const std::string &s) {
  size_t pos = 0;
  int leaf = 0;
  uint32_t mask = 0;
  leaf_weight_mask(s, pos, 0, 0, leaf, mask);
  return mask;
}

/* Non-prime test: a non-root internal vertex of one tree covering the same
 * interval as an internal vertex of the other (the roots cover the whole set). */
static bool is_prime_pair(const Tree &a, const Tree &b, bool even_start_only = false) {
  size_t i = 0, j = 0;
  while (i < a.intervals.size() && j < b.intervals.size()) {
    if (a.intervals[i] == b.intervals[j] && !(even_start_only && (a.intervals[i] >> 6) % 2)) return false;
    if (a.intervals[i] < b.intervals[j])
      ++i;
    else
      ++j;
  }
  return true;
}

/* ---------------------------------------------------------------------------
 * Link diagram of a tree diagram
 * ------------------------------------------------------------------------- */

struct Visit {
  int x;      // crossing
  bool over;  // passing over
};

struct Diagram {
  int ncross = 0;
  int ncomp = 0;
  std::vector<Visit> gauss;          // oriented Gauss code of the first component
  std::vector<int> enter_slot;       // slot through which visit i enters its crossing
  std::vector<int> sign;             // crossing sign (+1 right handed)
};

/* position of a slot in the counterclockwise order around a crossing:
 * top tree:    parent, left, middle, right   (children below)
 * bottom tree: parent, right, middle, left   (children above) */
static inline int slot_pos(int x, int c, int slot) { return x < c ? slot : (4 - slot) & 3; }

/* Builds the partner array and walks along the first component. Returns false if
 * the link has more than one component (when only_knots is set). */
static bool build_diagram(const Tree &top, const Tree &bot, std::vector<int> &partner, Diagram &d,
                          bool only_knots) {
  const int c = top.c;
  const int nports = 8 * c;
  partner.assign(nports, -1);
  for (auto &l : top.links) {
    partner[l.first] = l.second;
    partner[l.second] = l.first;
  }
  const int off = 4 * c;
  for (auto &l : bot.links) {
    partner[l.first + off] = l.second + off;
    partner[l.second + off] = l.first + off;
  }
  partner[0] = off;
  partner[off] = 0;
  for (int j = 0; j < top.m; ++j) {
    partner[top.leaf_port[j]] = bot.leaf_port[j] + off;
    partner[bot.leaf_port[j] + off] = top.leaf_port[j];
  }

  d.ncross = 2 * c;
  d.gauss.clear();
  d.enter_slot.clear();
  // walk: leave crossing 0 through its parent slot
  int p = 0;
  do {
    int q = partner[p];
    int y = q >> 2, t = q & 3;
    d.gauss.push_back({y, (t & 1) != 0});
    d.enter_slot.push_back(t);
    p = (y << 2) | (t ^ 2);
  } while (p != 0);

  if ((int)d.gauss.size() != 2 * d.ncross) {
    if (only_knots) return false;
    // count components
    std::vector<char> seen(nports, 0);
    d.ncomp = 0;
    for (int s = 0; s < nports; ++s) {
      if (seen[s]) continue;
      ++d.ncomp;
      int pp = s;
      do {
        seen[pp] = 1;
        int q = partner[pp];
        seen[q] = 1;
        pp = q ^ 2;
      } while (pp != s);
    }
    return false;
  }
  d.ncomp = 1;

  // crossing signs
  std::vector<int> over_exit(d.ncross), under_exit(d.ncross);
  for (size_t i = 0; i < d.gauss.size(); ++i) {
    int x = d.gauss[i].x;
    int ex = d.enter_slot[i] ^ 2;
    if (d.gauss[i].over)
      over_exit[x] = ex;
    else
      under_exit[x] = ex;
  }
  d.sign.assign(d.ncross, 0);
  for (int x = 0; x < d.ncross; ++x) {
    int po = slot_pos(x, c, over_exit[x]);
    int pu = slot_pos(x, c, under_exit[x]);
    d.sign[x] = (pu == ((po + 1) & 3)) ? 1 : -1;
  }
  return true;
}

/* PD code (Sage/KnotInfo convention: start with the incoming under strand and go
 * counterclockwise). Edge i+1 is the edge entering visit i. */
static std::string pd_code(const Diagram &d, int c) {
  const int V = (int)d.gauss.size();
  std::vector<std::array<int, 4>> lab(d.ncross);  // label by slot
  std::vector<int> under_enter(d.ncross);
  for (int i = 0; i < V; ++i) {
    int x = d.gauss[i].x, t = d.enter_slot[i];
    lab[x][t] = i + 1;
    lab[x][t ^ 2] = (i + 1) % V + 1;
    if (!d.gauss[i].over) under_enter[x] = t;
  }
  std::ostringstream o;
  o << "[";
  for (int x = 0; x < d.ncross; ++x) {
    int p0 = slot_pos(x, c, under_enter[x]);
    o << (x ? ", " : "") << "[";
    for (int k = 0; k < 4; ++k) {
      int pos = (p0 + k) & 3;
      int slot = x < c ? pos : (4 - pos) & 3;
      o << (k ? ", " : "") << lab[x][slot];
    }
    o << "]";
  }
  o << "]";
  return o.str();
}

/* ---------------------------------------------------------------------------
 * Simplification of Gauss codes (Reidemeister I and generalised II)
 * ------------------------------------------------------------------------- */

static void erase_positions(std::vector<Visit> &g, std::vector<int> pos) {
  std::sort(pos.rbegin(), pos.rend());
  for (int p : pos) g.erase(g.begin() + p);
}

static void simplify(std::vector<Visit> &g, const std::vector<int> &sign) {
  bool changed = true;
  while (changed && !g.empty()) {
    changed = false;
    const int L = (int)g.size();
    // Reidemeister I: a crossing met twice in a row
    for (int i = 0; i < L; ++i) {
      int j = (i + 1) % L;
      if (g[i].x == g[j].x) {
        erase_positions(g, {i, j});
        changed = true;
        break;
      }
    }
    if (changed) continue;
    if (L < 4) continue;
    // Reidemeister II: an arc over (or under) two crossings a, b with no
    // crossing in between, the other arc between a and b also free, and
    // opposite signs. The first arc can then be pushed along the second.
    std::vector<int> other(L);
    {
      std::vector<int> first(sign.size(), -1);
      for (int i = 0; i < L; ++i) {
        int x = g[i].x;
        if (first[x] < 0)
          first[x] = i;
        else {
          other[i] = first[x];
          other[first[x]] = i;
        }
      }
    }
    for (int i = 0; i < L && !changed; ++i) {
      int j = (i + 1) % L;
      int a = g[i].x, b = g[j].x;
      if (g[i].over != g[j].over || sign[a] == sign[b]) continue;
      int oa = other[i], ob = other[j];
      if ((oa + 1) % L == ob || (ob + 1) % L == oa) {
        erase_positions(g, {i, j, oa, ob});
        changed = true;
      }
    }
  }
}

/* libhomfly input: "1 L  x f ... (x hand)..." with crossings renamed 0..k-1. */
static std::string homfly_input(const std::vector<Visit> &g, const std::vector<int> &sign,
                                std::vector<int> *out_names = nullptr) {
  std::vector<int> name(sign.size(), -1);
  int k = 0;
  for (auto &v : g)
    if (name[v.x] < 0) name[v.x] = k++;
  std::ostringstream o;
  o << "1 " << g.size();
  for (auto &v : g) o << " " << name[v.x] << " " << (v.over ? 1 : -1);
  std::vector<int> hand(k);
  for (size_t x = 0; x < sign.size(); ++x)
    if (name[x] >= 0) hand[name[x]] = sign[x];
  for (int i = 0; i < k; ++i) o << " " << i << " " << hand[i];
  if (out_names) *out_names = name;
  return o.str();
}

/* Sage oriented Gauss code: [[+-(crossing+1) ...], [signs]] (positive = over). */
static std::string sage_ogc(const std::vector<Visit> &g, const std::vector<int> &sign) {
  std::vector<int> name(sign.size(), -1);
  int k = 0;
  for (auto &v : g)
    if (name[v.x] < 0) name[v.x] = k++;
  std::ostringstream o;
  o << "[[";
  for (size_t i = 0; i < g.size(); ++i) o << (i ? "," : "") << (g[i].over ? 1 : -1) * (name[g[i].x] + 1);
  o << "],[";
  std::vector<int> hand(k);
  for (size_t x = 0; x < sign.size(); ++x)
    if (name[x] >= 0) hand[name[x]] = sign[x];
  for (int i = 0; i < k; ++i) o << (i ? "," : "") << hand[i];
  o << "]]";
  return o.str();
}

/* Canonical form of a Gauss code up to rotation and reversal (cache key). */
static std::string canonical_gauss(const std::vector<Visit> &g, const std::vector<int> &sign) {
  const int L = (int)g.size();
  std::string best;
  std::vector<int> name(sign.size());
  for (int dir = 0; dir < 2; ++dir)
    for (int r = 0; r < L; ++r) {
      std::fill(name.begin(), name.end(), -1);
      std::string s;
      s.reserve(2 * L);
      int k = 0;
      for (int i = 0; i < L; ++i) {
        const Visit &v = dir == 0 ? g[(r + i) % L] : g[((r - i) % L + L) % L];
        if (name[v.x] < 0) {
          name[v.x] = k++;
          s.push_back(char(sign[v.x] > 0 ? 'p' : 'n'));
        }
        s.push_back(char(33 + name[v.x]));
        s.push_back(v.over ? 'o' : 'u');
      }
      if (best.empty() || s < best) best = s;
    }
  return best;
}

static std::string clean(const char *s) {
  std::string r(s);
  size_t a = r.find_first_not_of(' ');
  if (a == std::string::npos) return "";
  return r.substr(a);
}

static std::string UNKNOT_KEY;
static const std::string UNKNOT_MIRROR_KEY = "1*L^0*M^0 ";

static std::string compute_homfly(std::vector<Visit> g, const std::vector<int> &sign) {
  if (g.size() < 6) return UNKNOT_KEY;  // at most 2 crossings
  std::string in = homfly_input(g, sign);
  std::vector<char> buf(in.begin(), in.end());
  buf.push_back(0);
  return clean(homfly_str(buf.data()));
}

/* HOMFLY (variables M, L of libhomfly) as a canonical string up to mirror (L -> L^-1):
 * the same key as bin/fknots. */
static std::string homfly_mirror_key(const std::vector<Visit> &g, const std::vector<int> &sign) {
  if (g.size() < 6) return UNKNOT_MIRROR_KEY;
  std::string in = homfly_input(g, sign);
  std::vector<char> buf(in.begin(), in.end());
  buf.push_back(0);
  Poly *p = homfly(buf.data());
  std::vector<std::array<long, 3>> a, b;  // (l, m, coef)
  for (int i = 0; i < p->len; i++) {
    a.push_back({(long)p->term[i].l, (long)p->term[i].m, (long)p->term[i].coef});
    b.push_back({-(long)p->term[i].l, (long)p->term[i].m, (long)p->term[i].coef});
  }
  std::sort(a.begin(), a.end());
  std::sort(b.begin(), b.end());
  const auto &best = std::min(a, b);
  std::string s;
  for (auto &t : best)
    s += std::to_string(t[2]) + "*L^" + std::to_string(t[0]) + "*M^" + std::to_string(t[1]) + " ";
  return s;
}

/* Simplified Gauss code in the format of bin/fknots: "seq|hands" (Sage oriented Gauss code,
 * + = over, crossings renamed in order of appearance). */
static std::string gauss_string(const std::vector<Visit> &g, const std::vector<int> &sign) {
  std::vector<int> name(sign.size(), -1);
  int k = 0;
  std::string seq, hands;
  for (auto &v : g) {
    if (name[v.x] < 0) {
      name[v.x] = k++;
      hands += (hands.empty() ? "" : ",") + std::to_string(sign[v.x]);
    }
    seq += (seq.empty() ? "" : ",") + std::to_string((v.over ? 1 : -1) * (name[v.x] + 1));
  }
  return seq + "|" + hands;
}

/* ---------------------------------------------------------------------------
 * Modes
 * ------------------------------------------------------------------------- */

static void usage() {
  std::cerr << "usage:\n"
               "  iota_knots F|F3|F3vec n shard nshards out.tsv [max_reps] [only_key|@file]\n"
               "  iota_knots eval   (reads lines 'F|F3 top_words bottom_words' from stdin)\n";
  std::exit(1);
}

/* eval: one line per input pair with components, PD, simplified OGC, HOMFLY. */
static int mode_eval() {
  std::string group, tw, bw;
  while (std::cin >> group >> tw >> bw) {
    int arity = group == "F" ? 2 : 3;
    auto split = [](const std::string &s) {
      std::vector<std::string> r;
      std::stringstream ss(s);
      std::string w;
      while (std::getline(ss, w, ',')) r.push_back(w);
      return r;
    };
    auto tws = split(tw), bws = split(bw);
    if (tws.size() != bws.size()) {
      std::cout << "ERROR different number of leaves\n";
      continue;
    }
    std::string ts = shape_from_words(tws, arity), bs = shape_from_words(bws, arity);
    if (arity == 2) {
      ts = iota_shape(ts);
      bs = iota_shape(bs);
    }
    Tree top = build_tree(ts), bot = build_tree(bs);
    if (top.c == 0) {
      std::cout << "components=1\tprime=1\tpd=[]\togc=[[],[]]\thomfly=" << UNKNOT_KEY << "\n";
      continue;
    }
    std::vector<int> partner;
    Diagram d;
    bool knot = build_diagram(top, bot, partner, d, false);
    std::cout << "components=" << d.ncomp << "\tprime=" << is_prime_pair(top, bot);
    if (!knot) {
      std::cout << "\n";
      continue;
    }
    std::vector<Visit> g = d.gauss;
    std::cout << "\tpd=" << pd_code(d, top.c) << "\tfull_ogc=" << sage_ogc(g, d.sign)
              << "\tfull_homfly=" << compute_homfly(g, d.sign);
    simplify(g, d.sign);
    std::cout << "\togc=" << sage_ogc(g, d.sign) << "\thomfly=" << compute_homfly(g, d.sign) << "\n";
  }
  return 0;
}

struct ClassInfo {
  long long count = 0;
  int min_crossings = 1 << 30;  // after the Reidemeister I/II simplification
  std::vector<std::string> reps;
};

static int mode_enum(const std::string &group, int n, int shard, int nshards, const std::string &out,
                     int max_reps, const std::unordered_set<std::string> &only_keys) {
  FILE *all = nullptr;
  if (max_reps < 0) {
    all = std::fopen((out + ".all").c_str(), "w");
    if (!all) {
      std::perror(out.c_str());
      return 1;
    }
  }
  const int arity = group == "F" ? 2 : 3;
  const bool vec = group == "F3vec";
  const int c = n - 1;
  std::vector<std::string> shapes;  // in the group's own arity
  gen_shapes(c, arity, shapes);
  std::sort(shapes.begin(), shapes.end());
  const int N = (int)shapes.size();
  std::unordered_map<std::string, int> index;
  for (int i = 0; i < N; ++i) index[shapes[i]] = i;
  std::vector<int> sig(N);
  std::vector<Tree> trees(N);
  for (int i = 0; i < N; ++i) {
    sig[i] = index.at(mirror_shape(shapes[i], arity));
    trees[i] = build_tree(arity == 2 ? iota_shape(shapes[i]) : shapes[i]);
  }
  std::vector<uint32_t> wmask(vec ? N : 0);
  std::unordered_map<uint32_t, std::vector<int>> bucket;  // weight mask -> trees (increasing)
  for (int i = 0; i < (int)wmask.size(); ++i) bucket[wmask[i] = leaf_weight_mask(shapes[i])].push_back(i);

  long long examined = 0, canonical = 0, prime = 0, knots = 0, cache_hits = 0;
  std::unordered_map<std::string, std::string> cache;  // canonical gauss -> homfly key
  const size_t max_cache = 1000000;
  std::map<std::string, ClassInfo> classes;
  std::vector<int> partner;
  Diagram d;

  for (int a = shard; a < N; a += nshards) {
    const std::vector<int> *bs = vec ? &bucket[wmask[a]] : nullptr;
    size_t k0 = vec ? std::lower_bound(bs->begin(), bs->end(), a) - bs->begin() : 0;
    for (size_t k = k0; vec ? k < bs->size() : (int)k < N; ++k) {
      const int b = vec ? (*bs)[k] : (int)k;
      if (b < a) continue;
      ++examined;
      // canonical representative of the symmetry orbit (in vec{F}_3 only (a,b) <-> (b,a))
      if (vec) {
        // every pair (a, b) with a <= b in the same bucket
      } else {
        int sa = sig[a], sb = sig[b];
        if (std::make_pair(sa, sb) < std::make_pair(a, b)) continue;
        if (std::make_pair(sb, sa) < std::make_pair(a, b)) continue;
      }
      ++canonical;
      if (!is_prime_pair(trees[a], trees[b], vec)) continue;
      ++prime;
      if (!build_diagram(trees[a], trees[b], partner, d, true)) continue;
      ++knots;
      std::vector<Visit> g = d.gauss;
      simplify(g, d.sign);
      std::string key = UNKNOT_MIRROR_KEY;
      if (g.size() >= 6) {
        std::string cg = canonical_gauss(g, d.sign);
        auto it = cache.find(cg);
        if (it != cache.end()) {
          key = it->second;
          ++cache_hits;
        } else {
          key = homfly_mirror_key(g, d.sign);
          if (cache.size() < max_cache) cache.emplace(std::move(cg), key);
        }
      }
      ClassInfo &ci = classes[key];
      ++ci.count;
      ci.min_crossings = std::min(ci.min_crossings, (int)g.size() / 2);
      if (all && only_keys.count(key))
        std::fprintf(all, "%s\t%s\t%s\t%s\n", key.c_str(), shape_words(shapes[a], arity).c_str(),
                     shape_words(shapes[b], arity).c_str(), pd_code(d, trees[a].c).c_str());
      else if ((int)ci.reps.size() < max_reps && (only_keys.empty() || only_keys.count(key)))
        ci.reps.push_back(shape_words(shapes[a], arity) + "|" + shape_words(shapes[b], arity) + "|" +
                          (g.empty() ? std::string("|") : gauss_string(g, d.sign)));
    }
  }

  if (all) std::fclose(all);
  FILE *f = std::fopen(out.c_str(), "w");
  if (!f) {
    std::perror(out.c_str());
    return 1;
  }
  std::fprintf(f,
               "# n=%d shard=%d/%d examined=%lld canonical=%lld prime=%lld knots=%lld classes=%zu "
               "cache_hits=%lld\n",
               n, shard, nshards, examined, canonical, prime, knots, classes.size(), cache_hits);
  for (auto &kv : classes) {
    std::fprintf(f, "%s\t%lld\t%d\t", kv.first.c_str(), kv.second.count, kv.second.min_crossings);
    for (size_t r = 0; r < kv.second.reps.size(); ++r)
      std::fprintf(f, "%s%s", r ? ";" : "", kv.second.reps[r].c_str());
    std::fprintf(f, "\n");
  }
  std::fclose(f);
  return 0;
}

int main(int argc, char **argv) {
  {
    char unknot[] = "1 2 0 1 0 -1 0 1";  // one-crossing diagram of the unknot
    UNKNOT_KEY = clean(homfly_str(unknot));
  }
  if (argc < 2) usage();
  std::string mode = argv[1];
  if (mode == "eval") return mode_eval();
  if ((mode != "F" && mode != "F3" && mode != "F3vec") || argc < 6) usage();
  int n = std::atoi(argv[2]), shard = std::atoi(argv[3]), nshards = std::atoi(argv[4]);
  int max_reps = argc > 6 ? std::atoi(argv[6]) : 20;
  std::unordered_set<std::string> only_keys;  // empty = store representatives of every class
  if (argc > 7) {
    std::string a = argv[7];
    if (a[0] == '@') {
      std::ifstream in(a.substr(1));
      std::string line;
      while (std::getline(in, line))
        if (!line.empty()) only_keys.insert(line);
    } else {
      only_keys.insert(a);
    }
  }
  if (max_reps < 0 && only_keys.empty()) usage();
  if (n < 2) usage();
  return mode_enum(mode, n, shard, nshards, argv[5], max_reps, only_keys);
}
