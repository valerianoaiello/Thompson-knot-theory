"""
Builds the job files of descent_search.py for the open cases of the tables (tmp_check/descent/jobs_<name>.json):
  F3       knots not found in F_3 (n <= 9) with <= 12 crossings: start from their vec{F}_3 witness (vec{F}_3 is in
           F_3), one step down;
  F        knots not found in F (n <= 13) with <= 11 crossings: start from their vec{F} witness, down to n = 14;
  F3vec    knots not found in vec{F}_3 (n <= 11) with <= 12 crossings and a vec{F} witness: start from iota of it,
           down to n = 13;
  rev3     the knots of results/reverse_bound_F3vec.csv with '13-15': start from the move with four new vertices
           (n = 15, it realizes the other orientation), one step down, looking for the other orientation;
  rev      the same in vec{F} (results/reverse_bound_Fvec.csv, '19-21'): from n = 21 to n = 19.
Every starting diagram built by a move is checked with SnapPy before it is used.
usage (from F_index/): sage -python descent_jobs.py
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
csv.field_size_limit(10**9)

REVERSE = {'K': ['reverse', 'mirror'], 'Kr': ['same', 'mirror reverse']}  # the other orientation (inverse rule)


def last_leaf(ws, sub):
    """Leaf words with the last leaf replaced by the subtree with leaf words `sub`."""
    last = max(ws)
    return [w for w in ws if w != last] + [last + s for s in sub]


def move4_ternary(top, bottom):
    t, b = top.split(','), bottom.split(',')
    tp = ['00', '01'] + ['02' + w for w in last_leaf(t, '012')] + ['1', '20', '21', '22']
    tm = ['0', '1'] + ['2' + w for w in last_leaf(b, ['00', '01', '020', '021', '022', '1', '2'])]
    return ','.join(sorted(tp)), ','.join(sorted(tm))


def move4_binary(top, bottom):
    t, b = top.split(','), bottom.split(',')
    tp = ['00'] + ['01' + w for w in last_leaf(t, '01')] + ['10', '11']
    tm = ['0'] + ['1' + w for w in last_leaf(b, ['00', '010', '011', '1'])]
    return ','.join(sorted(tp)), ','.join(sorted(tm))


def main():
    from sage.all import KnotInfo
    import ftrees as F
    import oriented as O
    T = {G: {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', '%s_index.csv' % G)))}
         for G in ('F', 'F3', 'Fvec', 'F3vec')}
    d = os.path.join(HERE, 'tmp_check', 'descent')
    os.makedirs(d, exist_ok=True)

    def witness(G, k):
        return T[G][k]['top_tree'] + ' | ' + T[G][k]['bottom_tree']

    def open_cases(G, maxc):
        return [k for k, r in T[G].items() if not r[G + '_index'] and int(r['crossing_number']) <= maxc]

    def ref(k):
        return [list(map(int, c)) for c in getattr(KnotInfo, 'K' + k).link().pd_code()]

    jobs = {'F3': [], 'F': [], 'F3vec': [], 'rev3': [], 'rev': []}
    for k in open_cases('F3', 12):
        if T['F3vec'][k]['F3vec_index']:
            jobs['F3'].append({'name': 'F3', 'group': 'F3', 'knot': k, 'starts': [witness('F3vec', k)], 'steps': 1})
    for k in open_cases('F', 11):
        if T['Fvec'][k]['Fvec_index']:
            n = int(T['Fvec'][k]['Fvec_index'])
            jobs['F'].append({'name': 'F', 'group': 'F', 'knot': k, 'starts': [witness('Fvec', k)], 'steps': n - 14})
    for k in open_cases('F3vec', 12):
        if T['Fvec'][k]['Fvec_index']:
            n = int(T['Fvec'][k]['Fvec_index'])
            t, b = [F.from_leaf_words(x.strip().split(',')) for x in witness('Fvec', k).split('|')]
            start = ','.join(O.ternary_words(O.iota(t))) + ' | ' + ','.join(O.ternary_words(O.iota(b)))
            jobs['F3vec'].append({'name': 'F3vec', 'group': 'F3vec', 'knot': k, 'starts': [start],
                                  'steps': (n - 13) // 2})
    ori = {G: {r['knot']: r for r in csv.DictReader(open(os.path.join(HERE, 'results', 'oriented_index_%s.csv' % G)))}
           for G in ('Fvec', 'F3vec')}
    for G, name, move, tree, pd in (('F3vec', 'rev3', move4_ternary, O.ternary_from_words, O.oriented_pd_code3),
                                    ('Fvec', 'rev', move4_binary, F.from_leaf_words, O.oriented_pd_code)):
        for r in csv.DictReader(open(os.path.join(HERE, 'results', 'reverse_bound_%s.csv' % G))):
            if '-' not in r['index_other']:
                continue
            k, want = r['knot'], r['realized']
            t, b = [x.strip() for x in ori[G][k]['witness_' + want].split('|')]
            mt, mb = move(t, b)
            rel = O.relation_to(pd(tree(mt.split(',')), tree(mb.split(','))), ref(k))
            if not rel & set(REVERSE[want]):
                print('move check FAILED', G, k, want, sorted(rel))
                continue
            jobs[name].append({'name': name, 'group': G, 'knot': k, 'starts': [mt + ' | ' + mb], 'steps': 1,
                               'want': REVERSE[want]})
    for name, js in jobs.items():
        json.dump(js, open(os.path.join(d, 'jobs_%s.json' % name), 'w'), indent=1)
        print(name, len(js), 'jobs')


if __name__ == '__main__':
    main()
