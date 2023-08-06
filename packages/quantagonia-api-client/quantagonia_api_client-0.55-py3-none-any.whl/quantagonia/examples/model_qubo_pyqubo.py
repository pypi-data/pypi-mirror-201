import sys, os

import pyqubo as pq

from quantagonia.enums import HybridSolverServers
from quantagonia.qubo import *
from quantagonia.runner import Runner
from quantagonia.runner_factory import RunnerFactory
from quantagonia.spec_builder import QUBOSpecBuilder
from quantagonia.enums import HybridSolverConnectionType, HybridSolverServers, HybridSolverOptSenses

API_KEY = os.environ["QUANTAGONIA_API_KEY"]

def test_model_qubo_pyqubo():
  x0, x1, x2, x3, x4 = pq.Binary("x0"), pq.Binary("x1"), pq.Binary("x2"), \
                       pq.Binary("x3"), pq.Binary("x4")

  pyqubo_qubo = (2 * x0 + 2 * x2 + 2 * x4 - x0 * x2 - x2 * x0 - x0 * x4 - x4 * x0 - x2 * x4 - x4 * x2 + 3).compile()

  # setup model
  adap = PyQUBOAdapter()
  model = adap.convert(pyqubo_qubo)

  for s in ["x0", "x2", "x4"]:
    model.vars[s].assignment = 1

  print("Problem: ", model)
  print("Initial: ", model.eval())

  runner = RunnerFactory.getRunner(HybridSolverConnectionType.CLOUD,
    api_key=API_KEY, server = HybridSolverServers.PROD)
  specs = QUBOSpecBuilder()
  model.solve(specs.getd(), runner=runner)

  print("Optimized: ", model.eval())
  return model.eval()

if __name__ == '__main__':
  if test_model_qubo_pyqubo() != 3.0:
    raise Exception("Objective value is not correct")
