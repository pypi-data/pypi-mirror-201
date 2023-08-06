import logging
from pathlib import Path
import typing as t
import os

import typer
from rich import print
from rich.prompt import Confirm

from difPy import dif

app = typer.Typer()


@app.command(help="deal with dublicated :camera: images")
def img_dedub(
    dirs: t.List[Path] = typer.Argument(..., help="Path to dirs with images"),
    delete: bool = False,
):
    search = dif(dirs, recursive=True)

    for entry in search.result:
        entry_payload = search.result[entry]

        origin = entry_payload["location"]
        print(f":floppy_disk: origin -> {origin}")

        dublicates = list()
        for d in entry_payload["matches"]:
            dublicates.append(entry_payload["matches"][d]["location"])
        print(f"dublicates: {dublicates}")

        if delete and Confirm.ask(":skull: Are you sure want to delete duplicates?"):
            for d in dublicates:
                logging.info(f"Deleting: {d}")
                os.remove(d)


if __name__ == "__main__":
    app()
