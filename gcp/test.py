from pkg.pysat import solver
solver.logger.setLevel('DEBUG')

gcp1 = solver.Solver('./gcp/cnf/sat_input_k5.txt')
gcp1.run()
assert gcp1.compute_cnf() == 1