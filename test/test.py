"""
testing
"""
import sys
from pkg.pysat import solver

filename = sys.argv[1] if len(sys.argv) > 1 else 'test/test5.cnf'

solver.logger.setLevel('DEBUG')
s = solver.Solver(filename)
s.run()
assert s.compute_cnf() == 1