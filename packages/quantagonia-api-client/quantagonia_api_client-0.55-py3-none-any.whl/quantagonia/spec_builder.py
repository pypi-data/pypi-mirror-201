import os
import json
from enum import Enum
from abc import ABC
from typing import Dict
import warnings
from .enums import PriorityEnum

# set up warnings
def plain_warning(message, category, filename, lineno, line=None):
    return '%s: %s\n' % (category.__name__, message)

warnings.formatwarning = plain_warning


THIS_SCRIPT = os.path.dirname(os.path.abspath(__file__))

class ProblemType(Enum):
    MIP = 0
    QUBO = 1

class QuboSolverType(Enum):
    """This class is deprecated and to be removed soon."""
    COOK = 0
    METROPOLIS_HASTINGS = 1
    FVSDP = 2
    THROW_DICE = 3
    THROW_DICE_SDP_ROOT = 4
    THROW_DICE_SDP_ALL = 5
    THROW_DICE_SDP_ALL_NEWTON = 6
    NO_SOLVER_SDP_ALL = 7


class SpecBuilder(ABC):
    def __init__(self):
        self.spec = {"solver_config" : {}}

    def gets(self) -> str:
        return json.dumps(self.spec)

    def getd(self) -> Dict:
        return self.spec

    def set_option(self, option: str, value) -> None:
        self.spec["solver_config"][option] = value

    def set_time_limit(self, time_limit: float):
        check_type("time_limit", time_limit, (float, int), type_name="numeric")
        check_numeric_value("time_limit", time_limit, lb=0)
        self.set_option("time_limit", time_limit)

    def set_priority(self, priority: PriorityEnum = PriorityEnum['MEDIUM']):
        try:
            self.spec["processing"]["priority"] = priority
        except KeyError as e:
            self.spec["processing"] = {}
            self.spec["processing"]["priority"] = priority

    def set_exclusivity(self, exclusive: bool = False):
        try:
            self.spec["processing"]["exclusive"] = exclusive
        except KeyError as e:
            self.spec["processing"] = {}
            self.spec["processing"]["exclusive"] = exclusive


class MIPSpecBuilder(SpecBuilder):
    def __init__(self):
        super().__init__()
        self.spec["problem_type"] = "MIP"

    def set_write_style(self, style: int) -> None:
        self.set_option("write_solution_style", style)

    def set_heuristics(self, heuristics: float):
        check_type("heuristics", heuristics, float)
        check_numeric_value("heuristics", heuristics, lb=0, ub=1)
        self.set_option("mip_heuristic_effort", heuristics)

class QUBOSpecBuilder(SpecBuilder):
    def __init__(self, type = None):
        super().__init__()
        self.spec["problem_type"] = "QUBO"

        if type:
            warnings.warn("Setting a specific QuboSolverType is deprecated and ignored. Instead, a default spec is loaded. Please do all modifications via the dedicated methods of the SpecBuilder.")

        # always read default spec
        with open(os.path.join(THIS_SCRIPT, "default_spec.json")) as jsonf:
            self.spec["solver_config"] = json.load(jsonf)

    # general settings
    ###################################################################################
    def set_sense(self, sense: str):
        warnings.warn("Setting the sense via the spec is deprecated and ignored! " +\
                      "Set the sense in the .qubo file or via QuboModel.sense().")

    # termination settings
    ###################################################################################
    def set_max_num_nodes(self, max_num_nodes: int):
        """Limit number of branch-and-bound nodes."""
        check_type("max_num_nodes", max_num_nodes, int)
        check_numeric_value("max_num_nodes", max_num_nodes, lb=1)
        self.set_option("max_num_nodes", max_num_nodes)

    def root_node_only(self):
        """Only solve the root node"""
        self.set_max_num_nodes(1)

    def set_absolute_gap(self, abs_gap: float):
        """
        Set the absolute gap for termination.
        If the current absolute gap falls below this value, the solver terminates.
        """
        check_type("absolute_gap", abs_gap, (float, int), type_name="numeric")
        self.set_option("absolute_gap", abs_gap)

    def set_relative_gap(self, rel_gap: float):
        """
        Set the relative gap for termination.
        If the current relative gap falls below this value, the solver terminates.
        """
        check_type("relative_gap", rel_gap, (float, int), type_name="numeric")
        self.set_option("relative_gap", rel_gap)

    def set_objective_cutoff(self, cutoff_value: float):
        """
        Set a cutoff value for the objective.
        If incumbent reaches cutoff value, the solver terminates
        """
        check_type("objective_cutoff", cutoff_value, (float, int), type_name="numeric")
        self.set_option("primal_cutoff_value", cutoff_value)

    # presolve settings
    ###################################################################################
    def set_presolve(self, presolve: bool):
        """
        Enable or disable presolve.
        """
        check_type("presolve", presolve, bool)
        self.spec["solver_config"]["presolve"]["enabled"] = presolve

    def set_node_presolve(self, node_presolve: bool):
        """
        Enable or disable node presolve.
        """
        check_type("node_presolve", node_presolve, bool)
        self.set_option("node_presolve", node_presolve)

    def set_decomposition(self, decomposition: True):
        """
        Enable or disable decomposition of the QUBO matrix.
        """
        check_type("decomposition", decomposition, bool)
        self.spec["solver_config"]["presolve"]["decompose"] = decomposition

    # search strategy settings
    ###################################################################################
    def set_enumeration(self, enumeration: bool):
        """
        Enable or disable enumeration.
        If subproblem size falls below threshold, it is enumerated out.
        """
        check_type("enumeration", enumeration, bool)
        self.spec["solver_config"]["enumerate"]["enabled"] = enumeration

    def add_quantum_heuristic(self, heuristic):
        if "root_node_quantum_heuristics" not in self.spec["solver_config"]:
            self.spec["solver_config"]["root_node_quantum_heuristics"] = []
        self.spec["solver_config"]["root_node_quantum_heuristics"].append(heuristic)
        
def check_type(option_name, option_value, type, type_name=None):
    if not isinstance(option_value, type):
        if type_name is None:
            type_name = type.__name
        raise ValueError(f"Value for {option_name} is set to {option_value} but must be a {type_name}.")

def check_numeric_value(option_name, option_value, lb=None, ub=None):
    if lb is not None and option_value < lb:
        raise ValueError(f"Value for {option_name} must be >= {lb}")
    if ub is not None and option_value > ub:
        raise ValueError(f"Value for {option_name} must be <= {ub}")
