import os

import click

plugin_folder = os.path.join(os.path.dirname(__file__), "commands")


class FtCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith(".py") and filename.startswith("ftcli_"):
                rv.append(filename[6:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"ftCLI.commands.ftcli_{name}", None, None, ["cli"])
        except ImportError as e:
            print(e)
            return

        return mod.cli


cli = FtCLI(help="A command line font editor.")


def main():
    cli()
