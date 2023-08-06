import h5py
from pydantic import FilePath
from typing import List
from typing_extensions import TypedDict


class ResultDict(TypedDict):
    label: str
    array: List[float]


class H5pyStruct(TypedDict):
    name: str
    result: List[ResultDict]


def write_result(result: ResultDict, result_file: FilePath):
    """
    Export a
    :param result:
    :param result_file:
    :return:
    """
    with h5py.File(result_file, "w") as f:
        for keys in result:
            f[keys] = result[keys]
