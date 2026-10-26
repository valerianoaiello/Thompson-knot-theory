// Fast enumeration of the knots L(T+, T-) produced by binary tree diagrams with n leaves
// (Jones' construction for Thompson's group F), with their HOMFLY polynomials.
//
// Same conventions as ftrees.py (the slow reference implementation), see the comments there.
//
// For every pair (T+, T-) of binary trees with n leaves we
//   1. keep one representative of its orbit under the two reflections
//      (T+, T-) -> (T-, T+) and (T+, T-) -> (flip T+, flip T-), which only change L into its mirror;
//   2. skip it if it is not prime (a non-root subtree of T+ and one of T- span the same leaves);
//   3. skip it if L(T+, T-) has more than one component;
//   4. compute the HOMFLY polynomial with libhomfly and group the diagrams by HOMFLY up to mirror.
//
// usage: fknots n shard nshards out.tsv [max_reps] [vec|all] [only_key]
// With only_key, representatives are stored only for the HOMFLY class with that key (the other classes
// are still counted): this is used by oriented_index.py to get all the diagrams of one knot.
// With "vec" only the elements of Jones' oriented subgroup vec{F} are kept (see Tree::parity). The
// vertical reflection (flip) does not preserve vec{F}, so it is not used: the orbits are {g, g^-1}
// ((T-, T+) is in vec{F} iff (T+, T-) is, and gives the mirror image).
// The output has one line per HOMFLY class: key \t count \t min_crossings \t reps, where
// min_crossings is the smallest number of crossings left after Reidemeister I/II simplification
// and reps is a ';'-separated list of "top_words|bottom_words|gauss_seq|gauss_signs": leaf addresses
// (0 = left, 1 = right, separated by ',') and the simplified Gauss code (see gauss_string).
// The first line is a '#' comment with the statistics of the run.

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <string>
#include <unordered_map>
#include <vector>

extern "C" {
#include "homfly.h"
}

static const int MAXN = 16;

struct Tree {
    uint8_t parent[MAXN];          // Tait edge (parent[j], j) for j = 1..n-1
    std::array<uint64_t, 4> bits;  // leaf intervals [l, r] of the non-root internal vertices
    int flip;                      // index of the reflected tree
    uint32_t parity;               // bit j = parity of the number of right edges from the root to leaf j;
                                   // (T+, T-) is in vec{F} iff the Tait graph is 2-colourable iff
                                   // T+ and T- have the same parity (checked in tests/check_vecF.sage)
};

struct Level {                     // all trees with a given number of leaves
    std::vector<Tree> trees;
    std::vector<int> split, left, right;  // tree i = (left[i], right[i]), left one with split[i] leaves
};

static std::vector<Level> levels;

static inline void set_bit(std::array<uint64_t, 4> &b, int l, int r) {
    int id = l * MAXN + r;
    b[id >> 6] |= uint64_t(1) << (id & 63);
}

static void build_levels(int n) {
    levels.assign(n + 1, Level());
    Tree leaf{};
    leaf.flip = 0;
    levels[1].trees.push_back(leaf);
    levels[1].split.push_back(0);
    levels[1].left.push_back(-1);
    levels[1].right.push_back(-1);
    for (int m = 2; m <= n; m++) {
        Level &L = levels[m];
        std::vector<size_t> offset(m, 0);
        for (int k = 1; k < m; k++) {
            offset[k] = L.trees.size();
            const Level &A = levels[k], &B = levels[m - k];
            for (size_t a = 0; a < A.trees.size(); a++)
                for (size_t b = 0; b < B.trees.size(); b++) {
                    Tree t{};
                    t.parent[k] = 0;
                    for (int j = 1; j < k; j++) t.parent[j] = A.trees[a].parent[j];
                    for (int j = 1; j < m - k; j++) t.parent[k + j] = k + B.trees[b].parent[j];
                    for (int w = 0; w < 4; w++) t.bits[w] = A.trees[a].bits[w];
                    // leaves of the left subtree get a 0 (parity unchanged), of the right one a 1
                    t.parity = A.trees[a].parity |
                               ((~B.trees[b].parity & ((uint32_t(1) << (m - k)) - 1)) << k);
                    if (k >= 2) set_bit(t.bits, 0, k - 1);
                    if (m - k >= 2) set_bit(t.bits, k, m - 1);
                    for (int l = 0; l < m - k; l++)
                        for (int r = l + 1; r < m - k; r++) {
                            int id = l * MAXN + r;
                            if (B.trees[b].bits[id >> 6] >> (id & 63) & 1) set_bit(t.bits, k + l, k + r);
                        }
                    L.trees.push_back(t);
                    L.split.push_back(k);
                    L.left.push_back((int)a);
                    L.right.push_back((int)b);
                }
        }
        // flip(A, B) = (flip B, flip A)
        for (size_t i = 0; i < L.trees.size(); i++) {
            int k = L.split[i];
            int fa = levels[m - k].trees[L.right[i]].flip, fb = levels[k].trees[L.left[i]].flip;
            L.trees[i].flip = (int)(offset[m - k] + (size_t)fa * levels[k].trees.size() + fb);
        }
    }
}

static void leaf_words(int m, int i, const std::string &prefix, std::vector<std::string> &out) {
    if (m == 1) {
        out.push_back(prefix);
        return;
    }
    const Level &L = levels[m];
    int k = L.split[i];
    leaf_words(k, L.left[i], prefix + "0", out);
    leaf_words(m - k, L.right[i], prefix + "1", out);
}

static std::string words_string(int n, int i) {
    std::vector<std::string> w;
    leaf_words(n, i, "", w);
    std::string s;
    for (size_t k = 0; k < w.size(); k++) s += (k ? "," : "") + w[k];
    return s;
}

// ---------------------------------------------------------------------------------------------
// link diagram: medial graph of the Tait graph (see ftrees.medial_of_graph)
// ---------------------------------------------------------------------------------------------

struct Diagram {
    int n, E;                        // vertices of the Tait graph, crossings
    int eu[2 * MAXN], ew[2 * MAXN];  // endpoints of the Tait edges (eu < ew)
    int corner_at[8 * MAXN];         // (crossing * 4 + slot) -> corner
    int end_cs[8 * MAXN][2];         // corner -> its two ends, encoded as crossing * 4 + slot
    int ncorners;
};

static void build_diagram(int n, const Tree &tp, const Tree &tm, Diagram &D) {
    D.n = n;
    D.E = 2 * (n - 1);
    for (int j = 1; j < n; j++) {
        D.eu[j - 1] = tp.parent[j];
        D.ew[j - 1] = j;
        D.eu[n - 2 + j] = tm.parent[j];
        D.ew[n - 2 + j] = j;
    }
    D.ncorners = 0;
    int rot[2 * MAXN];
    for (int v = 0; v < n; v++) {
        int d = 0;
        for (int j = v + 1; j < n; j++)  // upper arcs to the right, nearest first
            if (tp.parent[j] == v) rot[d++] = j - 1;
        if (v >= 1) {
            rot[d++] = v - 1;          // upper arc to the left
            rot[d++] = n - 2 + v;      // lower arc to the left
        }
        for (int j = n - 1; j > v; j--)  // lower arcs to the right, farthest first
            if (tm.parent[j] == v) rot[d++] = n - 2 + j;
        for (int k = 0; k < d; k++) {
            int a = rot[k], b = rot[(k + 1) % d];
            int c = D.ncorners++;
            int ea = a * 4 + (D.eu[a] == v ? 3 : 1);
            int eb = b * 4 + (D.eu[b] == v ? 0 : 2);
            D.end_cs[c][0] = ea;
            D.end_cs[c][1] = eb;
            D.corner_at[ea] = c;
            D.corner_at[eb] = c;
        }
    }
}

// Walks along the link; returns the number of components. If `walk` is given and the link is a
// knot, stores the visited (crossing * 4 + entry slot) in order.
static int components(const Diagram &D, int *walk) {
    bool seen[8 * MAXN] = {false};
    int comps = 0, len = 0;
    for (int c0 = 0; c0 < D.ncorners; c0++) {
        if (seen[c0]) continue;
        comps++;
        int c = c0, end = 1;
        while (!seen[c]) {
            seen[c] = true;
            int xs = D.end_cs[c][end];
            if (walk && comps == 1) walk[len++] = xs;
            int out = (xs & ~3) | ((xs + 2) & 3);
            c = D.corner_at[out];
            end = (D.end_cs[c][0] == out) ? 1 : 0;
        }
    }
    return comps;
}

// Oriented Gauss code of a knot: the sequence of passages (crossing, over?) and the handedness of
// each crossing.
struct Gauss {
    std::vector<std::pair<int, bool>> seq;
    std::vector<int> hand;
};

static Gauss gauss_code(const Diagram &D, const int *walk) {
    int len = 2 * D.E;
    std::vector<int> under_in(D.E, -1), over_in(D.E, -1);
    Gauss G;
    for (int k = 0; k < len; k++) {
        int x = walk[k] >> 2, slot = walk[k] & 3;
        bool positive = x < D.n - 1;           // edges of the top tree
        bool over = positive ? (slot % 2 == 0) : (slot % 2 == 1);
        (over ? over_in : under_in)[x] = slot;
        G.seq.push_back({x, over});
    }
    G.hand.resize(D.E);
    for (int x = 0; x < D.E; x++) G.hand[x] = (over_in[x] == (under_in[x] + 1) % 4) ? -1 : 1;
    return G;
}

// Reidemeister I and II simplifications, read off the Gauss code:
//   I : a crossing met twice in a row;
//  II : two crossings x, y met consecutively over-over somewhere and consecutively under-under
//       somewhere else (the two arcs bound a bigon face, the rest of the knot being on one side).
static void simplify(Gauss &G) {
    std::vector<int> pos(2 * G.hand.size());  // the two positions of each crossing in seq
    std::vector<std::pair<int, bool>> s;
    while (!G.seq.empty()) {
        int L = (int)G.seq.size();
        std::fill(pos.begin(), pos.end(), -1);
        for (int k = 0; k < L; k++) {
            int x = G.seq[k].first;
            pos[2 * x + (pos[2 * x] >= 0)] = k;
        }
        auto other = [&](int x, int k) { return pos[2 * x] == k ? pos[2 * x + 1] : pos[2 * x]; };
        int rx = -1, ry = -1;
        for (int k = 0; k < L && rx < 0; k++) {
            const auto &a = G.seq[k], &b = G.seq[(k + 1) % L];
            if (a.first == b.first) {
                rx = a.first;  // Reidemeister I
            } else if (a.second == b.second) {
                int pa = other(a.first, k), pb = other(b.first, (k + 1) % L);
                if ((pa + 1) % L == pb || (pb + 1) % L == pa) rx = a.first, ry = b.first;  // Reidemeister II
            }
        }
        if (rx < 0) return;
        s.clear();
        for (auto &p : G.seq) if (p.first != rx && p.first != ry) s.push_back(p);
        G.seq.swap(s);
    }
}

// libhomfly input (see sage/libs/homfly.pyx); crossings must be renamed 0, 1, ..., m-1
static std::string homfly_input(const Gauss &G) {
    std::vector<int> name(G.hand.size(), -1);
    int m = 0;
    std::string s = "1 " + std::to_string(G.seq.size());
    for (auto &p : G.seq) {
        if (name[p.first] < 0) name[p.first] = m++;
        s += " " + std::to_string(name[p.first]) + (p.second ? " 1" : " -1");
    }
    std::vector<int> hand(m);
    for (size_t x = 0; x < G.hand.size(); x++)
        if (name[x] >= 0) hand[name[x]] = G.hand[x];
    for (int x = 0; x < m; x++) s += " " + std::to_string(x) + (hand[x] > 0 ? " 1" : " -1");
    return s;
}

// HOMFLY (variables M, L of libhomfly) as a canonical string, up to mirror (L -> L^-1)
static std::string homfly_key(const std::string &gauss) {
    std::vector<char> buf(gauss.begin(), gauss.end());
    buf.push_back('\0');
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
    for (auto &t : best) s += std::to_string(t[2]) + "*L^" + std::to_string(t[0]) + "*M^" + std::to_string(t[1]) + " ";
    return s;
}

// Canonical form of a Gauss code up to rotation, reversal of the orientation and mirror
// (relabelling the crossings in order of appearance); used as a key for caching HOMFLY.
static std::string gauss_canonical(const Gauss &G) {
    int L = (int)G.seq.size();
    std::string best;
    std::string cur(L + L / 2, '\0');
    std::vector<int> name(G.hand.size());
    for (int dir = 0; dir < 2; dir++)
        for (int mir = 0; mir < 2; mir++)
            for (int r = 0; r < L; r++) {
                std::fill(name.begin(), name.end(), -1);
                int m = 0;
                for (int k = 0; k < L; k++) {
                    const auto &p = G.seq[dir ? (r - k + 2 * L) % L : (r + k) % L];
                    if (name[p.first] < 0) {
                        name[p.first] = m;
                        cur[L + m] = char(G.hand[p.first] * (mir ? -1 : 1) > 0 ? 1 : 2);
                        m++;
                    }
                    cur[k] = char(1 + 2 * name[p.first] + (p.second != (mir == 1)));
                }
                if (best.empty() || cur < best) best = cur;
            }
    return best;
}

// Simplified Gauss code in Sage's oriented_gauss_code format: passages as +-(crossing + 1)
// (+ = over), then the sign of each crossing, both comma-separated.
static std::string gauss_string(const Gauss &G) {
    std::vector<int> name(G.hand.size(), -1);
    int m = 0;
    std::string seq, hands;
    for (auto &p : G.seq) {
        if (name[p.first] < 0) {
            name[p.first] = m++;
            hands += (hands.empty() ? "" : ",") + std::to_string(G.hand[p.first]);
        }
        seq += (seq.empty() ? "" : ",") + std::to_string((p.second ? 1 : -1) * (name[p.first] + 1));
    }
    return seq + "|" + hands;
}

struct Rep {
    int top, bottom;
    std::string gauss;
};

struct ClassInfo {
    long long count = 0;
    int min_crossings = 1 << 30;  // after the Reidemeister I/II simplification
    std::vector<Rep> reps;
};

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "usage: %s n shard nshards out.tsv [max_reps]\n", argv[0]);
        return 1;
    }
    int n = atoi(argv[1]), shard = atoi(argv[2]), nshards = atoi(argv[3]);
    const char *outpath = argv[4];
    int max_reps = argc > 5 ? atoi(argv[5]) : 20;
    bool vec = argc > 6 && strcmp(argv[6], "vec") == 0;
    std::string only_key = argc > 7 ? argv[7] : "";
    if (n < 2 || n > MAXN) {
        fprintf(stderr, "n must be in [2, %d]\n", MAXN);
        return 1;
    }
    build_levels(n);
    const std::vector<Tree> &T = levels[n].trees;
    int C = (int)T.size();

    std::map<std::string, ClassInfo> classes;
    const std::string unknot_key = "1*L^0*M^0 ";
    long long examined = 0, canonical = 0, prime = 0, knots = 0, cache_hits = 0;
    std::unordered_map<std::string, std::string> cache;
    const size_t max_cache = 1000000;
    Diagram D;
    int walk[8 * MAXN];
    // vec mode: (T+, T-) is in vec{F} iff T+ and T- have the same parity, so the candidates for T- are
    // only the trees of the same parity class (the cost is proportional to the size of vec{F})
    std::unordered_map<uint32_t, std::vector<int>> same_parity;
    if (vec)
        for (int t = 0; t < C; t++) same_parity[T[t].parity].push_back(t);  // increasing indices
    for (int i = shard; i < C; i += nshards) {
        int fi = T[i].flip;
        if (!vec && fi < i) continue;  // (flip T+, flip T-) would come first (not with vec)
        const std::vector<int> *cand = vec ? &same_parity[T[i].parity] : nullptr;
        size_t start = vec ? std::lower_bound(cand->begin(), cand->end(), i) - cand->begin() : 0;
        size_t ncand = vec ? cand->size() - start : (size_t)(C - i);
        for (size_t q = 0; q < ncand; q++) {  // j >= i: (T-, T+) would come first if j < i
            int j = vec ? (*cand)[start + q] : i + (int)q;
            examined++;
            int fj = T[j].flip;
            std::pair<int, int> me(i, j);
            if (vec) {
                if (T[i].parity != T[j].parity) continue;  // not in vec{F} (j >= i: the inverse comes later)
            } else if (std::make_pair(j, i) < me || std::make_pair(fi, fj) < me || std::make_pair(fj, fi) < me) {
                continue;
            }
            canonical++;
            if ((T[i].bits[0] & T[j].bits[0]) | (T[i].bits[1] & T[j].bits[1]) |
                (T[i].bits[2] & T[j].bits[2]) | (T[i].bits[3] & T[j].bits[3]))
                continue;
            prime++;
            build_diagram(n, T[i], T[j], D);
            if (components(D, walk) != 1) continue;
            knots++;
            Gauss G = gauss_code(D, walk);
            simplify(G);
            std::string key = unknot_key;
            if (!G.seq.empty()) {
                std::string cg = gauss_canonical(G);
                auto it = cache.find(cg);
                if (it != cache.end()) {
                    key = it->second;
                    cache_hits++;
                } else {
                    key = homfly_key(homfly_input(G));
                    if (cache.size() < max_cache) cache.emplace(cg, key);
                }
            }
            ClassInfo &ci = classes[key];
            ci.count++;
            ci.min_crossings = std::min(ci.min_crossings, (int)G.seq.size() / 2);
            if ((int)ci.reps.size() < max_reps && (only_key.empty() || key == only_key))
                ci.reps.push_back({i, j, gauss_string(G)});
        }
    }

    FILE *f = fopen(outpath, "w");
    if (!f) {
        perror(outpath);
        return 1;
    }
    fprintf(f, "# n=%d shard=%d/%d examined=%lld canonical=%lld prime=%lld knots=%lld classes=%zu cache_hits=%lld\n",
            n, shard, nshards, examined, canonical, prime, knots, classes.size(), cache_hits);
    for (auto &kv : classes) {
        fprintf(f, "%s\t%lld\t%d\t", kv.first.c_str(), kv.second.count, kv.second.min_crossings);
        for (size_t r = 0; r < kv.second.reps.size(); r++)
            fprintf(f, "%s%s|%s|%s", r ? ";" : "", words_string(n, kv.second.reps[r].top).c_str(),
                    words_string(n, kv.second.reps[r].bottom).c_str(), kv.second.reps[r].gauss.c_str());
        fprintf(f, "\n");
    }
    fclose(f);
    return 0;
}
