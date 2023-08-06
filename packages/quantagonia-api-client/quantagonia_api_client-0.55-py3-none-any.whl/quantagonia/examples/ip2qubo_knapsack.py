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
  prob = pulp.LpProblem("knapsack", pulp.LpMaximize)

  # 9-item problem
  x_0 = pulp.LpVariable("x_0", 0, 1, pulp.LpBinary)
  x_1 = pulp.LpVariable("x_1", 0, 1, pulp.LpBinary)
  x_2 = pulp.LpVariable("x_2", 0, 1, pulp.LpBinary)
  x_3 = pulp.LpVariable("x_3", 0, 1, pulp.LpBinary)
  x_4 = pulp.LpVariable("x_4", 0, 1, pulp.LpBinary)
  x_5 = pulp.LpVariable("x_5", 0, 1, pulp.LpBinary)
  x_6 = pulp.LpVariable("x_6", 0, 1, pulp.LpBinary)
  x_7 = pulp.LpVariable("x_7", 0, 1, pulp.LpBinary)
  x_8 = pulp.LpVariable("x_8", 0, 1, pulp.LpBinary)

  prob += 36 * x_0 + 43 * x_1 + 90 * x_2 + 45 * x_3 + 30 * x_4 + 56 * x_5 + 67 * x_6 + 95 * x_7 + 98 * x_8, "obj"
  prob += 38 * x_0 + 54 * x_1 + 36 * x_2 + 24 * x_3 + 40 * x_4 + 25 * x_5 + 37 * x_6 + 30 * x_7 + 59 * x_8 <= 150, "capacity"

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

  as_qubo = AutomaticPenaltyScalingIPviaQUBOSolver(True, 1.0,
    HybridSolverConnectionType.CLOUD, api_key=API_KEY, max_iters=100)
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
