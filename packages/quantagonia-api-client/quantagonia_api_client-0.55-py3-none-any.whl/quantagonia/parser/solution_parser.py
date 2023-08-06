"""
Class to parse solution from file.
"""

class SolutionParser:

    def __init__(self):
        """Constructor."""
        pass

    @staticmethod
    def parse(solution_file, rename_keys={}):
        """
        Parse solution from file.
        If rename_keys are given, rename variable names according to it.
        """

        if not len(solution_file):  # if file is empty
            return None

        sol_as_list = solution_file.splitlines()

        if "Model status" in sol_as_list:
            # MIP solution
            values = {}

            # extract everything between the first Columns and the first Rows keyword
            col_idx = -1
            row_idx = -1
            for ix, line in enumerate(sol_as_list):
                if "Columns" in line:
                    col_idx = ix
                # row comes after columns, so it is safe to break after row keyword
                if "Row" in line:
                    row_idx = ix
                    break
            if col_idx == -1 or row_idx == -1:
                return values  # no solution

            solution = sol_as_list[col_idx + 1 : row_idx]

            for l in solution:
                var_name, var_val = l.split()
                values[var_name] = float(var_val)

            # adapt variabel names to obfuscated names
            if len(rename_keys) > 0:
                new_values = {}

                for k in rename_keys:
                    new_values[k] = values[rename_keys[k]]

                return new_values
            return values

        else:
            # QUBO solution
            return {idx: val for idx, val in enumerate(sol_as_list)}
