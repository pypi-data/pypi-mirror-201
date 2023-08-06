import sys, os, os.path

from quantagonia.enums import *
from quantagonia.runner import Runner
from quantagonia.runner_factory import RunnerFactory
from quantagonia.spec_builder import MIPSpecBuilder, QUBOSpecBuilder

mip_path0 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "example.mps")
mip_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "garbage.mps")
qubo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "example.qubo")
api_key = os.environ["QUANTAGONIA_API_KEY"]

runner = RunnerFactory.getRunner(HybridSolverConnectionType.CLOUD,
                                 api_key=api_key,
                                 server = HybridSolverServers.PROD,
                                 suppress_output=True)
mip_spec = MIPSpecBuilder()
qubo_spec = QUBOSpecBuilder()

problems = [mip_path0, mip_path1, qubo_path]
specs = [mip_spec.getd(), mip_spec.getd(), qubo_spec.getd()]
res = runner.solveBatched(problems, specs)

batch_size = len(problems)

for ix in range(batch_size):
    print(f"=== PROBLEM {ix}: status {res[ix]['status']} ===")
    print(res[ix]["solver_log"])
