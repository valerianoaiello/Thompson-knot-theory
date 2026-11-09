"""
The whole computation of one index, phase after phase, with timings and resumption.

usage (from F_index/):   python3 scripts/pipeline.py GROUP NMAX [--jobs 8] [--from PHASE] [--only PHASE] [--dry-run] [--force]

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
Long runs: start them with  caffeinate -i python3 scripts/pipeline.py ...  so that the Mac does not sleep.

Progress files.  Several phases resume from files in tmp_check/ (and run.py skips the n already in
results/raw*/). Those files are reused only when the same phase was interrupted (the phase recorded as
'started' and not 'done' in pipeline_<G>.json). In every other case (a new run, --from, --only, a phase
already completed) they come from an earlier run, possibly with older code, and are moved, never deleted, to
tmp_check/old_<G>_<date-time>/ before the phase starts: a resolve pass resumed from such a file once left
35 diagrams undecided that the current code excludes.
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repository root (the scripts are in scripts/)
SAGE = os.environ.get('SAGE', '/Applications/SageMath-10-8.app/Contents/Frameworks/Sage.framework/Versions/Current/venv/bin/sage')
PHASES = ['enumerate', 'identify', 'complete_check', 'resolve', 'apply', 'table', 'oriented', 'reverse_bound',
          'verify_oriented', 'certify', 'certify_retry', 'completeness']
RAW = {'F': 'raw', 'F3': 'raw_F3', 'Fvec': 'raw_Fvec', 'F3vec': 'raw_F3vec'}
# files a phase resumes from (relative to F_index/; {G} = group, {raw} = its raw directory)
PROGRESS = {
    'enumerate': ['results/{raw}/n*.tsv'],
    'complete_check': ['tmp_check/targets_{G}.tsv', 'tmp_check/keys_{G}.txt', 'tmp_check/{G}_n*',
                       'tmp_check/progress_{G}.jsonl'],
    'resolve': ['tmp_check/resolve_{G}.jsonl'],
    'oriented': ['tmp_check/oriented_{G}_c*.jsonl', 'tmp_check/oriented_{G}_c*_n*', 'tmp_check/keys_oriented_{G}_c*.txt'],
    'verify_oriented': ['tmp_check/verify_{G}.jsonl'],
    'certify': ['tmp_check/certify_{G}.jsonl'],
    'certify_retry': ['tmp_check/certify_retry_{G}.jsonl'],
}


def progress_files(group, phase):
    return sorted(f for pat in PROGRESS.get(phase, [])
                  for f in glob.glob(os.path.join(HERE, pat.format(G=group, raw=RAW[group]))))


def move_aside(group, phase, files, stamp):
    """Moves the progress files of an earlier run to tmp_check/old_<G>_<stamp>/, keeping their paths."""
    dest = os.path.join(HERE, 'tmp_check', 'old_%s_%s' % (group, stamp))
    for f in files:
        target = os.path.join(dest, os.path.relpath(f, HERE))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        os.rename(f, target)
    return dest


def commands(group, nmax, jobs):
    py, sp = [sys.executable], [SAGE, '-python']
    j = str(jobs)
    cmd = {
        'enumerate': py + ['scripts/run.py', str(nmax), '--group', group, '--jobs', j],
        'identify': [SAGE, 'scripts/identify.sage', '13', group, j],
        'complete_check': sp + ['scripts/complete_check.py', group, j],
        'resolve': sp + ['scripts/resolve_undecided.py', group, j],
        'apply': sp + ['scripts/apply_complete_check.py', group],
        'table': py + ['scripts/make_table.py', group],
        'oriented': sp + ['scripts/oriented_scan.py', group, j, '13'],
        'reverse_bound': py + ['scripts/reverse_bound_F3vec.py'],
        'verify_oriented': sp + ['scripts/verify_oriented.py', group, j],
        'certify': sp + ['scripts/certify_indices.py', group, j],
        'certify_retry': sp + ['scripts/certify_retry.py', group, j],
        'completeness': sp + ['scripts/certify_completeness.py', group],
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
    stamp = time.strftime('%Y%m%d-%H%M%S')
    for name, cmd in phases:
        say('%s: %s' % (name, ' '.join(cmd)))
        old = progress_files(a.group, name)
        resumed = state.get('started') == name and name not in state['done']
        if old and resumed:
            say('%s: resuming the interrupted phase from %d progress files' % (name, len(old)))
        elif old:
            if a.dry_run:
                say('%s: would move %d progress files of an earlier run aside' % (name, len(old)))
            else:
                say('%s: %d progress files of an earlier run moved to %s' % (
                    name, len(old), os.path.relpath(move_aside(a.group, name, old, stamp), HERE)))
        if a.dry_run:
            continue
        state['done'].pop(name, None)
        state['started'] = name
        json.dump(state, open(state_path, 'w'), indent=1)
        t0 = time.time()
        with open(os.path.join(logs, 'pipeline_%s_%s.out' % (a.group, name)), 'w') as out:
            rc = subprocess.call(cmd, cwd=HERE, env=env, stdout=out, stderr=subprocess.STDOUT)
        dt = time.time() - t0
        total += dt
        if rc != 0:
            say('%s FAILED (exit code %d) after %.0f s; see results/logs/pipeline_%s_%s.out' % (name, rc, dt, a.group, name))
            sys.exit(rc)
        state['done'][name] = round(dt, 1)
        state['started'] = None
        json.dump(state, open(state_path, 'w'), indent=1)
        say('%s done in %.0f s' % (name, dt))
    if not a.dry_run:
        say('timings (s): ' + ', '.join('%s %.0f' % kv for kv in state['done'].items()) + '; this run %.0f s' % total)


if __name__ == '__main__':
    main()
