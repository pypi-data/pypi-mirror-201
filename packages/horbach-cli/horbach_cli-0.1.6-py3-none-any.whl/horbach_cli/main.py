import logging
import typing as t

from rich.logging import RichHandler
from rich import print
import typer

from horbach_cli import __version__
from horbach_cli.libs.common import log_lvl_callback, LOG_LVL
from horbach_cli import converter, deduplicator

app = typer.Typer(rich_markup_mode="markdown")


def version_callback(value: bool):
    version = __version__
    if value:
        print(f":speech_balloon: h-cli Version: {version}")
        raise typer.Exit()


@app.callback()
def main(
    verbose: str = typer.Option(
        "INFO", "--verbose", "-v", callback=log_lvl_callback, help=f":mag: `LOG_LEVEL` one of: {', '.join(LOG_LVL)}"
    ),
    version: t.Optional[bool] = typer.Option(None, "--version", callback=version_callback, is_eager=True),
):
    logging.basicConfig(
        level=verbose, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)]
    )


app.add_typer(converter.app, name="converter", help=":rocket: manipulates files and etc.", rich_help_panel="Hacks")
app.add_typer(
    deduplicator.app, name="dedub", help=":two_men_holding_hands: dedublicates something.", rich_help_panel="Hacks"
)

if __name__ == "__main__":
    app(prog_name="h-cli")
