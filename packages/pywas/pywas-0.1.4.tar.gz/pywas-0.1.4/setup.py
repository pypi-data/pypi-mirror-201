# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywas', 'pywas.parse', 'pywas.wrapper']

package_data = \
{'': ['*'], 'pywas': ['template/*']}

install_requires = \
['h5py>=3.7.0,<4.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'numpy>=1.23.2,<2.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=13.3.3,<14.0.0',
 'typer>=0.7.0,<0.8.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['pywas = pywas.main:cli']}

setup_kwargs = {
    'name': 'pywas',
    'version': '0.1.4',
    'description': '',
    'long_description': '# `pyWAS`\n\n*Py*thon *W*rapper for *A*nalog design *S*oftware\n\n**Installation using [pipx](https://pypa.github.io/pipx/installation/)**:\n\n```console\n$ pipx install pywas\n```\n\n**Usage**:\n\n```console\n$ pyWAS [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `new`\n* `ngspice`\n\n## `pyWAS new`\n\n**Usage**:\n\n```console\n$ pyWAS new [OPTIONS] NAME\n```\n\n**Arguments**:\n\n* `NAME`: [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `pyWAS ngspice`\n\n**Usage**:\n\n```console\n$ pyWAS ngspice [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `config`\n* `install`: Install ngspice executable in the correct...\n* `run`: Should not be named "run"\n\n### `pyWAS ngspice config`\n\n**Usage**:\n\n```console\n$ pyWAS ngspice config [OPTIONS] KEY PATH\n```\n\n**Arguments**:\n\n* `KEY`: [required]\n* `PATH`: [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### `pyWAS ngspice install`\n\nInstall ngspice executable in the correct location.\n\n**Usage**:\n\n```console\n$ pyWAS ngspice install [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### `pyWAS ngspice run`\n\nShould not be named "run"\n\n**Usage**:\n\n```console\n$ pyWAS ngspice run [OPTIONS] IN_FILE\n```\n\n**Arguments**:\n\n* `IN_FILE`: [required]\n\n**Options**:\n\n* `--out-folder TEXT`: [default: C:\\Users\\Potereau\\PycharmProjects\\pyWES/tmp/]\n* `--help`: Show this message and exit.\n',
    'author': 'Patarimi',
    'author_email': 'mpqqch@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
