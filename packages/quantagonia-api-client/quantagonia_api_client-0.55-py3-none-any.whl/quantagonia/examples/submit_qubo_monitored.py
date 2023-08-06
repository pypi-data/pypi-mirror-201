import sys, os, os.path

from quantagonia.enums import *
from quantagonia.runner import Runner
from quantagonia.runner_factory import RunnerFactory
from quantagonia.spec_builder import QUBOSpecBuilder

input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "example_monitor.qubo")
api_key = os.environ["QUANTAGONIA_API_KEY"]

# set up a callback function that is called whenever a new incumbent solution is detected
def report_new_incumbent(batch_index, obj, solution):
  print("[CALLBACK] New primal solution discovered with objective", obj)

runner = RunnerFactory.getRunner(HybridSolverConnectionType.CLOUD,
                                 api_key=api_key,
                                 suppress_output=True)

spec = QUBOSpecBuilder()
spec.set_time_limit(60)

print("Submitting job with a time limit of 60 secs - the output is suppressed except for callbacks when a new incumbent is found...")
res_dict = runner.solve(input_file_path, spec.getd(), new_incumbent_callback=report_new_incumbent)

print("Finished, printing solver log for reference:")
print("==========")

print(res_dict["solver_log"])
