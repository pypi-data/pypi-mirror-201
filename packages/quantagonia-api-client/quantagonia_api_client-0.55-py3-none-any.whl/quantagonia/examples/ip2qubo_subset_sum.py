import sys, os
import pulp

from quantagonia.qubo import *
from quantagonia.pulp.qpulp_adapter import QPuLPAdapter
from quantagonia.enums import HybridSolverConnectionType, HybridSolverServers

API_KEY = os.environ["QUANTAGONIA_API_KEY"]

if __name__ == '__main__':

  q_solver = QPuLPAdapter.getSolver(HybridSolverConnectionType.CLOUD,
    api_key=API_KEY)

  # create subset sum problem
  prob = pulp.LpProblem("subset_sum", pulp.LpMinimize)

  # 6-variable problem
  v3 = pulp.LpVariable("v3", 0, 1, pulp.LpBinary)
  v34 = pulp.LpVariable("v34", 0, 1, pulp.LpBinary)
  v4 = pulp.LpVariable("v4", 0, 1, pulp.LpBinary)
  v12 = pulp.LpVariable("v12", 0, 1, pulp.LpBinary)
  v5 = pulp.LpVariable("v5", 0, 1, pulp.LpBinary)
  v2 = pulp.LpVariable("v2", 0, 1, pulp.LpBinary)

  prob += v3 + v34 + v4 + v12 + v5 + v2, "obj"
  prob += 3 * v3 + 34 * v34 + 4 * v4 + 12 * v12 + 5 * v5 + 2 * v2 == 21, "subset"

  ###
  # Solve as MIP
  ###

  print("\nSOLVE MIP ========================================\n")

  prob.solve(solver=q_solver)

  # Each of the variables is printed with it's value
  print("Optimal solution from MIP solver:")
  for v in prob.variables():
      print("\t", v.name, "=", v.varValue)

  # The optimised objective function value is printed to the screen
  mip_obj = pulp.value(prob.objective)
  print("Optimal value from MIP solver = ", mip_obj)

  ###
  # Convert to QUBO
  ###

  print("\nSOLVE AS QUBO ====================================\n")

  as_qubo = OneShotIPviaQUBOSolver(True, 1.0, HybridSolverConnectionType.CLOUD,
    api_key=API_KEY)
  prob = as_qubo.solveIP(prob)

  # Each of the variables is printed with it's value
  print("Optimal solution from QUBO solver:")
  for v in prob.variables():
      print("\t", v.name, "=", v.varValue)

  # The optimised objective function value is printed to the screen
  qubo_obj = pulp.value(prob.objective)
  print("Optimal value from QUBO solver = ", qubo_obj)

  print("\nCHECK ============================================\n")

  if mip_obj == qubo_obj:
    print("MIP and QUBO objectives match!")
  else:
    raise Exception("IP and QUBO delivered different optimal values...")
