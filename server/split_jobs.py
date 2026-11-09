"""
Splits a job file of descent_search.py between two machines (e.g. a laptop and a SLURM server). The jobs already
done (tmp_check/descent/done_<name>.txt) are left out.
usage (from F_index/): python3 server/split_jobs.py tmp_check/descent/jobs_<name>.json [fraction for the Mac, default 0.33]
-> tmp_check/descent/jobs_<name>_mac.json and jobs_<name>_server.json
"""
import json
import os
import sys

path = sys.argv[1]
frac = float(sys.argv[2]) if len(sys.argv) > 2 else 0.33
name = os.path.basename(path).split('.')[0]
done_file = os.path.join(os.path.dirname(path), 'done_%s.txt' % name)
done = set(open(done_file).read().split()) if os.path.exists(done_file) else set()
jobs = [j for j in json.load(open(path)) if j['name'] + ':' + j['knot'] not in done]
k = round(len(jobs) * frac)
for part, sub in (('mac', jobs[:k]), ('server', jobs[k:])):
    json.dump(sub, open(path.replace('.json', '_%s.json' % part), 'w'))
print('%d jobs to do (%d done): %d for the Mac, %d for the server' % (len(jobs), len(done), k, len(jobs) - k))
