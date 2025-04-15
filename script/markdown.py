from pathlib import Path
import pandoc

from paths import *
from images import extract_images
from html_handler import format

def iterate_and_generate():
    for source_path in SOURCE_DIRECTORY.rglob('*.md'):
        relative_path = source_path.relative_to(SOURCE_DIRECTORY)
        dest_path = OUTPUT_DIRECTORY / relative_path.with_suffix(".html")

        print(f"Generating {source_path} -> {dest_path}")

        pandoc_tree = pandoc.read(file=source_path, format='markdown')

        extract_images(pandoc_tree, relative_path)

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        res = pandoc.write(pandoc_tree, format='html')
        formated = format(res, dest_path)

        with open(dest_path, 'w') as file:
            file.write(formated)

