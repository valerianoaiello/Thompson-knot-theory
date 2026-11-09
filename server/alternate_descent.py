"""
Alternating descent in vec{F} (or vec{F}_3) for one knot: greedy_descent.py until it stops, then one level of the
exhaustive local search of descent_search.py (extra = 1, then extra = 2 if nothing is found and n <= 29) from the last
diagram, then greedy_descent.py again from the diagram found, and so on, down to N_MIN or until both fail.
The starting diagram is tmp_check/alexander/KNOT.json (alexander.py, run first if missing); the progress is in
tmp_check/alexander/KNOT_greedy.jsonl (one line per level, resumable).

usage (from F_index/): python server/alternate_descent.py KNOT [processes] [n_min] [--group Fvec|F3vec] [--seed S]
With --seed S (default 50) other than 50 the construction starts from other special diagrams and its files are
tmp_check/alexander/KNOT_sS.json, KNOT_sS_greedy.jsonl (the earlier ones are kept).
"""
import csv
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.environ.get('PY', sys.executable).split()


def last_level(k, group):
    path = os.path.join(HERE, 'tmp_check', 'alexander', '%s_greedy.jsonl' % k)  # k = file stem
    steps = [json.loads(x) for x in open(path) if x.strip()] if os.path.exists(path) else []
    if steps:
        return steps[-1]['n'], steps[-1]['diagram']
    s = json.load(open(os.path.join(HERE, 'tmp_check', 'alexander', '%s.json' % k)))
    top = s[group].split('|')[0]
    n = len(top.split(',')) if group == 'Fvec' else (len(top.split(',')) + 1) // 2
    return n, s[group]


def run(cmd, log, env=None):
    with open(log, 'a') as f:
        subprocess.run(cmd, cwd=HERE, stdout=f, stderr=subprocess.STDOUT, env=env)


def main():
    args = sys.argv[1:]
    k = args[0]
    procs = args[1] if len(args) > 1 and not args[1].startswith('--') else '3'
    n_min = int(args[2]) if len(args) > 2 and not args[2].startswith('--') else 19
    group = args[args.index('--group') + 1] if '--group' in args else 'Fvec'
    seed = args[args.index('--seed') + 1] if '--seed' in args else '50'
    knot, k = k, (k if seed == '50' else '%s_s%s' % (k, seed))  # k: stem of the files
    alex = os.path.join(HERE, 'tmp_check', 'alexander')
    desc = os.path.join(HERE, 'tmp_check', 'descent')
    os.makedirs(alex, exist_ok=True)
    os.makedirs(desc, exist_ok=True)
    if not os.path.exists(os.path.join(alex, '%s.json' % k)):
        run(PY + ['scripts/alexander.py', knot, '--seed', seed, '--minutes', '3', '--tries', '4', '--out', k],
            os.path.join(HERE, 'tmp_check', 'alexander_%s.log' % k))
    if not os.path.exists(os.path.join(alex, '%s.json' % k)):
        print(k, 'no construction', flush=True)
        return
    while True:
        run(PY + ['scripts/greedy_descent.py', os.path.join('tmp_check', 'alexander', '%s.json' % k), procs, '--group', group,
                  '--n-min', str(n_min)], os.path.join(alex, '%s_greedy.log' % k))
        n, d = last_level(k, group)
        print(k, 'greedy at', n, flush=True)
        if n <= n_min:
            print(k, 'FOUND n =', n, flush=True)
            return
        found = None
        for extra in ((1, 2) if n <= 29 else (1,)):  # extra = 2 is too heavy on large diagrams
            name = 'alt_%s_n%d_e%d' % (k, n, extra)  # unique per level: a rerun reuses the results
            jobs = os.path.join(desc, 'jobs_%s.json' % name)
            out = os.path.join(desc, 'out_%s.csv' % name)
            json.dump([dict(name=name, group=group, knot=knot, starts=[d], steps=1, extra=extra)], open(jobs, 'w'))
            env = dict(os.environ, DESCENT_OUT=out)
            run(PY + ['scripts/descent_search.py', jobs, procs], os.path.join(desc, '%s.log' % name), env)
            hits = [r for r in csv.DictReader(open(out))] if os.path.exists(out) else []
            print(k, 'exhaustive from', n, 'extra', extra, ':', len(hits), 'diagrams', flush=True)
            if hits:
                found = hits[0]
                break
        if not found:
            print(k, 'stopped at n =', n, flush=True)
            return
        with open(os.path.join(alex, '%s_greedy.jsonl' % k), 'a') as f:
            f.write(json.dumps({'n': int(found['n']), 'diagram': found['diagram']}) + '\n')


if __name__ == '__main__':
    main()
