from typing import List
from pydantic import FilePath
import numpy as np
from .results import ResultDict


def read(result_file: FilePath):
    """
    read a spice3 raw files and convert it to a dict.
    :param result_file:
    :return:
    di
    """
    num_var: int
    num_pts: int
    var_names: List[str] = list()
    results: ResultDict = dict()
    with open(result_file) as f:
        for line in f:
            if "No. Variables:" in line:
                num_var = int(line.split(" ")[2])
                print(f"{num_var} variables expected")
                break
        for line in f:
            if "No. Points:" in line:
                num_pts = int(line.split(" ")[2])
                print(f"{num_pts} points expected")
                break
        for line in f:
            if "Variables" in line:
                continue
            var_names.append(line.split("\t")[2])
            if len(var_names) >= num_var:
                print(var_names)
                break
        for name in var_names:
            results[name] = np.zeros(num_pts)
        i = 0
        for line in f:
            if "Values" in line:
                continue
            if i == 0:
                results[var_names[i]] = float(line.split("\t")[2])
            else:
                results[var_names[i]] = float(line)
            i = 0 if (i >= num_var - 1) else i + 1
    return results
