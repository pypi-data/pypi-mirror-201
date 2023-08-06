import os

from qiskit_optimization import *
from quantagonia.qubo import *

API_KEY = os.environ["QUANTAGONIA_API_KEY"]

###
# Same subset sum example as in the Ocean Adapter, just this time using Qiskit
###
def build_qiskit_qp():
  weights = [.9, .7, .2, .1]
  capacity = 1

  qp = QuadraticProgram()

  # create binary variables (y_j = 1 if bin j is used, x_i_j = 1 if item i 
  # is packed in bin j)
  for j in range(len(weights)):
    qp.binary_var(f'y_{j}')
  for i in range(len(weights)):
    for j in range(len(weights)):
      qp.binary_var(f'x_{i}_{j}')

  # minimize the number of used bins
  qp.minimize(linear={f'y_{j}': 1 for j in range(len(weights))})

  # ensure that each item is packed in exactly one bin
  for i in range(len(weights)):
    qp.linear_constraint(name=f'item_placing_{i}', linear={f'x_{i}_{j}': 1 for j in range(len(weights))}, sense='==', rhs=1)

  # ensure that the total weight of items in each bin does not exceed the capacity
  for j in range(len(weights)):
    lhs_x = {f'x_{i}_{j}': weights[i] for i in range(len(weights))}
    lhs_y = {f'y_{j}': -capacity}
    qp.linear_constraint(name=f'capacity_bin_{j}', linear={**lhs_x, **lhs_y}, sense='<=', rhs=0)

  return qp

if __name__ == "__main__":
  qp = build_qiskit_qp()

  print(qp.prettyprint())

  # convert to QUBO
  qubo_converter = QiskitQPAdapter(penalty = 1e2)
  qubo = qubo_converter.convert(qp)

  # solve QUBO with Quantagonia's (remote) solver
  runner = RunnerFactory.getRunner(HybridSolverConnectionType.CLOUD, api_key=API_KEY)
  spec = QUBOSpecBuilder()
  qubo.solve(specs=spec.getd(), runner=runner)

  # return solution in original CQM space
  obj = qubo.eval()
  sol = qubo_converter.getSolutionAsSample(qubo)

  print("Optimal solution vector:")
  for var in sol:
    print("\t", var, "\t", sol[var])

  # in order to use these as test
  if obj != 2.0:
    raise Exception("Objective value is not correct")