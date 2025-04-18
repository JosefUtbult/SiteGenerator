import re
from pathlib import Path

GENERATOR_DIRECTORY = Path(__file__).parent.parent.resolve() / Path("site")
GENERATOR_MEDIA_DIRECTORY = GENERATOR_DIRECTORY / Path("media")
GENERATOR_CSS_DIRECTORY = GENERATOR_DIRECTORY / Path("css")
GENERATOR_FONT_DIRECTORY = GENERATOR_DIRECTORY / Path("fonts")
GENERATOR_TEMPLATE_DIRECTORY = GENERATOR_DIRECTORY / Path("templates")

SOURCE_DIRECTORY = Path.cwd() / Path("docs")
SOURCE_MEDIA_DIRECTORY = SOURCE_DIRECTORY / Path("media")
SOURCE_CSS_DIRECTORY = SOURCE_DIRECTORY / Path("css")
SOURCE_FONT_DIRECTORY = SOURCE_DIRECTORY / Path("fonts")
SOURCE_TEMPLATE_DIRECTORY = SOURCE_DIRECTORY / Path("templates")
SOURCE_DEF_FILE = SOURCE_DIRECTORY / Path("generator.def")

OUTPUT_DIRECTORY = Path.cwd() / Path("static")
OUTPUT_MEDIA_DIRECTORY = OUTPUT_DIRECTORY / Path("media")
OUTPUT_CSS_DIRECTORY = OUTPUT_DIRECTORY / Path("css")
OUTPUT_FONT_DIRECTORY = OUTPUT_DIRECTORY / Path("fonts")
OUTPUT_TEMPLATE_DIRECTORY = OUTPUT_DIRECTORY / Path("templates")

SOURCE_INDEX_FILE = SOURCE_DIRECTORY / Path("index.md")
OUTPUT_INDEX_FILE = OUTPUT_DIRECTORY / Path("index.html")


def get_from_def_file(key, default_value):
    if SOURCE_DEF_FILE.is_file():
        def_file_content = open(SOURCE_DEF_FILE).read()
        match = re.search(
            rf'^{key}\s*=\s*["\']?(.*?)["\']?$', def_file_content, re.MULTILINE
        )
        if match:
            return match.group(1)

    return default_value
