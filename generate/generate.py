from pathlib import Path

OUTPUT_DIRECTORY = Path("../static")

def setup():
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    print(f"Generating static site into {OUTPUT_DIRECTORY}")
    setup()

    with open(OUTPUT_DIRECTORY / Path('index.html'), 'w') as index:
        index.write("<h1>Hello World!</h1>")
