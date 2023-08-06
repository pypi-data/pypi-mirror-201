from sym.flow.cli.helpers.yaml import configure_yaml

from .commands.symflow import symflow

configure_yaml()

if __name__ == "__main__":
    symflow(prog_name="symflow")
