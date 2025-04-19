import os
import re
from pathlib import Path

from paths import *


def add_width_to_img_tag(match):
    tag = match.group(0)
    if "width=" not in tag:
        # Insert width before the closing >
        tag = (
            tag.rstrip("/>") + ' width="1000"' + (" />" if tag.endswith("/>") else ">")
        )
    return tag


def format_header(header_template, relative_root, site_name):
    relative_index = relative_root / Path("navigation.html")
    relative_home = relative_root / Path("index.html")

    relative_logo = None

    for extension in ["png", "jpg", "jpeg"]:
        test_path = OUTPUT_MEDIA_DIRECTORY / Path(f"logo.{extension}")

        if test_path.is_file():
            relative_logo = test_path
            print(f"Found logo at {relative_logo}")
            break

    if relative_logo is not None:
        img_tag = f'<img src="{relative_logo}" alt="{site_name}" class="logo-img">'
    else:
        relative_logo = OUTPUT_MEDIA_DIRECTORY / Path("logo.svg")
        img_tag = open(relative_logo).read()

    header_template = re.sub(r"<!--\s*title\s*-->", site_name, header_template)
    header_template = re.sub(r"<!--\s*logo\s*-->", img_tag, header_template)
    header_template = re.sub(r"<!--\s*home\s*-->", str(relative_home), header_template)
    header_template = re.sub(
        r"<!--\s*index\s*-->", str(relative_index), header_template
    )

    # Indent each line in the content
    header_template = "".join(
        [f"  {line}\n" for line in header_template.split("\n") if len(line)]
    )

    return header_template


def format_footer(footer_template, relative_root):
    contact_mail = get_from_def_file("CONTACT_EMAIL", None)
    if contact_mail:
        contact_string = f'<p>Contact: <a href="mailto:{contact_mail}">{contact_mail}</a></p>'
    else:
        contact_string = ""

    about_entity = get_from_def_file("ABOUT_ENTITY", None)
    if not about_entity:
        about_entity = ""
    else:
        about_entity = f" {about_entity}"

    about_me_file = SOURCE_DIRECTORY / Path("about.md")
    about_me_relative_root = relative_root / Path("about.html")
    about_me_string = ""
    if about_me_file.is_file():
        about_me_string = f'<a href="{about_me_relative_root}">About{about_entity}</a>'

    about_this_site_file = SOURCE_DIRECTORY / Path("about_site.md")
    about_this_site_relative_root = relative_root / Path("about_site.html")
    about_this_site_string = ""
    if about_this_site_file.is_file():
        about_this_site_string = f'<a href="{about_this_site_relative_root}">About this site</a>'

    res = re.sub(r"<!--\s*contact\s*-->", contact_string, footer_template)
    res = re.sub(r"<!--\s*about\s*-->", about_me_string, res)
    res = re.sub(r"<!--\s*about_site\s*-->", about_this_site_string, res)

    return res


def format_base(base_template, relative_root, site_name):
    # Use a css path relative to the current file to be compatible with
    # viewing the site on a local machine
    relative_css = relative_root / Path("css")
    relative_main_css = relative_css / Path("main.css")
    relative_theme_css = relative_css / Path("theme.css")
    relative_fonts_css = relative_css / Path("fonts.css")
    relative_header_css = relative_css / Path("header.css")
    relative_footer_css = relative_css / Path("footer.css")
    relative_navigation_css = relative_css / Path("navigation.css")

    # Substitute the various comments in the template
    res = re.sub(r"<!--\s*title\s*-->", site_name, base_template)

    res = re.sub(r"<!--\s*base_css\s*-->", str(relative_main_css), res)
    res = re.sub(r"<!--\s*theme_css\s*-->", str(relative_theme_css), res)
    res = re.sub(r"<!--\s*fonts_css\s*-->", str(relative_fonts_css), res)
    res = re.sub(r"<!--\s*header_css\s*-->", str(relative_header_css), res)
    res = re.sub(r"<!--\s*footer_css\s*-->", str(relative_footer_css), res)
    res = re.sub(r"<!--\s*navigation_css\s*-->", str(relative_navigation_css), res)

    return res


def format_content(base_template, content):
    # Indent each line in the content
    content = "".join([f"  {line}\n" for line in content.split("\n") if len(line)])
    res = re.sub(r"<!--\s*content\s*-->", content, base_template)

    # Add a width to each img element, to keep support for non-css browsers
    res = re.sub(r"<img\b[^>]*>", add_width_to_img_tag, res)

    # Substitute all URLs to markdown documents to html
    res = re.sub(r'(<a[^>]+href=["\'])([^"\']+?)\.md(["\'])', r'\1\2.html\3', res)

    return res


def insert_header_and_footer(base_template, header_template, footer_template):
    res = re.sub(r"<!--\s*header\s*-->", header_template, base_template)
    res = re.sub(r"<!--\s*footer\s*-->", footer_template, res)
    return res


def format(content, relative_path):
    # Use a css path relative to the current file to be compatible with
    # viewing the site on a local machine
    relative_root = os.path.relpath(OUTPUT_DIRECTORY, relative_path.parent)

    # Load the base, header and footer templates from the source directory if they exists.
    # Otherwise, use the generator template
    base_template_file = SOURCE_TEMPLATE_DIRECTORY / Path("base.html")
    if not base_template_file.is_file():
        base_template_file = GENERATOR_TEMPLATE_DIRECTORY / Path("base.html")

    header_template_file = SOURCE_TEMPLATE_DIRECTORY / Path("header.html")
    if not header_template_file.is_file():
        header_template_file = GENERATOR_TEMPLATE_DIRECTORY / Path("header.html")

    footer_template_file = SOURCE_TEMPLATE_DIRECTORY / Path("footer.html")
    if not footer_template_file.is_file():
        footer_template_file = GENERATOR_TEMPLATE_DIRECTORY / Path("footer.html")

    # Load the templates contents
    base_template = open(base_template_file).read()
    header_template = open(header_template_file).read()
    footer_template = open(footer_template_file).read()

    site_name = get_from_def_file("SITE_NAME", "Unnamed Site")

    base_template = format_base(base_template, relative_root, site_name)
    header_template = format_header(header_template, relative_root, site_name)
    footer_template = format_footer(footer_template, relative_root)
    base_template = format_content(base_template, content)
    base_template = insert_header_and_footer(base_template, header_template, footer_template)

    return base_template
