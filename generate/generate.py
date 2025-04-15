from pathlib import Path

OUTPUT_DIRECTORY = Path("../static")

def setup():
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    print(f"Generating static site into {OUTPUT_DIRECTORY}")
    setup()

    index = OUTPUT_DIRECTORY / Path('index.html')
    print(f"Writing index to {index}")
    with open(index, 'w') as index:
        index.write("<h1>Hello World!</h1>")
