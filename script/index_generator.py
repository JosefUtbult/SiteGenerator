import os
import re
from pathlib import Path

from html_handler import format
from paths import *

def generate_tree(index_file):
    tree = {}

    for document in OUTPUT_DIRECTORY.rglob("*.html"):
        if document == index_file:
            continue

        relative_root = Path(os.path.relpath(document, OUTPUT_DIRECTORY))
        content = open(document, 'r').read()
        title = document.stem

        # Find the first instance of a h1 tag. If none exists, use the filename
        match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE | re.DOTALL)
        if match:
            title = match.group(1)

        # Create a tree structure with all directories
        parts = relative_root.parts
        root = tree
        root_key = None
        previous_root = None
        for part in parts[:-1]:
            if not part in root:
                root[part] = {}

            previous_root = root
            root = root[part]
            root_key = part

        # If the respting filename is the same as the directory name it is under,
        # handle it as if it was the parent directory
        if root_key == title and previous_root is not None:
            del previous_root[root_key]
            previous_root[title] = str(relative_root)
        else:
            root[title] = str(relative_root)

    return tree


def generate_tree_view_recursivly(tree, current_level):
    # You can't use spaces in html paragraphs
    spaces_per_indentation = int(get_from_def_file("NAVIGATION_SPACES_PER_INDENTATION", "6"))

    indentation = '&nbsp' * spaces_per_indentation
    res = ""

    for key in tree:
        item = tree[key]

        # Check if first level overall
        if current_level == 0 and key == list(tree.keys())[0]:
            branch_char = '┌'
            sub_branch_char = '│'
        elif key == list(tree.keys())[-1]:
            branch_char = '└'
            sub_branch_char = '&nbsp' * int(spaces_per_indentation / 3)
        else:
            branch_char = '├'
            sub_branch_char = '│'

        if type(item) is dict:
            res += f'{branch_char}── {key}\n'
            sub_res = generate_tree_view_recursivly(item, current_level + 1)
            for line in [line for line in sub_res.split('\n') if len(line)]:
                res += f'{sub_branch_char}{indentation}{line}\n'

        else:
            res += f'{branch_char}── <a href="{item}">{key}</a>\n'

    return res


def generate_tree_view(tree):
    res = generate_tree_view_recursivly(tree, 0)
    res = ''.join([f"    <p>{line}</p>\n" for line in res.split('\n') if len(line)])
    return res


def generate_list_view_recursivly(tree, current_level):
    res = ""

    for key in tree:
        item = tree[key]

        if type(item) is dict:
            res += f'      <li>{key}\n'
            res += f'        <ul>\n'
            sub_res = generate_list_view_recursivly(item, current_level + 1)
            for line in [line for line in sub_res.split('\n') if len(line)]:
                res += f'    {line}\n'
            res += f'        </ul>\n'
            res += f'      </li>\n'

        else:
            res += f'      <li><a href="{item}">{key}</a></li>\n'

    return res


def generate_list_view(tree):
    return f'    <ul>\n{generate_list_view_recursivly(tree, 1)}    </ul>\n'


def generate_index():
    index_file = OUTPUT_DIRECTORY / Path('navigation.html')

    tree = generate_tree(index_file)

    index_view = get_from_def_file("NAVIGATION_VIEW", None)
    if index_view == "tree":
        res = generate_tree_view(tree)
    else:
        res = generate_list_view(tree)

    # Add a title
    res = f'  <h1>Index</h1>\n  <div class="navigation">\n{res}  </div>'

    res = format(res, index_file)

    with open(index_file, 'w') as file:
        file.write(res)
