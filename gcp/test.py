from pkg.pysat import solver
from pkg.pysat import branch_heuristics as solvers
solver.logger.setLevel('DEBUG')

gcp1 = solvers.FrequentVarsFirstSolver('./gcp/cnf/sat_input_k5.txt')
gcp1.run()
assert gcp1.compute_cnf() == 1