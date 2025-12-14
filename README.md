# GCP_SAT_SOLVER

A SAT solver implementation using CDCL (Conflict-Driven Clause Learning) algorithm with multiple branching heuristics, designed to solve the Graph Coloring Problem (GCP) and general SAT problems.

## 项目概述 (Project Overview)

This project implements a complete SAT solver that can solve satisfiability problems in CNF (Conjunctive Normal Form), with special support for graph k-coloring problems. The solver uses the CDCL algorithm with multiple variable selection heuristics to efficiently find solutions.

## 目录结构 (Directory Structure)

```
GCP_SAT_SOLVER/
├── pkg/                              # Main solver package
│   ├── main.py                       # Entry point for running the solver
│   ├── pysat/
│   │   ├── solver.py                 # Core CDCL SAT solver
│   │   └── branch_heuristics.py      # Multiple branching heuristics
│   └── utils/
│       ├── constants.py              # Constants (TRUE, FALSE, UNASSIGN)
│       ├── exceptions.py             # Custom exceptions
│       └── logger.py                 # Logging utilities
├── gcp/                              # Graph Coloring Problem utilities
│   ├── parse.py                      # Graph parsing and SAT formula generation
│   ├── test.py                       # GCP test cases
│   ├── cnf/                          # Sample CNF files for k-coloring
│   │   ├── sat_input_k4.txt
│   │   ├── sat_input_k5.txt
│   │   └── sat_input_k6.txt
│   └── colors/                       # Graph files in DIMACS format
│       └── le450_5a.col.txt
└── test/                             # Test suite
    ├── sample.cnf                    # Sample CNF files
    ├── test*.cnf
    ├── test.py                       # Main test file
    ├── heuristics_benchmark.py       # Benchmark for different heuristics
    ├── test_uf20-91.py               # SAT competitions test sets
    ├── test_uuf50-218.py
    └── uf*/                          # SAT competition benchmark instances
        ├── uf20-91/
        ├── uf50-218/
        ├── uf75-325/
        ├── uf100-430/
        └── uf150-645/
```

## 核心模块 (Core Modules)

### 1. **Solver** (`pkg/pysat/solver.py`)
The main CDCL SAT solver implementation.

**Key features:**
- Reads CNF formulas from DIMACS format files
- Implements unit propagation
- Performs conflict analysis and clause learning
- Supports multiple branching heuristics
- Provides detailed logging and statistics

**Main methods:**
- `run()`: Execute the solver and return result
- `solve()`: Core solving algorithm
- `propagate()`: Unit propagation
- `analyze_conflict()`: Conflict analysis

### 2. **Branching Heuristics** (`pkg/pysat/branch_heuristics.py`)
Multiple variable selection strategies for the CDCL solver:

- **OrderedChoiceSolver**: Selects variables in a fixed order
- **RandomChoiceSolver**: Randomly selects unassigned variables
- **FrequentVarsFirstSolver**: Prioritizes variables that appear most frequently in clauses (Default)
- **DynamicLargestIndividualSumSolver**: DLIS heuristic - selects based on positive and negative occurrences in unresolved clauses

### 3. **Graph Coloring Problem** (`gcp/parse.py`)
Utilities to convert graph k-coloring problems to SAT formulas:

**Functions:**
- `parse_graph(filename)`: Parse DIMACS graph format files
- `generate_kcoloring_sat_formula(n, m, E, k)`: Convert k-coloring problem to SAT clauses
- `export_dimacs(n, m, clauses, filename)`: Export clauses in DIMACS format

## 使用方法 (Usage)

### Basic Usage

Solve a SAT problem with default heuristic (FrequentVarsFirstSolver):
```bash
python -m pkg.main test/sample.cnf
```

### Specify Heuristic

Choose a different branching heuristic:
```bash
python -m pkg.main test/sample.cnf RandomChoiceSolver
python -m pkg.main test/sample.cnf OrderedChoiceSolver
python -m pkg.main test/sample.cnf DynamicLargestIndividualSumSolver
```

### Set Log Level

Control logging verbosity:
```bash
python -m pkg.main test/sample.cnf FrequentVarsFirstSolver --loglevel DEBUG
python -m pkg.main test/sample.cnf FrequentVarsFirstSolver --loglevel WARNING
```

### Programmatic Usage

```python
from pkg.pysat import branch_heuristics as solvers

# Create solver instance
solver = solvers.FrequentVarsFirstSolver('test/sample.cnf')

# Run the solver
sat, time_spent, answer = solver.run()

# Output result
print(answer)
```

### Graph Coloring Problem

```python
from gcp.parse import parse_graph, generate_kcoloring_sat_formula, export_dimacs

# Parse a graph
n, m, edges = parse_graph('gcp/colors/le450_5a.col.txt')

# Generate SAT formula for 5-coloring
num_vars, num_clauses, clauses = generate_kcoloring_sat_formula(n, m, edges, k=5)

# Export to DIMACS format
export_dimacs(num_vars, num_clauses, clauses, 'output.cnf')
```

## 输入格式 (Input Format)

The solver accepts CNF formulas in DIMACS format:

```
c This is a comment
p cnf <number_of_variables> <number_of_clauses>
<clause1> 0
<clause2> 0
...
```

Example:
```
c Sample CNF formula
p cnf 3 2
1 2 3 0
-1 -2 0
```

Each clause ends with 0, and variables are represented by positive/negative integers (1-indexed).

## 输出格式 (Output Format)

The solver outputs results in SAT competition format:
```
c ====================
c pysat reading from test/sample.cnf
c ====================
s SATISFIABLE
v 1 -2 3 0
c Done (time: 0.12 s, picked: 5 times)
```

Or for unsatisfiable formulas:
```
s UNSATISFIABLE
```

## 测试 (Testing)

Run tests:
```bash
python -m pytest test/
python test/test.py
```

Run benchmarks on SAT competition instances:
```bash
python test/test_uf20-91.py
python test/test_uuf50-218.py
python test/heuristics_benchmark.py
```

## 关键算法 (Key Algorithms)

### CDCL (Conflict-Driven Clause Learning)
1. **Decision**: Select an unassigned variable using a heuristic
2. **Propagation**: Apply unit propagation to derive new assignments
3. **Conflict Analysis**: When a conflict is found, analyze it to learn a new clause
4. **Backtrack**: Backtrack to an earlier decision level

### Unit Propagation
If a clause has all but one literal assigned to FALSE, the remaining literal must be TRUE.

### Conflict Analysis
When a conflict is detected:
1. Build an implication graph
2. Resolve clauses to find a reason for the conflict
3. Learn a new clause to prevent the same conflict

## 依赖 (Dependencies)

- Python 3.6+
- Standard library only (no external dependencies required)

Optional:
- pytest: For running tests

## 配置 (Configuration)

Logging can be configured via `pkg/utils/logger.py`. Default log levels:
- DEBUG: Detailed information
- INFO: General information
- WARNING: Warning messages only
- ERROR: Error messages only

## 性能 (Performance)

The solver is optimized for:
- Small to medium SAT instances (up to ~150 variables)
- Graph coloring problems with moderate graph sizes
- Educational purposes and algorithm comparison

Performance varies significantly based on:
- Problem hardness (2/3-SAT phase transition)
- Selected branching heuristic
- Instance structure and properties

## 许可证 (License)

This project is part of the GCP_SAT_SOLVER research project.

## 作者 (Authors)

Implementation of SAT solver with CDCL algorithm and multiple heuristics.

## 参考资源 (References)

- **CDCL Algorithm**: "A Fast and Scalable Algorithm for Detecting Community Structure in Networks"
- **SAT Solving**: Standard references on SAT solver implementations
- **Benchmarks**: SAT Competition benchmarks used in testing

---

**Last Updated**: December 2024
