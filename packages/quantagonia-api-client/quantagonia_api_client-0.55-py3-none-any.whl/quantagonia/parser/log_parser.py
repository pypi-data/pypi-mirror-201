"""
Class to parse solver log.
"""

import re
import numpy as np


def get_regex_result(regex_string: str, search_string: str, group_name: str = None):
    m = re.compile(regex_string).search(search_string)
    if m is not None:
        return m.group(group_name) if group_name is not None else m.group()
    return None


class SolverLogParser:
    """Class for parsing the solver log."""

    def __init__(self, log: str):
        self.log = log

    def get_sol_status(self) -> str:
        """ """
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\sSolution\sStatus:(?P<solution_status>.*)"
        sol_status = str(get_regex_result(regex, self.log, "solution_status")).strip()
        return sol_status

    def get_timing(self) -> float:
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\sWall\sTime:(?P<wall_time>.*) seconds"
        timing = str(get_regex_result(regex, self.log, "wall_time")).strip()
        if (timing is None) or (timing == "None"):
            return np.nan
        return float(timing)

    def get_objective(self) -> float:
        """ """
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\sObjective:(?P<objective>.*)"
        objective = str(get_regex_result(regex, self.log, "objective")).strip()
        if (objective is None) or (objective == "None"):
            return np.nan
        return float(objective)

    def get_bound(self) -> float:
        """ """
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\sBound:(?P<bound>.*)"
        bound = str(get_regex_result(regex, self.log, "bound")).strip()
        if (bound is None) or (bound == "None"):
            return np.nan
        return float(bound)

    def get_absolute_gap(self):
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\sAbsolute\sGap:(?P<absolute_gap>.*)"
        absolute_gap = str(get_regex_result(regex, self.log, "absolute_gap")).strip()
        absolute_gap = absolute_gap.split()[0]
        if (absolute_gap is None) or (absolute_gap == "None"):
            return np.nan
        return float(absolute_gap)

    def get_relative_gap(self):
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\sRelative\sGap:(?P<relative_gap>[^%|^\n]*)"

        relative_gap = str(get_regex_result(regex, self.log, "relative_gap")).strip()
        if (relative_gap is None) or (relative_gap == "None"):
            return np.nan
        return float(relative_gap)

    def get_nodes(self) -> int:
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\sNodes:(?P<nodes>.*)"
        nodes = str(get_regex_result(regex, self.log, "nodes")).strip()
        if (nodes is None) or (nodes == "None"):
            return np.nan
        return int(nodes)

    def get_iterations(self) -> int:
        """Get LP iterations."""
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\s(LP|Simplex|IPM)\sIterations:(?P<iterations>.*)"
        iterations = str(get_regex_result(regex, self.log, "iterations")).strip()
        if (iterations is None) or (iterations == "None"):
            return np.nan
        return int(iterations)

    def get_nodes_per_sec(self) -> float:
        """Get nodes per second."""
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\sNodes\s/\ss:(?P<nodes_per_sec>.*)"
        nodes_per_sec = str(get_regex_result(regex, self.log, "nodes_per_sec")).strip()
        if (nodes_per_sec is None) or (nodes_per_sec == "None"):
            return np.nan
        return float(nodes_per_sec)

    def get_best_node(self) -> str:
        """Get the node count of the best solution."""
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\sBest\ssolution\sfound\sat\snode (?P<best_node>.*) after (?P<best_time>.*) seconds"
        best_node = str(get_regex_result(regex, self.log, "best_node")).strip()
        if (best_node is None) or (best_node == "None"):
            return np.nan
        return int(best_node)

    def get_best_time(self) -> str:
        """Get the node count of the best solution."""
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\sBest\ssolution\sfound\sat\snode (?P<best_node>.*) after (?P<best_time>.*) seconds"
        best_time = str(get_regex_result(regex, self.log, "best_time")).strip()
        if (best_time is None) or (best_time == "None"):
            return np.nan
        return float(best_time)

    def get_nodes_over_time(self) -> list:
        """Get the number of open and closed nodes over time."""
        nodes_over_time = []
        log = self.log.split("\n")
        in_table = False
        for l in log:
            l = [s.strip() for s in l.split("|")]
            if l[0] == "Nodes":
                in_table = True
            if in_table and l[0] == "":
                break
            elif in_table and l[0] != "Nodes" and not "-------" in l[0]:
                time = float(l[-3])
                processed_nodes = float(l[0].split()[-1]) # if new incumbent is found then first column is of the form 'R   123' -> split and take last entry
                open_nodes = float(l[1])
                nodes_over_time.append((time, processed_nodes, open_nodes))

        return nodes_over_time

    def get_solving_mix(self) -> list:
        """Get list of used solvers."""
        regex = r"(?<=(Running\ssolver\smix:))[\s]*(?P<solving_mix>.*);"
        solving_mix = [s.strip() for s in str(get_regex_result(regex, self.log, "solving_mix")).split(',')]
        return solving_mix

    def get_number_of_quantum_solutions(self) -> int:
        """Get the number of quantum solutions."""
        regex = r"(?<=(Solver\sResults))[\s\S]*\s-\sNumber\sof\sgenerated\squantum\ssolutions:\s(?P<sols>.*)"
        solutions = str(get_regex_result(regex, self.log, "sols")).strip()
        if (solutions is None) or (solutions == "None"):
            return np.nan
        return int(solutions)

    def get_all(self):
        rdata = {}
        rdata["sol_status"] = self.get_sol_status()
        rdata["timing"] = self.get_timing()
        rdata["objective"] = self.get_objective()
        rdata["bound"] = self.get_bound()
        rdata["absolute_gap"] = self.get_absolute_gap()
        rdata["relative_gap"] = self.get_relative_gap()
        rdata["iterations"] = self.get_iterations()
        rdata["nodes"] = self.get_nodes()
        rdata["nodes_per_sec"] = self.get_nodes_per_sec()
        rdata["best_node"] = self.get_best_node()
        rdata["best_time"] = self.get_best_time()
        rdata["num_quantum_solutions"] = self.get_number_of_quantum_solutions()
        rdata["solver_mix"] = self.get_solving_mix()

        return rdata
