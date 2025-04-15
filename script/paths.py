from pathlib import Path

GENERATOR_DIRECTORY = Path(__file__).parent.parent.resolve()
GENERATOR_CSS_DIRECTORY = GENERATOR_DIRECTORY / Path("css")

SOURCE_DIRECTORY = Path.cwd() / Path("docs")
SOURCE_INDEX_FILE = SOURCE_DIRECTORY / Path("index.md")
SOURCE_CSS_DIRECTORY = SOURCE_DIRECTORY / Path("css")

OUTPUT_DIRECTORY = Path.cwd() / Path("static")
OUTPUT_INDEX_FILE = OUTPUT_DIRECTORY / Path("index.html")
OUTPUT_MEDIA_DIRECTORY = OUTPUT_DIRECTORY / Path("media")
OUTPUT_CSS_DIRECTORY = OUTPUT_DIRECTORY / Path("css")

