import os
from pathlib import Path
import shutil
import pandoc
from urllib.parse import urlparse

from paths import *
from markdown import iterate_and_generate

def copy_contents(dest_directory, source_directory):
    print(f"Copying contents from {source_directory} to {dest_directory}")

    for item in source_directory.iterdir():
        dest_item = dest_directory / item.name
        if item.is_dir():
            shutil.copytree(item, dest_item, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest_item)


def setup():
    if not SOURCE_DIRECTORY.is_dir():
        print(f"No source directory found at {SOURCE_DIRECTORY}")
        exit(1)

    if not SOURCE_INDEX_FILE.is_file():
        print(f"No source index.md found at {SOURCE_INDEX_FILE}")
        exit(1)

    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    OUTPUT_MEDIA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    OUTPUT_CSS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    OUTPUT_FONT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    copy_contents(OUTPUT_CSS_DIRECTORY, GENERATOR_CSS_DIRECTORY)
    copy_contents(OUTPUT_FONT_DIRECTORY, GENERATOR_FONT_DIRECTORY)
    copy_contents(OUTPUT_MEDIA_DIRECTORY, GENERATOR_MEDIA_DIRECTORY)

    if SOURCE_CSS_DIRECTORY.is_dir():
        copy_contents(OUTPUT_CSS_DIRECTORY, SOURCE_CSS_DIRECTORY)

    if SOURCE_FONT_DIRECTORY.is_dir():
        copy_contents(OUTPUT_FONT_DIRECTORY, SOURCE_FONT_DIRECTORY)

    if SOURCE_MEDIA_DIRECTORY.is_dir():
        copy_contents(OUTPUT_MEDIA_DIRECTORY, SOURCE_MEDIA_DIRECTORY)
