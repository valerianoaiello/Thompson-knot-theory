# Checks of bin/iota_knots (F_3, and F through Jones' map iota). Ported from the former nuovo_codice/.
# Run from F_index/:   sage tests/check_iota_engine.sage
#
# 1) The PD code (built only from the geometry of the tree diagram) and the oriented Gauss code (whose
#    crossing signs come from our own rule) give the same HOMFLY in Sage, equal to the one of libhomfly
#    in C++; the Reidemeister I/II simplification does not change it. Random diagrams of F and F_3.
# 2) Agreement with the author's earlier ternary code (directory $THOMPSON_OLD_CODE, skipped if absent) (up to mirror image, see
#    tests/check_graft_and_old_code.sage for the cases where the old code returns the mirror).
# 3) Example 2.3 of the paper: iota(x0 x2^2 x5 x6 (x4 x6 x7)^-1) gives the knot 4_1.
# 4) For F, bin/iota_knots (construction through iota) and bin/fknots (Tait graph) are independent
#    implementations: they must give the same counts and the same HOMFLY classes.
import os, random, subprocess, sys, tempfile
from sage.libs.homfly import homfly_polynomial_string

HERE = os.getcwd()
IOTA = os.path.join(HERE, 'bin', 'iota_knots')
FKNOTS = os.path.join(HERE, 'bin', 'fknots')
# the author's earlier Python implementation (optional; its location can be set with THOMPSON_OLD_CODE)
OLD = os.environ.get('THOMPSON_OLD_CODE', os.path.join(HERE, '..', 'old_code'))

random.seed(int(2026))
failures = 0


def check(cond, msg):
    global failures
    if not cond:
        failures += 1
        print('FAIL:', msg)


def random_words(internal, arity):
    """Leaf words of a random tree with `internal` internal vertices."""
    if internal == 0:
        return ['']
    sizes = [0] * arity
    for _ in range(internal - 1):
        sizes[random.randrange(arity)] += 1
    out = []
    for i, s in enumerate(sizes):
        out += [str(i) + w for w in random_words(s, arity)]
    return out


def fix(words):
    return ['0'] if words == [''] else words


def run_eval(lines):
    p = subprocess.run([IOTA, 'eval'], input='\n'.join(lines) + '\n', capture_output=True,
                       text=True, check=True)
    return [dict(item.split('=', 1) for item in line.split('\t')) for line in p.stdout.strip().split('\n')]


def libhomfly_string(L):
    """The string libhomfly returns for the Sage link L (same input Sage builds)."""
    ogc = L.oriented_gauss_code()
    if not ogc[0]:
        return '1'
    s = '{}'.format(L.number_of_components())
    for comp in ogc[0]:
        s += ' {}'.format(len(comp))
        for cr in comp:
            s += ' {} {}'.format(abs(cr) - 1, sign(cr))
    for i, cr in enumerate(ogc[1]):
        s += ' {} {}'.format(i, cr)
    return homfly_polynomial_string(s).strip()


def link_from_ogc(ogc):
    ogc = sage_eval(ogc)
    return Link([]) if not ogc[0] else Link([[ogc[0]], ogc[1]])


def homfly(L):
    return L.homfly_polynomial('L', 'M', 'lm')


# 1) internal consistency against Sage --------------------------------------------------------
pairs = []
for _ in range(int(400)):
    group = random.choice(['F', 'F3'])
    arity = 2 if group == 'F' else 3
    k = random.randint(1, 7 if group == 'F' else 5)
    pairs.append((group, fix(random_words(k, arity)), fix(random_words(k, arity))))
res = run_eval(['{} {} {}'.format(g, ','.join(t), ','.join(b)) for g, t, b in pairs])
nknots = 0
for (g, t, b), r in zip(pairs, res):
    if 'pd' not in r:
        continue
    nknots += 1
    Lpd = Link(sage_eval(r['pd']))
    check(Lpd.number_of_components() == 1, 'components {}'.format((g, t, b)))
    H = homfly(Lpd)
    check(H == homfly(link_from_ogc(r['full_ogc'])), 'signs of the Gauss code {}'.format((g, t, b)))
    check(H == homfly(link_from_ogc(r['ogc'])), 'simplification {}'.format((g, t, b)))
    check(libhomfly_string(Lpd) == r['full_homfly'], 'C++ HOMFLY string {}'.format((g, t, b)))
print('1) checked {} knot diagrams out of {} random pairs'.format(nknots, len(pairs)))

# 2) old code ---------------------------------------------------------------------------------
if os.path.isdir(OLD):
    sys.path.insert(0, OLD)
    import group_operations as go
    import knot_construction as kc

    agree = mirror = other = crash = 0
    old_pairs = [(fix(random_words(random.randint(1, 4), 3)), fix(random_words(random.randint(1, 4), 3)))
                 for _ in range(int(300))]
    old_pairs = [(t, b) for t, b in old_pairs if len(t) == len(b)]
    res = run_eval(['F3 {} {}'.format(','.join(t), ','.join(b)) for t, b in old_pairs])
    for (t, b), r in zip(old_pairs, res):
        if 'pd' not in r:
            continue
        try:
            Hold = homfly(Link(kc.tree_diagram_to_planar_diagram(go.Ternary_tree_diagrams(list(t), list(b)))))
        except Exception:
            crash += 1
            continue
        Lnew = Link(sage_eval(r['pd']))
        if Hold == homfly(Lnew):
            agree += 1
        elif Hold == homfly(Lnew.mirror_image()):
            mirror += 1
        else:
            other += 1
    print('2) old code: agree={} mirror={} different={} old-code-crash={}'.format(agree, mirror, other, crash))
    check(other == 0, 'disagreement with the old code')
else:
    print('2) old code not found in %s: skipped' % OLD)

# 3) Example 2.3 ------------------------------------------------------------------------------
sys.path.insert(0, HERE)
import ftrees as FT
# x0 x2^2 x5 x6 (x4 x6 x7)^-1 = x0 x2 x2 x5 x6 x7^-1 x6^-1 x4^-1, sent to F_3 by iota inside bin/iota_knots
g = FT.word(0, 2, 2, 5, 6, -7, -6, -4)
r = run_eval(['F {} {}'.format(','.join(FT.leaf_words(g[0])), ','.join(FT.leaf_words(g[1])))])[0]
K = link_from_ogc(r['ogc'])
print('3) Example 2.3 ->', K.get_knotinfo())
check(str(K.get_knotinfo()) == "KnotInfo['K4_1']", 'Example 2.3')

# 4) iota_knots F == fknots -------------------------------------------------------------------
tmp = tempfile.mkdtemp()


def load(path):
    lines = open(path).read().split('\n')
    head = dict(kv.split('=') for kv in lines[0][2:].split() if '=' in kv)
    return head, {l.split('\t')[0]: int(l.split('\t')[1]) for l in lines[1:] if l}


for n in range(2, 9):
    a, b = os.path.join(tmp, 'iota.tsv'), os.path.join(tmp, 'tait.tsv')
    subprocess.run([IOTA, 'F', str(n), '0', '1', a, '1'], check=True)
    subprocess.run([FKNOTS, str(n), '0', '1', b, '1'], check=True)
    (ha, ca), (hb, cb) = load(a), load(b)
    same = ca == cb and all(ha[k] == hb[k] for k in ('canonical', 'prime', 'knots'))
    check(same, 'iota_knots and fknots differ at n = %d' % n)
print('4) iota_knots F and fknots agree for n = 2..8')

print('FAILURES:', failures)
