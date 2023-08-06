import sys, os
import pulp
import math

from quantagonia.pulp.qpulp_adapter import QPuLPAdapter
from quantagonia.enums import HybridSolverConnectionType, HybridSolverServers
from quantagonia.spec_builder import MIPSpecBuilder

# retrieve API key from environment
API_KEY = os.getenv('QUANTAGONIA_API_KEY')

if __name__ == '__main__':

    ###
    # We model with vanilla PuLP code
    ###

    # define MIP problem
    prob = pulp.LpProblem("test", pulp.LpMaximize)
    x1 = pulp.LpVariable("x1", 0, None)
    x2 = pulp.LpVariable("x2", 0, None, pulp.LpInteger)
    x3 = pulp.LpVariable("x3", 0, None)
    prob += 2 * x1 + 4 * x2 + 3 * x3, "obj"
    prob += 3 * x1 + 4 * x2 + 2 * x3 <= 60, "c1"
    prob += 2 * x1 + 1 * x2 + 2 * x3 <= 40, "c2"
    prob += 1 * x1 + 3 * x2 + 2 * x3 <= 80, "c3"

    ###
    # Quantagonia-specific code
    ###
    spec = MIPSpecBuilder()
    spec.set_option("mip_heuristic_effort", 0.2)
    spec.set_option("mip_rel_gap", 5e-2)
    q_solver = QPuLPAdapter.getSolver(HybridSolverConnectionType.CLOUD,
                                      api_key=API_KEY,
                                      spec_dict=spec.getd(),
                                      keep_files=True)

    # solve
    prob.solve(solver=q_solver)

    # Each of the variables is printed with it's value
    for v in prob.variables():
        print(v.name, "=", v.varValue)

    # The optimised objective function value is printed to the screen
    print("Optimal value = ", pulp.value(prob.objective))

    # in order to use these as test
    if math.fabs(pulp.value(prob.objective) - 74) > 1e-4:
        raise Exception("Objective value is not correct")
