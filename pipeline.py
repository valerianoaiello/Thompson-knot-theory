"""
The whole computation of one index, phase after phase, with timings and resumption.

usage (from F_index/):   python3 pipeline.py GROUP NMAX [--jobs 8] [--from PHASE] [--only PHASE] [--dry-run] [--force]

GROUP = F, F3, Fvec or F3vec. Phases, in this order (the oriented ones only for Fvec and F3vec):
  enumerate       run.py NMAX --group GROUP                       -> results/raw_<G>/n<n>.tsv
  identify        identify.sage 13 GROUP                          -> results/<G>_index.csv
  complete_check  complete_check.py GROUP                         -> results/complete_check_<G>.csv
  resolve         resolve_undecided.py GROUP                      (second pass on undecided diagrams)
  apply           apply_complete_check.py GROUP                   (updates results/<G>_index.csv)
  table           make_table.py GROUP                             -> results/<G>_index_table.md
  oriented        oriented_scan.py GROUP 13                       -> results/oriented_index_<G>.csv
  reverse_bound   reverse_bound_F3vec.py (F3vec only)             -> results/reverse_bound_F3vec.csv
  verify_oriented verify_oriented.py GROUP                        -> results/oriented_verified_<G>.md
  certify         certify_indices.py GROUP                        -> results/certified_<G>.md
  certify_retry   certify_retry.py GROUP                          -> results/certified_retry_<G>.md
  completeness    certify_completeness.py GROUP                   -> results/certified_completeness_<G>.md
(reverse_bound.py for Fvec reads the all-diagram files of n = 17 and is not part of the pipeline.)

Every phase is timed; the log is results/logs/pipeline_<G>.log, and results/logs/pipeline_<G>.json records the
phases already completed, so that a second run resumes after the last completed phase (--from restarts from a
given phase). The scripts overwrite results/: to keep the existing results, run the pipeline in a separate
checkout, e.g.  git worktree add ../F_index_rerun  (then `make` there). Without --force the pipeline refuses to
start when results/<G>_index.csv already exists and no phase has been recorded.
Long runs: start them with  caffeinate -i python3 pipeline.py ...  so that the Mac does not sleep.
"""
import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SAGE = os.environ.get('SAGE', '/Applications/SageMath-10-8.app/Contents/Frameworks/Sage.framework/Versions/Current/venv/bin/sage')
PHASES = ['enumerate', 'identify', 'complete_check', 'resolve', 'apply', 'table', 'oriented', 'reverse_bound',
          'verify_oriented', 'certify', 'certify_retry', 'completeness']


def commands(group, nmax, jobs):
    py, sp = [sys.executable], [SAGE, '-python']
    j = str(jobs)
    cmd = {
        'enumerate': py + ['run.py', str(nmax), '--group', group, '--jobs', j],
        'identify': [SAGE, 'identify.sage', '13', group, j],
        'complete_check': sp + ['complete_check.py', group, j],
        'resolve': sp + ['resolve_undecided.py', group, j],
        'apply': sp + ['apply_complete_check.py', group],
        'table': py + ['make_table.py', group],
        'oriented': sp + ['oriented_scan.py', group, j, '13'],
        'reverse_bound': py + ['reverse_bound_F3vec.py'],
        'verify_oriented': sp + ['verify_oriented.py', group, j],
        'certify': sp + ['certify_indices.py', group, j],
        'certify_retry': sp + ['certify_retry.py', group, j],
        'completeness': sp + ['certify_completeness.py', group],
    }
    skip = set()
    if group not in ('Fvec', 'F3vec'):
        skip |= {'oriented', 'reverse_bound', 'verify_oriented'}
    if group != 'F3vec':
        skip.add('reverse_bound')
    return [(p, cmd[p]) for p in PHASES if p not in skip]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('group', choices=['F', 'F3', 'Fvec', 'F3vec'])
    ap.add_argument('nmax', type=int)
    ap.add_argument('--jobs', type=int, default=os.cpu_count())
    ap.add_argument('--from', dest='start', choices=PHASES)
    ap.add_argument('--only', choices=PHASES)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()

    logs = os.path.join(HERE, 'results', 'logs')
    os.makedirs(logs, exist_ok=True)
    state_path = os.path.join(logs, 'pipeline_%s.json' % a.group)
    state = json.load(open(state_path)) if os.path.exists(state_path) else {'nmax': a.nmax, 'done': {}}
    if state.get('nmax') != a.nmax:
        state = {'nmax': a.nmax, 'done': {}}
    if (not state['done'] and not a.force and not a.dry_run
            and os.path.exists(os.path.join(HERE, 'results', '%s_index.csv' % a.group))):
        sys.exit('results/%s_index.csv exists and would be overwritten: run the pipeline in a separate checkout '
                 '(git worktree add ../F_index_rerun), or use --force' % a.group)

    phases = commands(a.group, a.nmax, a.jobs)
    names = [p for p, _ in phases]
    if a.only:
        phases = [x for x in phases if x[0] == a.only]
    elif a.start:
        phases = phases[names.index(a.start):] if a.start in names else []
        for p in names[names.index(a.start):] if a.start in names else []:
            state['done'].pop(p, None)
    else:
        phases = [x for x in phases if x[0] not in state['done']]

    env = dict(os.environ)
    if a.group == 'F3vec' and a.nmax >= 11:
        env.setdefault('NAME_REPS', '0')  # 700k HOMFLY classes outside KnotInfo at n = 11: do not name them
    log = open(os.path.join(logs, 'pipeline_%s.log' % a.group), 'a')

    def say(msg):
        line = '%s  %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)
        print(line, flush=True)
        log.write(line + '\n')
        log.flush()

    say('pipeline %s, n <= %d, %d processes: %s' % (a.group, a.nmax, a.jobs, ', '.join(p for p, _ in phases) or 'nothing to do'))
    total = 0.0
    for name, cmd in phases:
        say('%s: %s' % (name, ' '.join(cmd)))
        if a.dry_run:
            continue
        t0 = time.time()
        with open(os.path.join(logs, 'pipeline_%s_%s.out' % (a.group, name)), 'w') as out:
            rc = subprocess.call(cmd, cwd=HERE, env=env, stdout=out, stderr=subprocess.STDOUT)
        dt = time.time() - t0
        total += dt
        if rc != 0:
            say('%s FAILED (exit code %d) after %.0f s; see results/logs/pipeline_%s_%s.out' % (name, rc, dt, a.group, name))
            sys.exit(rc)
        state['done'][name] = round(dt, 1)
        json.dump(state, open(state_path, 'w'), indent=1)
        say('%s done in %.0f s' % (name, dt))
    if not a.dry_run:
        say('timings (s): ' + ', '.join('%s %.0f' % kv for kv in state['done'].items()) + '; this run %.0f s' % total)


if __name__ == '__main__':
    main()
