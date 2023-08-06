import typer
from .wrapper.ngspice import ng_spice

"""could be :
    from importlib import import_module
    module = import_module(var: str)
"""
help = """
*Py*thon *W*rapper for *A*nalog design *S*oftware

**Installation using [pipx](https://pypa.github.io/pipx/installation/)**:

```console
$ pipx install pywas
```
"""
cli = typer.Typer(help=help)
cli.add_typer(ng_spice, name="ngspice")

@cli.command("new")
def new_project(name: str, ):
    return

if __name__ == "__main__":
    cli()
