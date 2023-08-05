from toolbox import cli


def version():
    """
    Reads the version from the installed package and prints it.
    """
    from importlib.metadata import version as get_version

    cli.echo(get_version("housenomics"))


class CommandVersion:
    name = "version"
    help = "Shows current version"
    handler = version
