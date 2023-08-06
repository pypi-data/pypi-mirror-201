import os
import logging

from PIL import Image


def convert_images_to_pdf(images_folder: str, pdf_file: str) -> None:
    images = []
    allowed_formats = (".jpg", ".png", ".jpeg")
    files = os.listdir(images_folder)
    files.sort()
    logging.info(f"Files in the {images_folder} -> {files}")
    for file in files:
        logging.debug(f"Processing with {file}")
        if file.endswith(allowed_formats):
            image = Image.open(os.path.join(images_folder, file))
            if image.mode == "RGBA":
                image = image.convert("RGB")
            images.append(image)
    images[0].save(f"{images_folder}/{pdf_file}", save_all=True, append_images=images[1:])
