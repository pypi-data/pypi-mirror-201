import subprocess
import logging

import typer
from rich import print

from horbach_cli.libs.converter import convert_images_to_pdf

app = typer.Typer()


@app.command(help=":camera: images into :memo: pdf")
def img_to_pdf(
    images_folder: str = typer.Argument(..., help="Path to folder with images"),
    pdf_file: str = typer.Argument("result.pdf", help="Result file name"),
):
    convert_images_to_pdf(images_folder, pdf_file)


@app.command(help=":camera: images from :green_apple: heic to jpg")
def heic_to_jpg(images_folder: str = typer.Argument(..., help="Path to folder with images")):
    cmd = f"magick mogrify -monitor -format jpg {images_folder}/*.HEIC {images_folder}/*.heic"
    result = subprocess.run(cmd.split(), capture_output=True, text=True)
    print(":tada: converting has finished")
    logging.debug(result.stderr)


if __name__ == "__main__":
    app()
