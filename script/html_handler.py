from pathlib import Path
import os
import re

from paths import *

TITLE = "Epic Site"

def format(content, relative_path):
    # Use a css path relative to the current file to be compatible with
    # viewing the site on a local machine
    relative_root = os.path.relpath(OUTPUT_DIRECTORY, relative_path.parent)
    relative_css = relative_root / Path('css')
    relative_main_css = relative_css / Path('main.css')

    # Load the base template
    base_template = open(GENERATOR_TEMPLATE_DIRECTORY / Path("base.html")).read()

    # Indent each line in the content
    content = ''.join([f"  {line}\n" for line in content.split('\n') if len(line)])

    # Substitute the various comments in the template
    res = re.sub(r'<!--\s*title\s*-->', TITLE, base_template)
    res = re.sub(r'<!--\s*base_css\s*-->', str(relative_main_css), res)
    res = re.sub(r'<!--\s*content\s*-->', content, res)

    return res
