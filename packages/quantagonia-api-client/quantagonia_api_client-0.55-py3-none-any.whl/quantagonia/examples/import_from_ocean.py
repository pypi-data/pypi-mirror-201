import os

import dimod
from quantagonia.qubo import *

API_KEY = os.environ["QUANTAGONIA_API_KEY"]

###
# Implements the small bin packing exmaple from
# https://docs.ocean.dwavesys.com/en/stable/docs_dimod/reference/models.html#dimod.ConstrainedQuadraticModel
###
def build_ocean_cqm():
  weights = [.9, .7, .2, .1]
  capacity = 1

  # create binary variables (y_j = 1 if bin j is used, x_i_j = 1 if item i 
  # is packed in bin j)
  y = [dimod.Binary(f'y_{j}') for j in range(len(weights))]
  x = [[dimod.Binary(f'x_{i}_{j}') for j in range(len(weights))] for i in range(len(weights))]

  # minimize the number of used bins
  cqm = dimod.ConstrainedQuadraticModel()
  cqm.set_objective(sum(y))

  # ensure that each item is packed in exactly one bin
  for i in range(len(weights)):
    cqm.add_constraint(sum(x[i]) == 1, label=f'item_placing_{i}')

  # ensure that the total weight of items in each bin does not exceed the capacity
  for j in range(len(weights)):
    cqm.add_constraint(sum(weights[i] * x[i][j] for i in range(len(weights))) - y[j] * capacity <= 0, label=f'capacity_bin_{j}')

  return cqm

if __name__ == "__main__":
  cqm = build_ocean_cqm()

  # convert to QUBO
  qubo_converter = DWaveCQMAdapter(penalty = 1e2)
  qubo = qubo_converter.convert(cqm)

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

  # evalute constraint violation
  viols = cqm.violations(sol, skip_satisfied=True)
  print("Constraint violations:", end="")
  if len(viols) == 0:
    print("\tNone")
  else:
    print(viols)

  # in order to use these as test
  if obj != 2.0:
    raise Exception("Objective value is not correct")