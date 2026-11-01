"""
Certified verification of the index tables results/<G>_index.csv.

usage (from F_index/):   sage -python certify_indices.py GROUP [processes]      (GROUP = F, F3, Fvec, F3vec)

Every value of the tables rests on two kinds of statements, both checked here with exact or certified
methods only (no floating-point decision):

A. Exclusions. For every knot K of the complete check (results/complete_check_<G>.csv), every diagram of the
   HOMFLY-PT class of K with lower_bound <= n < index (n <= n_max if K is not found) is not K (up to mirror image
   and orientation). For each such diagram, in this order:
     1. its simplified diagram has fewer crossings than the crossing number of K, or it is a connected sum of
        diagrams with non-trivial Alexander polynomial (a composite knot, whereas K is prime);
     2. its knot Floer homology differs from that of K, up to mirror image (exact);
     3. its hyperbolic volume, computed with a verified hyperbolic structure (interval arithmetic), is disjoint
        from that of K;
     4. there is no combinatorial isomorphism between the verified canonical retriangulations of the two
        complements (if there is one, the diagram is K: this would contradict the table);
     5. if no verified hyperbolic structure is found: its complement contains an essential torus (Regina: a
        closed normal torus that is incompressible and is not parallel to the boundary, i.e. no piece obtained
        by cutting along it is T^2 x I), so it is a satellite knot, whereas K is hyperbolic.
   The knots of the table whose index equals the lower bound need no exclusion: their HOMFLY-PT class does not
   occur with smaller n (the polynomial is computed for every diagram).
B. Witnesses. For every knot with a known index, its witness diagram is K: a combinatorial isomorphism between
   the verified canonical retriangulations of the two complements (K hyperbolic), or, for a non-hyperbolic K,
   Sage's identification with KnotInfo of a diagram with at most 13 crossings (unique match by HOMFLY-PT
   polynomial and determinant among the knots of KnotInfo).
Every verified computation is retried on randomized triangulations. Progress: tmp_check/certify_<G>.jsonl
(resumed). Output: results/certified_<G>.md.
"""
import csv
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
STEP = 25           # diagrams per task
TIMEOUT = int(os.environ.get('CERTIFY_TIMEOUT', 180))  # seconds per diagram; more: reported as not certified
WITNESS_BATCH = 1
_K = {}             # per process: knot -> data


# ------------------------------------------------------------------------------------------------ helpers

def verified(E, f, tries=20):
    err = None
    for _ in range(tries):
        try:
            return f(E)
        except Exception as e:  # noqa: PERF203
            err = e
            E.randomize()
    raise err


def volume(E):
    return verified(E, lambda X: X.volume(verified=True, bits_prec=100))


def canonical(E):
    return verified(E, lambda X: X.canonical_retriangulation(verified=True))


def hfk(L):
    r = L.knot_floer_homology()['ranks']
    return frozenset(r.items()), frozenset(((-a, -m), v) for (a, m), v in r.items())


def knot_pd(knot):
    """PD code of the KnotInfo diagram of the knot."""
    from sage.all import KnotInfo
    return [list(map(int, c)) for c in getattr(KnotInfo, 'K' + knot).link().pd_code()]


def knot_exterior(knot):
    import snappy  # noqa: F401
    import spherogram
    return spherogram.Link([[x - 1 for x in c] for c in knot_pd(knot)]).exterior()


def knot_data(knot):
    """(crossing number, HFK, verified volume or None, verified canonical retriangulation or None, PD)."""
    if knot not in _K:
        import snappy  # noqa: F401
        import spherogram
        from sage.all import KnotInfo
        K = getattr(KnotInfo, 'K' + knot)
        pd = knot_pd(knot)
        L = spherogram.Link([[x - 1 for x in c] for c in pd])
        E = L.exterior()
        try:
            vol, can = volume(E), canonical(E)
        except Exception:
            vol = can = None  # not hyperbolic (or not verified)
        _K[knot] = (int(K.crossing_number()), hfk(L)[0], vol, can, pd)
    return _K[knot]


def pd_of(group, top, bottom, pd_field=None):
    if pd_field:
        return json.loads(pd_field)
    if group in ('F', 'Fvec'):
        import ftrees as F
        return F.pd_code(F.from_leaf_words(top.split(',')), F.from_leaf_words(bottom.split(',')))
    out = subprocess.run([os.path.join(HERE, 'bin', 'iota_knots'), 'eval'], input='F3 %s %s\n' % (top, bottom),
                         capture_output=True, text=True, check=True).stdout
    return json.loads(dict(kv.split('=', 1) for kv in out.strip().split('\t'))['pd'])


def covers(E, maxdeg=5):
    """Sorted homology groups of the connected covers of degree 2..maxdeg of the complement (exact: the covers
    come from the transitive permutation representations of the fundamental group). A topological invariant
    of the complement, hence of the knot up to mirror image."""
    return sorted((d, C.covering_type(), str(C.homology())) for d in range(2, maxdeg + 1) for C in E.covers(d))


def essential_torus(E):
    """True if Regina finds an essential torus in the complement (incompressible, not boundary parallel)."""
    import regina
    T = regina.Triangulation3.fromIsoSig(E.triangulation_isosig(decorated=False))
    T.idealToFinite()
    T.simplify()
    for s in regina.NormalSurfaces(T, regina.NS_STANDARD):
        if not (s.isCompact() and not s.hasRealBoundary() and s.eulerChar() == 0 and s.isOrientable()
                and s.isConnected() and s.isTwoSided()):
            continue
        if not s.isIncompressible():
            continue
        if any(c.isTxI() for c in s.cutAlong().triangulateComponents()):
            continue
        return True
    return False


def same_complement(E, F, tries=2000):
    """True if random retriangulations of the two knot complements reach the same triangulation (equal
    isomorphism signatures): the complements are then homeomorphic, and so are the knots up to mirror image
    (Gordon-Luecke). Exact and valid for every knot, hyperbolic or not. False means 'not found'."""
    sigs = set()
    for _ in range(200):
        F.randomize()
        sigs.add(F.triangulation_isosig(decorated=False))
    for _ in range(tries):
        if E.triangulation_isosig(decorated=False) in sigs:
            return True
        E.randomize()
    return False


def not_K(pd, knot):
    """('ok', method) if the diagram is certified not to be K; ('violation', ...) if it is certified to be K;
    ('uncertified', reason) otherwise."""
    import snappy  # noqa: F401
    import spherogram
    c, h, vol, can, _ = knot_data(knot)
    L = spherogram.Link([[x - 1 for x in c_] for c_ in pd])
    L.simplify('global')
    if len(L.crossings) < c:
        return 'ok', 'crossings'
    pieces = L.deconnect_sum()
    if len(pieces) > 1 and all(P.alexander_polynomial() != 1 for P in pieces):
        return 'ok', 'composite'  # a sum of non-trivial knots is not prime (Schubert), and K is prime
    try:
        if h not in hfk(L):
            return 'ok', 'hfk'
    except Exception:
        pass
    E = L.exterior()
    try:
        v = volume(E)
    except Exception:
        v = None
    if v is not None and vol is not None:
        if v.upper() < vol.lower() or v.lower() > vol.upper():
            return 'ok', 'volume'
        try:
            D = canonical(E)
        except Exception as e:
            return 'uncertified', 'canonical: %s' % str(e)[:50]
        if D.isomorphisms_to(can):
            return 'violation', 'isometric to K'
        return 'ok', 'canonical'
    if v is None and vol is not None:
        try:
            if covers(E) != covers(knot_exterior(knot)):
                return 'ok', 'covers'
        except Exception:
            pass
        try:
            if essential_torus(E):
                return 'ok', 'essential torus'
        except Exception as e:
            return 'uncertified', 'regina: %s' % str(e)[:50]
        return 'uncertified', 'no hyperbolic structure, no essential torus found'
    return 'uncertified', 'K not hyperbolic'


def is_K(pd, knot):
    """('ok', method) if the witness is certified to be K, ('uncertified', reason) otherwise."""
    import snappy  # noqa: F401
    import spherogram
    c, h, vol, can, _ = knot_data(knot)
    L = spherogram.Link([[x - 1 for x in c_] for c_ in pd])
    L.simplify('global')
    if can is not None:
        try:
            if canonical(L.exterior()).isomorphisms_to(can):
                return 'ok', 'canonical'
            return 'violation', 'not isometric to K'
        except Exception as e:
            return 'uncertified', 'canonical: %s' % str(e)[:50]
    if len(L.crossings) <= 13:
        from identify_lib import knotinfo_name
        if knotinfo_name(L) == knot:
            return 'ok', 'knotinfo'
    return 'uncertified', 'K not hyperbolic'


# ------------------------------------------------------------------------------------------------ tasks

class Timeout(Exception):
    pass


def timed(f, *args):
    """f(*args) with a time limit of TIMEOUT seconds: ('uncertified', 'timeout') if exceeded. The alarm of
    cysignals also interrupts the C code of SnapPy/Sage that is protected by sig_on; as a last resort, a call
    lasting more than 3 * TIMEOUT ends the worker process (faulthandler), and RobustPool reports the task as
    crashed (never as certified)."""
    import faulthandler
    from cysignals.alarm import alarm, cancel_alarm, AlarmInterrupt
    faulthandler.dump_traceback_later(3 * TIMEOUT, exit=True)
    alarm(TIMEOUT)
    try:
        return f(*args)
    except (AlarmInterrupt, Timeout):
        return 'uncertified', 'timeout (%d s)' % TIMEOUT
    finally:
        cancel_alarm()
        faulthandler.cancel_dump_traceback_later()


def exclusion_task(task):
    group, knot, path, offset, count = task
    out = {'task': task, 'ok': {}, 'violations': [], 'uncertified': []}
    with open(path) as f:
        f.seek(offset)
        for _ in range(count):
            line = f.readline()
            if not line:
                break
            fl = line.rstrip('\n').split('\t')
            try:
                kind, info = timed(not_K, pd_of(group, fl[1], fl[2], fl[3] if len(fl) > 3 else None), knot)
            except Exception as e:
                kind, info = 'uncertified', str(e)[:60]
            if kind == 'ok':
                out['ok'][info] = out['ok'].get(info, 0) + 1
            else:
                out['violations' if kind == 'violation' else 'uncertified'].append((fl[1], fl[2], info))
    return out


def witness_task(task):
    group, items = task
    out = {'task': ['witness1', items[0][0]], 'ok': {}, 'violations': [], 'uncertified': []}
    for knot, top, bottom in items:
        try:
            kind, info = timed(is_K, pd_of(group, top, bottom), knot)
        except Exception as e:
            kind, info = 'uncertified', str(e)[:60]
        if kind == 'ok':
            out['ok'][info] = out['ok'].get(info, 0) + 1
        else:
            out['violations' if kind == 'violation' else 'uncertified'].append((knot, top, bottom, info))
    return out


def inputs(group):
    """The table of the group, the HOMFLY-PT keys of the complete-check knots and the largest n enumerated."""
    raw = {'F': 'raw', 'F3': 'raw_F3', 'Fvec': 'raw_Fvec', 'F3vec': 'raw_F3vec'}[group]
    nmax = max(int(m) for m in re.findall(r'n(\d+)\.tsv', ' '.join(os.listdir(os.path.join(HERE, 'results', raw)))))
    table = {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', group + '_index.csv')))}
    keys = {}
    for line in open(os.path.join(HERE, 'tmp_check', 'targets_%s.tsv' % group)):
        k, lb, hi, key = line.rstrip('\n').split('\t')
        keys[k] = key
    return table, keys, nmax


def exclusion_tasks(group, table, keys, nmax):
    """The exclusion tasks [group, knot, path, offset, count] of part A."""
    tasks = []
    for r in csv.DictReader(open(os.path.join(HERE, 'results', 'complete_check_%s.csv' % group))):
        k = r['knot']
        idx = table[k][group + '_index']
        hi = int(idx) if idx else nmax + 1
        for n in range(int(r['lower_bound']), hi):
            d = os.path.join(HERE, 'tmp_check', '%s_n%d' % (group, n), 'classes', 'index.json')
            if not os.path.exists(d):
                if group in ('Fvec', 'F3vec') and n % 2 == 0:
                    continue  # no knots for even n
                sys.exit('missing %s' % d)
            for path, offset, count in json.load(open(d)).get(keys[k], []):
                with open(path, 'rb') as f:
                    f.seek(offset)
                    pos = offset
                    for s in range(0, count, STEP):
                        tasks.append([group, k, path, pos, min(STEP, count - s)])
                        for _ in range(min(STEP, count - s)):
                            f.readline()
                        pos = f.tell()
    return tasks


def main():
    from identify_lib import RobustPool
    group = sys.argv[1]
    processes = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    table, keys, nmax = inputs(group)

    # A. exclusions
    tasks = exclusion_tasks(group, table, keys, nmax)
    # B. witnesses
    wit = [(k, r['top_tree'], r['bottom_tree']) for k, r in table.items()
           if r[group + '_index'] and r['top_tree'] and int(r['crossing_number']) >= 3]
    # witnesses already certified in batches of 20 (earlier runs) are not redone
    covered = set()
    progress_file = os.path.join(HERE, 'tmp_check', 'certify_%s.jsonl' % group)
    if os.path.exists(progress_file):
        old_keys = {json.dumps(json.loads(line)['task']) for line in open(progress_file)}
        for i in range(0, len(wit), 20):
            if json.dumps(['witness', wit[i][0]]) in old_keys:
                covered.update(k for k, _, _ in wit[i:i + 20])
    wit = [w for w in wit if w[0] not in covered]
    # then those certified in batches of 5
    if os.path.exists(progress_file):
        covered5 = set()
        for i in range(0, len(wit), 5):
            if json.dumps(['witness5', wit[i][0]]) in old_keys:
                covered5.update(k for k, _, _ in wit[i:i + 5])
        wit = [w for w in wit if w[0] not in covered5]
    wtasks = [[group, wit[i:i + WITNESS_BATCH]] for i in range(0, len(wit), WITNESS_BATCH)]

    progress = os.path.join(HERE, 'tmp_check', 'certify_%s.jsonl' % group)
    done = {}
    if os.path.exists(progress):
        for line in open(progress):
            r = json.loads(line)
            done[json.dumps(r['task'])] = r
    todo = [t for t in tasks if json.dumps(t) not in done]
    wtodo = [t for t in wtasks if json.dumps(['witness1', t[1][0][0]]) not in done]
    print('%s: %d exclusion tasks (%d done), %d witness tasks (%d done)' % (
        group, len(tasks), len(tasks) - len(todo), len(wtasks), len(wtasks) - len(wtodo)), flush=True)
    with RobustPool(processes) as pool, open(progress, 'a') as prog:
        for func, ts in ((witness_task, wtodo), (exclusion_task, todo)):
            for i, r in enumerate(pool.map(func, ts), 1):
                prog.write(json.dumps(r) + '\n')
                prog.flush()
                done[json.dumps(r['task'])] = r
                if i % 200 == 0:
                    print('  %s: %d / %d' % (func.__name__, i, len(ts)), flush=True)
        dropped = list(pool.dropped)

    stats = {'exclusions': {}, 'witnesses': {}}
    viol, unc = [], []
    for key, r in done.items():
        part = 'witnesses' if r['task'][0] in ('witness', 'witness5', 'witness1') else 'exclusions'
        for m, c in r['ok'].items():
            stats[part][m] = stats[part].get(m, 0) + c
        viol += [(part,) + tuple(v) for v in r['violations']]
        unc += [(part,) + tuple(u) for u in r['uncertified']]
    lines = ['# Certified verification of the %s-index table' % group, '',
             'Script `certify_indices.py` (exact or certified methods only, see its docstring).', '',
             '- exclusions (diagrams certified not to be the knot): %s' % stats['exclusions'],
             '- witnesses (diagrams certified to be the knot): %s' % stats['witnesses'],
             '- **contradictions with the table: %d**' % len(viol),
             '- not certified: %d; crashed tasks: %d' % (len(unc), len(dropped)), '']
    if viol:
        lines += ['## Contradictions', ''] + ['- %s' % (v,) for v in viol] + ['']
    if unc:
        lines += ['## Not certified', ''] + ['- %s' % (u,) for u in unc[:500]] + ['']
    if dropped:
        lines += ['## Crashed tasks', ''] + ['- %s' % (t[:2],) for t in dropped] + ['']
    open(os.path.join(HERE, 'results', 'certified_%s.md' % group), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[:9]))


if __name__ == '__main__':
    main()
