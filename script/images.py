from pathlib import Path
import shutil
import pandoc
from urllib.parse import urlparse

from paths import *

def extract_images(pandoc_tree, relative_path):
    for item in pandoc.iter(pandoc_tree):
        # Filter out non-images
        if type(item) is not pandoc.types.Image:
            continue

        url = ''.join(item[-1])

        # If the URL have a scheme, that means that the image isn't a local file
        if len(urlparse(url).scheme):
            continue

        # If the image is a local file, copy it over to the output directory
        relative_image_path = relative_path.parent / Path(url)
        source_image_path = SOURCE_DIRECTORY / relative_image_path
        dest_image_path = OUTPUT_DIRECTORY / relative_image_path

        if not source_image_path.is_file():
            print(f"WARNING: Unable to find local image {source_image_path}")
            continue

        print(f"Copy image {source_image_path} -> {dest_image_path}")
        dest_image_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_image_path, dest_image_path)

