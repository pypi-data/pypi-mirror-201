import os, sys
import asyncio
import time

import pyqubo as pq
from quantagonia.cloud.cloud_runner import CloudRunner

from quantagonia.enums import HybridSolverServers, HybridSolverConnectionType
from quantagonia.qubo import *
from quantagonia.runner import Runner
from quantagonia.runner_factory import RunnerFactory
from quantagonia.spec_builder import QUBOSpecBuilder

API_KEY = os.environ["QUANTAGONIA_API_KEY"]

def build_sample_qubo(penalty : float = 1):
  x0, x1, x2, x3, x4 = pq.Binary("x0"), pq.Binary("x1"), pq.Binary("x2"), \
                       pq.Binary("x3"), pq.Binary("x4")

  alpha = 1
  pyqubo_cons = alpha * (x0 - x2) ** 2
  pyqubo_mdl = x0 + x2 + x4 - 1 * x0 * x2 - 1 * x0 * x4 - 1 * x2 * x4 + pyqubo_cons
  pyqubo_qubo = pyqubo_mdl.compile()

  adap = PyQUBOAdapter()
  qbo = adap.convert(pyqubo_qubo, {'alpha' : penalty})

  return qbo

async def mainAsync(num_problems : int):

  # create a solver
  runner = RunnerFactory.getRunner(HybridSolverConnectionType.CLOUD, api_key=API_KEY,
    server=HybridSolverServers.PROD, suppress_output=True)

  # create a bunch of problems with different penalties
  print("\tCreating example problems...")
  probs = []
  for ix in range(0, num_problems):
    probs.append(build_sample_qubo(penalty=float(2**ix)))

  print("\tSubmitting jobs...")
  tasks = []
  for ix in range(0, num_problems):
    print("\t\tSubmitting job #" + str(ix) + "...")
    specs = QUBOSpecBuilder()
    tasks.append(asyncio.create_task(probs[ix].solveAsync(specs.getd(), runner=runner)))

  print("\tWaiting for job completion...")
  for ix in range(0, num_problems):
    await tasks[ix]

  print("\tResults:")
  for ix in range(0, num_problems):
    print("\t\t" + str(ix) + ": " +  str(probs[ix].eval()))

  print("\tAll done!")

def main(num_problems : int):

  # create a solver
  runner = RunnerFactory.getRunner(HybridSolverConnectionType.CLOUD, api_key=API_KEY,
    server=HybridSolverServers.PROD, suppress_output=True)

  # create a bunch of problems with different penalties
  print("\tCreating example problems...")
  probs = []
  for ix in range(0, num_problems):
    probs.append(build_sample_qubo(penalty=float(2**ix)))

  print("\tSolving problems....")
  for ix in range(0, num_problems):

    specs = QUBOSpecBuilder()
    print("\t\tSubmitting job #" + str(ix) + " and waiting for results...")
    probs[ix].solve(specs.getd(), runner=runner)
    print("\t\tProcessed job #" + str(ix))

  print("\tResults:")
  for ix in range(0, num_problems):
    print("\t\t" + str(ix) + ": " + str(probs[ix].eval()))

  print("\tAll done!")


if __name__ == "__main__":

  num_problems = 3

  print("-- Blocking execution")
  start = time.time()
  main(num_problems)
  stop = time.time()

  print("Blocking Runtime: " + str(stop - start) + " secs.")

  print("-- Non-Blocking execution")
  start = time.time()
  asyncio.run(mainAsync(num_problems))
  stop = time.time()

  print("Non-blocking Runtime: " + str(stop - start) + " secs.")
