import typer


class CLIApplication:
    help: str = ""

    def __init__(self) -> None:
        if not self.help:
            raise Exception("Application help message is mandatory")
        self.app = typer.Typer(add_completion=False, help=self.help)

    def register_command(self, command):
        cmd = self.app.command(name=command.name, help=command.help)
        cmd(command.handler)


echo = typer.echo
confirm = typer.confirm
Abort = typer.Abort
Option = typer.Option
