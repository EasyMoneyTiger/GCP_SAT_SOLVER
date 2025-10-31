# parses graphs in DIMACS format
def parse_graph(filename):
    n = 0 #vertices
    m = 0 #edges
    E = []
    for line in open(filename, 'r').readlines():
        line = line.strip()
        if line.startswith('p'):
            line = line.split()
            n = int(line[2])
            m = int(line[3])
            continue    
        if line.startswith('e'):
            line = line.split()
            E += [(int(line[1])-1, int(line[2])-1)]
    return n, m, E
# reduction of k-coloring to SAT
def generate_kcoloring_sat_formula(n, m, E, k):
    clauses = []
    sat_vars = {}
    c = 1
    for i in range(n):
        for kdx in range(k):
            sat_vars[i, kdx] = c
            c += 1
    # at least one color for each vertex
    for i in range(n):
        clauses += [[sat_vars[i, kdx] for kdx in range(k)]] 
        # at most one color for each vertex
    for i in range(n):
        for r in range(k):
            for q in range(r+1, k):
                clauses += [[-sat_vars[i, q],-sat_vars[i, r]]]
    # connected nodes cannot have the same color
    for e in E:
        for kdx in range(k):
            clauses += [[-sat_vars[e[0], kdx],-sat_vars[e[1], kdx]]]
    return len(sat_vars.keys()), len(clauses), clauses

# translates clauses into DIMACS SAT format
def export_dimacs(n, m, clauses, filename='sat_input.txt'):
    f = open(filename, 'w+')
    print('p cnf {} {}'.format(n, m), file=f)
    for mdx in range(m):
        print(' '.join([str(var) for var in clauses[mdx] + [0]]), file=f)
    f.close()


filename = 'gcp/colors/le450_5a.col.txt' # k=5
#filename = 'queen8_8.col' # k=9
#filename = 'myciel6.col' # k=7
n, m, E = parse_graph(filename)
k = 5
sat_n, sat_m, sat_clauses = generate_kcoloring_sat_formula(n, m, E, k=k)
export_dimacs(sat_n, sat_m, sat_clauses, filename='gcp/cnf/sat_input_k{}.txt'.format(k))