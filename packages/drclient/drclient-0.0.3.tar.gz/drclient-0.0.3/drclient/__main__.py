import typer

from .cli import cmd_info, cmd_pull, verbose


def main():
    app = typer.Typer(short_help="Utility for interacting with docker registries")

    app.command(help="Show image info from a docker registry")(cmd_info.info)
    app.command(help="Pull image from a docker registry")(cmd_pull.pull)

    app.callback()(verbose.verbose)
    app()


if __name__ == "__main__":
    main()
