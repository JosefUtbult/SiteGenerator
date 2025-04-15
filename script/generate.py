from paths import *
from setup_folders import setup
from markdown import iterate_and_generate

if __name__ == '__main__':
    print(f"Generating static site into {OUTPUT_DIRECTORY}")
    setup()
    iterate_and_generate()
