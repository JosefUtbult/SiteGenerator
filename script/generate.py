from pathlib import Path
import pandoc

SOURCE_DIRECTORY = Path.cwd() / Path("docs")
SOURCE_INDEX_FILE = SOURCE_DIRECTORY / Path("index.md")
OUTPUT_DIRECTORY = Path.cwd() / Path("static")
OUTPUT_INDEX_FILE = OUTPUT_DIRECTORY / Path("index.html")
OUTPUT_MEDIA_DIRECTORY = OUTPUT_DIRECTORY / Path("media")

def setup():
    if not SOURCE_DIRECTORY.is_dir():
        print(f"No source directory found at {SOURCE_DIRECTORY}")
        exit(1)

    if not SOURCE_INDEX_FILE.is_file():
        print(f"No source index.md found at {SOURCE_INDEX_FILE}")
        exit(1)

    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    print(f"Generating static site into {OUTPUT_DIRECTORY}")
    setup()

    index = OUTPUT_DIRECTORY / Path('index.html')
    print(f"Writing index to {index}")

    index_pandoc = pandoc.read(file=SOURCE_INDEX_FILE, format='markdown', options=["--extract-media", OUTPUT_MEDIA_DIRECTORY])
    pandoc.write(index_pandoc, file=OUTPUT_INDEX_FILE, format='html')

    # with open(index, 'w') as file:
    #     file.write("<h1>Hello World!</h1>")
