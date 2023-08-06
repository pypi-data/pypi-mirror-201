"""
Base class for spice simulator
"""
import os.path

from pydantic import BaseModel, FilePath, DirectoryPath
from enum import Enum
from typing import List, Optional, Callable
import asyncio
from pywas.parse.results import ResultDict
import h5py
from asyncio import StreamReader
import yaml
from os import getcwd
from rich import print


class BaseWrapper(BaseModel):
    name: str
    input_extension: List[str]
    output_extension: str
    results: Optional[ResultDict]

    """
    Install the software on the machine.
    """
    install: Callable[[], bool]

    """
    Write configuration file
    """
    config: Callable[[], bool]

    """
    Parse the output of the simulation and convert it to a ResultDict
    """
    parse_out: Callable[[StreamReader], ResultDict]
    parse_err: Callable[[StreamReader], ResultDict]

    async def run(
        self,
        sim_file: FilePath,
        out_folder: DirectoryPath = f"{getcwd()}tmp",
    ):
        """
        run the spice simulation describe by the _spice_file
        :param sim_file: input file to be process by the program
        :param out_folder: directory to write simulation log
        :return: a temp file of the raw out of the simulator (to be process by serialize_result)
        """
        cir = open(sim_file)
        conf = load_conf()
        try:
            path = conf[self.name]["path"]
            proc = await asyncio.create_subprocess_shell(
                f"{path} -s",
                stdin=cir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            std_out_task = asyncio.create_task(self.parse_out(proc.stdout))
            std_err_task = asyncio.create_task(self.parse_err(proc.stderr, out_folder))
            res = await asyncio.gather(proc.wait(), std_out_task, std_err_task)
            cir.close()
            self.results = res[1]
        except KeyError:
            please_install(self.name)
            exit()

    def export(self, file: FilePath):
        with h5py.File(file, "w") as f:
            for res in self.results:
                f[f"res/{res}"] = self.results[res]


def load_conf(conf_file: FilePath = f"{getcwd()}/config.yaml") -> dict:
    if not (os.path.isfile(conf_file)):
        with open(conf_file, "w") as f:
            pass
    with open(conf_file) as f:
        conf = yaml.load(f, Loader=yaml.Loader)
    if conf is None:
        return dict()
    return conf


def write_conf(conf: dict, conf_file: FilePath = f"{getcwd()}/config.yaml"):
    conf_old = load_conf(conf_file)
    for key in conf:
        # update key in conf, keep all the old keys
        conf_old[key] = conf[key]
    with open(conf_file, "w") as f:
        f.write(yaml.dump(conf_old, Dumper=yaml.Dumper))


def please_install(prog_name: str) -> None:
    print(
        f"{prog_name} not found in config file. Please run 'pywas {prog_name} install'"
    )
