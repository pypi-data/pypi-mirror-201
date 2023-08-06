import os
from asyncio import StreamReader, run
from pydantic import FilePath, DirectoryPath
import pywas.wrapper.base_wrapper as base_wrapper
from typer import Typer
import wget
import zipfile

ng_spice = Typer()


async def parse_out(stdout: StreamReader) -> base_wrapper.ResultDict:
    ind = 0
    var_name = list()
    step = "start"
    results = base_wrapper.ResultDict()
    while line := await stdout.readline():
        l_str = line.decode()
        if l_str.startswith("Variables"):
            step = "var_name"
        if l_str.startswith("Values"):
            step = "values"
            continue
        l_split = l_str.split()
        # Variables name part
        if step == "var_name" and len(l_split) == 3:
            try:
                int(l_split[0])
            except ValueError:
                continue
            var_name.append(l_split[1])
            results[l_split[1]] = list()
            continue
        # Values extractions part
        if step == "values":
            if len(l_split) == 2:
                ind = 0
                results[var_name[ind]].append(float(l_str.split()[1]))
            else:
                r = float(l_str)
                ind += 1
                results[var_name[ind]].append(r)
    return results


async def parse_err(stderr: StreamReader, log_folder: DirectoryPath):
    """
    Dump the output of the error pipe
    """
    if not os.path.isdir(log_folder):
        os.mkdir(log_folder)
    with open(log_folder + "err.out", "wb") as err:
        err.write(await stderr.read())


@ng_spice.command()
def install():
    """
    Install ngspice executable in the correct location.
    """
    if os.name == "posix":
        os.system("sudo apt-get install ngspice")
        conf = {"ngspice": {"path": "ngspice"}}
    else:
        ngspice_version = 38
        ngspice_base_url = f"https://sourceforge.net/projects/ngspice/files/ng-spice-rework/{ngspice_version}/"
        ngspice_archive_name = f"ngspice-{ngspice_version}_64.zip"
        base_install = f"{os.getcwd()}/simulators/"
        if not (os.path.isdir(base_install)):
            os.makedirs(base_install)
        wget.download(ngspice_base_url + ngspice_archive_name, base_install)
        with zipfile.ZipFile(base_install + ngspice_archive_name) as archive:
            archive.extractall(base_install)
        os.remove(base_install + ngspice_archive_name)
        conf = {"ngspice": {"path": f"{base_install}Spice64/bin/ngspice_con.exe"}}
    base_wrapper.write_conf(conf)


@ng_spice.command()
def config(key: str, path: str) -> bool:
    base_wrapper.write_conf({"ngspice": {key: path}})
    return True


NGSpice = base_wrapper.BaseWrapper(
    name="ngspice",
    input_extension=("net", "cir"),
    output_extension="out",
    parse_out=parse_out,
    parse_err=parse_err,
    install=install,
    config=config,
)


@ng_spice.command(name="run")
def run_p(in_file: str, out_folder: str = f"{os.getcwd()}/tmp/"):
    """
    Should not be named "run"
    """
    run(NGSpice.run(in_file, out_folder))
    NGSpice.export(f"{out_folder}/res.hdf5")
