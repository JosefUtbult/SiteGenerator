from paths import *
from setup_folders import setup
from markdown import iterate_and_generate
from index_generator import generate_index

if __name__ == '__main__':
    print(f"Generating static site into {OUTPUT_DIRECTORY}")
    setup()
    iterate_and_generate()
    generate_index()
