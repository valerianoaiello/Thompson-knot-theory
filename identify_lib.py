"""
Identification of the knots found by run.py (used by identify.sage, which only calls main()).

usage (from F_index/):   sage identify.sage [max_crossing_number_in_output] [F|F3] [processes]

For every prime knot K of the table (up to mirror image):
  * lower bound for the F-index: the first n at which a diagram with the HOMFLY polynomial of K appears
    (no diagram with fewer leaves can be K);
  * F-index = n if, among the stored representatives at that n, one is identified as K: the diagram
    (already Reidemeister I/II simplified by fknots) is simplified further with spherogram and given to
    Sage's get_knotinfo (when it has <= 13 crossings: then the knot has crossing number <= 13, so it is
    in KnotInfo and the identification is a proof); if this fails or is ambiguous (several knots with
    the same HOMFLY), SnapPy identifies the complement (census of knots up to 15 crossings; by
    Gordon-Luecke the complement determines the knot up to mirror image).
Results: results/F_index.csv, results/F_index_summary.txt, results/unidentified_classes.csv (names,
when possible, the composite knots and the knots with 14-15 crossings), results/knots_beyond_table.csv.
With F3 the input is results/raw_F3/ (python3 run.py N --group F3) and the files are called
F3_index.csv, F3_index_summary.txt, unidentified_classes_F3.csv, knots_beyond_table_F3.csv.

Parallelism: n is processed in increasing order (a knot is new at n only if it was not identified
before), but within each n the HOMFLY classes are independent and are distributed over a pool of
processes; the same holds for reading the KnotInfo table and for naming the unidentified classes.
The pool uses 'spawn': SnapPy's sqlite database crashes in forked processes on macOS.
Some diagrams make a compiled library (SnapPy/spherogram) crash the whole worker process (SIGILL):
see robust_map, which restarts the pool and isolates the guilty representatives.
"""
import csv
import glob
import multiprocessing as mp
import os
import re
import sys
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from concurrent.futures.process import BrokenProcessPool

from cysignals.alarm import alarm, cancel_alarm, AlarmInterrupt
from sage.all import Link, KnotInfo, LaurentPolynomialRing, ZZ
import snappy  # noqa: F401  (needed by spherogram for exteriors)
import spherogram

TIMEOUT = 30        # seconds for each call to get_knotinfo / SnapPy ...
LONG_TIMEOUT = 600  # ... and for the second try of get_knotinfo after a timeout (with a busy CPU
                    # get_knotinfo can take more than 30 s on a 13-crossing diagram: a timeout must
                    # not make the result depend on the load of the machine)
NAME_REPS = int(os.environ.get('NAME_REPS', 1))  # representatives used to name the classes of
                    # unidentified_classes.csv (there are tens of thousands of them at n = 13)
TIMEOUTS = []       # representatives on which get_knotinfo timed out twice (per process)

RV = LaurentPolynomialRing(ZZ, 'v,z')
v, z = RV.gens()


def canonical_vz(p):
    """Canonical form of a knot HOMFLY polynomial (normalization vz) up to mirror image."""
    p = RV(p)
    q = p.subs(v=v**-1)
    t = lambda r: tuple(sorted((tuple(e), int(c)) for e, c in r.dict().items()))
    return min(t(p), t(q))


def lm_key_to_vz(key):
    """Convert the key written by fknots (libhomfly variables L, M) into Sage's vz normalization."""
    p = RV(0)
    for term in key.split():
        c, l, m = term.split('*')
        c, l, m = int(c), int(l[2:]), int(m[2:])
        sign = 1 if (l + m) % 4 == 0 else -1       # lm -> az (for knots), see Link.homfly_polynomial
        p += sign * c * v**(-l) * z**m             # az -> vz : a = v^-1
    return p


def base_name(k):
    """KnotInfo['K3_1m'] -> '3_1' (we work up to mirror image; r = reverse, c = mirror of reverse)."""
    m = re.search(r"K([0-9]+[an]?_[0-9]+)[mrc]?'", str(k))
    return m.group(1) if m else str(k)


class TimedOut(Exception):
    pass


def with_timeout(f, *args, timeout=TIMEOUT, raise_timeout=False):
    """f(*args), or None if it fails or takes more than `timeout` seconds (with raise_timeout,
    a timeout raises TimedOut instead)."""
    try:
        alarm(timeout)
        try:
            return f(*args)
        finally:
            cancel_alarm()
    except AlarmInterrupt:
        if raise_timeout:
            raise TimedOut()
        return None
    except Exception:
        return None


def simplified(seq, hands):
    """Spherogram link of a Gauss code "seq|hands" of fknots, simplified ('global')."""
    K = Link([[[int(a) for a in seq.split(',')]], [int(a) for a in hands.split(',')]])
    S = spherogram.Link([[int(x) for x in c] for c in K.pd_code()])
    S.simplify('global')
    return S


def sage_link(S):
    return Link([[int(x) + 1 for x in c] for c in S.PD_code()])  # spherogram is 0-based


def knotinfo_name(S):
    """Name (up to mirror) of a prime knot recognized by get_knotinfo, the product for composite
    knots, None if it cannot be decided."""
    if len(S.crossings) > 13:
        return None
    f = lambda: list(sage_link(S).get_knotinfo())
    try:
        res = with_timeout(f, raise_timeout=True)
    except TimedOut:
        try:
            res = with_timeout(f, timeout=LONG_TIMEOUT, raise_timeout=True)
        except TimedOut:
            TIMEOUTS.append(S.PD_code())
            return None
    if not res:
        return None
    return ' # '.join(sorted(base_name(k) for k, e in res for _ in range(e)))


def snappy_name(S):
    """Name (up to mirror) of the knot from its complement, 'non-hyperbolic' or None."""
    E = S.exterior()
    ids = with_timeout(E.identify) or []
    names = [str(M).split('(')[0] for M in ids]
    for name in names:  # KnotInfo uses Hoste-Thistlethwaite names above 10 crossings
        m = re.fullmatch(r'K(\d+)([an])(\d+)', name)
        if m and int(m.group(1)) > 10:
            return '%s%s_%s' % m.groups()
    for name in names:  # ... and Rolfsen names up to 10
        m = re.fullmatch(r'(\d+)_\d+', name)
        if m and int(m.group(1)) <= 10:
            return name
    if E.solution_type() != 'all tetrahedra positively oriented':
        return 'non-hyperbolic'
    return None


def is_beyond(nm):
    return bool(nm) and re.fullmatch(r'1[45][an]_\d+', nm) is not None


# ---------------------------------------------------------------------------------------------
# tasks run in the pool
# ---------------------------------------------------------------------------------------------

def read_knotinfo(names):
    """(name, crossing number, HOMFLY vz, canonical HOMFLY) for the given KnotInfo items."""
    out = []
    for item in names:
        K = KnotInfo[item]
        if not K.is_knot() or K.crossing_number() > 13:
            continue
        h = K.homfly_polynomial()
        out.append((K.value, K.crossing_number(), h, canonical_vz(h)))
    return out


def identify_class(task):
    """Tries the representatives of one HOMFLY class until all the knots in `todo` are found.
    Returns the knots found [(name, top, bottom, crossings)] and the 14-15 crossing knots met."""
    todo, reps = set(task[0]), task[1]
    found, beyond = [], []
    del TIMEOUTS[:]
    for top, bottom, seq, hands in reps:
        if not todo:
            break
        if not seq:
            continue
        S = with_timeout(simplified, seq, hands)
        if S is None or not S.crossings:
            continue
        nm = knotinfo_name(S)
        if nm not in todo:  # ambiguous HOMFLY, > 13 crossings, ...: all the representatives
            nm = snappy_name(S)  # are tried, since a class can contain several knots
            # (e.g. 14n_2554 has the HOMFLY of 13n_2638)
            if is_beyond(nm):
                beyond.append((nm, top, bottom))
        if nm in todo:
            todo.discard(nm)
            found.append((nm, top, bottom, len(S.crossings)))
    return found, beyond, len(TIMEOUTS)


def name_class(reps):
    """Names of the knots of a class not in the table, from a few representatives: KnotInfo
    (composite knots) or SnapPy (prime knots with 14-15 crossings). Several names = different knots
    with the same HOMFLY."""
    knots, beyond = set(), []
    for top, bottom, seq, hands in reps[:NAME_REPS]:
        S = with_timeout(simplified, seq, hands) if seq else None
        if S is None or not S.crossings:
            continue
        nm = knotinfo_name(S) or snappy_name(S)
        if is_beyond(nm):
            beyond.append((nm, top, bottom))
        knots.add(nm if nm else '? (%d crossings)' % len(S.crossings))
    return ' / '.join(sorted(knots)), beyond


# ---------------------------------------------------------------------------------------------
# a process pool that survives crashes of the workers
# ---------------------------------------------------------------------------------------------

class RobustPool:
    """map over a pool of 'spawn' processes that survives the death of a worker (e.g. SIGILL inside
    SnapPy).

    At most one task per process is in flight, so when the pool breaks only the tasks that were
    running are suspect (a ProcessPoolExecutor fails *all* its pending futures, so they must not be
    queued in it). The suspects are run again one at a time in an isolated single process: a task
    that crashes it alone is the culprit; it is split with `split` (if given) and its pieces are run
    one at a time again; only a piece that crashes the process alone and cannot be split is dropped.
    Dropped tasks are kept in self.dropped; more than max_dropped of them is an error."""

    def __init__(self, processes, max_dropped=100):
        self.processes = processes
        self.max_dropped = max_dropped
        self.ex = None
        self.dropped = []
        self.crashes = 0

    def __enter__(self):
        self.ex = self._new(self.processes)
        return self

    def __exit__(self, *exc):
        self.ex.shutdown(cancel_futures=True)

    @staticmethod
    def _new(processes):
        return ProcessPoolExecutor(processes, mp_context=mp.get_context('spawn'))

    def map(self, func, tasks, split=None):
        """Yields func(task) for every task (in completion order); for a task that had to be split,
        the results of its pieces are yielded instead."""
        pending = list(tasks)[::-1]
        running = {}  # future -> task
        while pending or running:
            while pending and len(running) < self.processes:
                t = pending.pop()
                running[self.ex.submit(func, t)] = t
            done, _ = wait(running, return_when=FIRST_COMPLETED)
            suspects = []
            for fut in done:
                t = running.pop(fut)
                try:
                    res = fut.result()
                except BrokenProcessPool:
                    suspects.append(t)
                    continue
                yield res
            if not suspects:
                continue
            # the pool is dead: the other running tasks are suspect too (unless they finished)
            for fut, t in running.items():
                if fut.done() and not isinstance(fut.exception(), BrokenProcessPool):
                    yield fut.result()
                else:
                    suspects.append(t)
            running = {}
            self.crashes += 1
            print('  a worker process crashed: %d running tasks are run again one at a time'
                  % len(suspects), flush=True)
            self.ex.shutdown(cancel_futures=True)
            yield from self._isolated(func, suspects, split)
            self.ex = self._new(self.processes)

    def _isolated(self, func, tasks, split):
        ex = self._new(1)
        queue = list(tasks)
        try:
            while queue:
                t = queue.pop(0)
                try:
                    res = ex.submit(func, t).result()
                except BrokenProcessPool:
                    ex.shutdown(cancel_futures=True)
                    ex = self._new(1)
                    pieces = split(t) if split else None
                    if pieces and len(pieces) > 1:
                        queue = pieces + queue
                    else:
                        self.dropped.append(t)
                        print('  dropped one task that crashes the process by itself (%d so far)'
                              % len(self.dropped), flush=True)
                        if len(self.dropped) > self.max_dropped:
                            raise RuntimeError('more than %d tasks crash SnapPy/spherogram: '
                                               'something is wrong' % self.max_dropped)
                    continue
                yield res
        finally:
            ex.shutdown(cancel_futures=True)


def split_class(task):
    """A class (todo, reps) as one task per representative."""
    todo, reps = task
    return [(todo, [r]) for r in reps]


def name_class_task(task):
    return task[0], name_class(task[1])


def split_name_task(task):
    i, reps = task
    return [(i, reps[j:j + 1]) for j in range(min(len(reps), NAME_REPS))]


# ---------------------------------------------------------------------------------------------

def main(argv):
    here = os.getcwd()
    max_c_out = int(argv[0]) if len(argv) > 0 else 13
    group = argv[1] if len(argv) > 1 else 'F'
    processes = int(argv[2]) if len(argv) > 2 else os.cpu_count()
    assert group in ('F', 'F3')
    raw = os.path.join(here, 'results', 'raw' if group == 'F' else 'raw_F3')
    suffix = '' if group == 'F' else '_F3'

    with RobustPool(processes) as pool:
        print('reading the KnotInfo table on %d processes ...' % processes, flush=True)
        items = [K.name for K in KnotInfo]
        chunks = [items[i::processes * 4] for i in range(processes * 4)]
        table = {}      # name -> (crossing number, vz polynomial)
        by_homfly = {}  # canonical HOMFLY -> list of names
        for part in pool.map(read_knotinfo, chunks):
            for name, c, h, key in part:
                table[name] = (c, h)
                by_homfly.setdefault(key, []).append(name)
        for names in by_homfly.values():
            names.sort()
        print('%d knots, %d distinct HOMFLY polynomials up to mirror' % (len(table), len(by_homfly)),
              flush=True)

        files = sorted(glob.glob(os.path.join(raw, 'n*.tsv')),
                       key=lambda f: int(re.findall(r'n(\d+)\.tsv', f)[0]))
        ns = [int(re.findall(r'n(\d+)\.tsv', f)[0]) for f in files]
        nmax = max(ns)

        timeouts = 0             # representatives on which get_knotinfo timed out twice
        lower = {'0_1': 1}       # name -> first n where its HOMFLY appears
        index = {'0_1': 1}       # name -> n where it is identified (F-index)
        example = {'0_1': ('', '', 0)}
        unknown_classes = []     # HOMFLY classes not in the table (composite knots or > 13 crossings)
        beyond = {}              # knots with 14-15 crossings found by SnapPy -> (first n, top, bottom)

        def note_beyond(items, n):
            for nm, top, bottom in items:
                if nm not in beyond or beyond[nm][0] > n:
                    beyond[nm] = (n, top, bottom)

        for n, fname in zip(ns, files):
            tasks = []
            with open(fname) as f:
                for line in f:
                    if line.startswith('#'):
                        continue
                    key, count, mincr, reps = line.rstrip('\n').split('\t')
                    reps = [tuple(r.split('|')) for r in reps.split(';') if r]
                    h = lm_key_to_vz(key)
                    names = by_homfly.get(canonical_vz(h), [])
                    if not names:
                        unknown_classes.append((n, int(count), int(mincr), h, reps))
                        continue
                    for nm in names:
                        lower.setdefault(nm, n)
                    todo = [nm for nm in names if nm not in index]
                    if not todo or names == ['0_1']:
                        continue
                    tasks.append((todo, reps))
            # big classes first, for a better load balance
            tasks.sort(key=lambda t: -len(t[1]))
            found_now = []
            for found, bey, nto in pool.map(identify_class, tasks, split=split_class):
                timeouts += nto
                note_beyond(bey, n)
                for nm, top, bottom, cr in found:
                    if nm not in index:
                        index[nm] = n
                        example[nm] = (top, bottom, cr)
                        found_now.append(nm)
            print('n = %2d: %d classes to check, identified %s' % (
                n, len(tasks), ', '.join(sorted(found_now, key=lambda s: (table[s][0], s))) or '-'),
                flush=True)

        # unidentified classes (one line per HOMFLY, at its first n)
        print('naming the HOMFLY classes not in the table ...', flush=True)
        first = {}
        for cl in unknown_classes:
            first.setdefault(canonical_vz(cl[3]), cl)
        unknown = sorted(first.values(), key=lambda cl: cl[0])
        parts = {}  # index of the class -> (names, beyond) of its pieces
        for i, (knots, bey) in pool.map(name_class_task, list(enumerate(cl[4] for cl in unknown)),
                                        split=split_name_task):
            parts.setdefault(i, []).append((knots, bey))
        named = []
        for i, cl in enumerate(unknown):
            names = set()
            for knots, bey in parts.get(i, []):
                note_beyond(bey, cl[0])
                names.update(x for x in knots.split(' / ') if x)
            if any('#' in x for x in names):  # 'non-hyperbolic' only says the same (timeouts)
                names.discard('non-hyperbolic')
            named.append((' / '.join(sorted(names)) or '? (crash)', None))
        dropped, crashes = list(pool.dropped), pool.crashes
    # representatives that crash SnapPy/spherogram by themselves: they were not examined
    with open(os.path.join(here, 'results', 'dropped_representatives%s.txt' % suffix), 'w') as f:
        f.write('# %d worker crashes; %d representatives crash SnapPy/spherogram by themselves and were '
                'skipped (top|bottom|gauss)\n' % (crashes, len(dropped)))
        for t in dropped:
            for r in t[1]:
                f.write('|'.join(r) + '\n')
    print('%d worker crashes, %d representatives skipped (see dropped_representatives%s.txt), '
          '%d representatives with a get_knotinfo timeout (%d s)' % (crashes, len(dropped), suffix,
                                                                     timeouts, LONG_TIMEOUT), flush=True)

    os.makedirs(os.path.join(here, 'results'), exist_ok=True)
    rows = []
    for nm, (c, h) in table.items():
        if c > max_c_out:
            continue
        if nm in index:
            status, lo, hi = 'identified', lower.get(nm), index[nm]
        elif nm in lower:
            status, lo, hi = 'HOMFLY appears, knot not yet identified', lower[nm], ''
        else:
            status, lo, hi = 'not found', max(nmax + 1, (c + 1) // 2 + 1), ''
        top, bottom, cr = example.get(nm, ('', '', ''))
        rows.append({'knot': nm, 'crossing_number': c, group + '_index': hi, 'lower_bound': lo,
                     'status': status, 'top_tree': top, 'bottom_tree': bottom, 'crossings_simplified': cr,
                     'homfly_vz': str(h)})

    def sort_key(r):
        c, rest = r['knot'].split('_', 1)
        alt = 0 if rest[0].isdigit() else (1 if rest[0] == 'a' else 2)
        num = int(re.sub(r'\D', '', rest))
        return (int(c.rstrip('an')), alt, num)

    rows.sort(key=sort_key)
    with open(os.path.join(here, 'results', group + '_index.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    with open(os.path.join(here, 'results', 'unidentified_classes%s.csv' % suffix), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['n_first', 'diagrams', 'min_crossings_after_RI_RII', 'knots', 'homfly_vz', 'top_tree',
                    'bottom_tree'])
        for (n, cnt, mc, h, reps), (knots, _) in zip(unknown, named):
            w.writerow([n, cnt, mc, knots, h, reps[0][0], reps[0][1]])

    with open(os.path.join(here, 'results', 'knots_beyond_table%s.csv' % suffix), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['knot', 'upper_bound_' + group + '_index', 'top_tree', 'bottom_tree'])
        for nm, (n, top, bottom) in sorted(beyond.items(), key=lambda kv: (kv[1][0], kv[0])):
            w.writerow([nm, n, top, bottom])

    lines = ['%s-index computed with tree diagrams up to n = %d' % (group, nmax),
             '%d worker crashes, %d representatives skipped because they crash SnapPy/spherogram, '
             '%d representatives with a get_knotinfo timeout (%d s)' % (crashes, len(dropped), timeouts,
                                                                       LONG_TIMEOUT), '']
    for c in range(3, max_c_out + 1):
        rc = [r for r in rows if r['crossing_number'] == c]
        if not rc:
            continue
        done = [r for r in rc if r['status'] == 'identified']
        lines.append('crossing number %2d: %4d / %4d knots with known %s-index' % (c, len(done), len(rc), group))
    lines.append('')
    for r in rows:
        if r['status'] == 'identified' and r['crossing_number'] <= 10:
            lines.append('%-8s %s-index %2d   T+ = %s   T- = %s' % (r['knot'], group, r[group + '_index'],
                                                                   r['top_tree'], r['bottom_tree']))
    open(os.path.join(here, 'results', group + '_index_summary.txt'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[:max_c_out + 2]))


if __name__ == '__main__':
    main(sys.argv[1:])
