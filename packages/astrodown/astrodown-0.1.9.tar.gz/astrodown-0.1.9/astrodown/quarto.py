"""
helpers for constructing post render scripts for Quarto projects
"""
from pathlib import Path
import shutil
import os
import re
from rich.console import Console
from astrodown.utils import enpath

console = Console()


def path_contains_dir(path: Path | str, dir: str):
    path = enpath(path)
    return len(list(path.glob(dir))) > 0


def move_html_assets(
    src: Path | str,
    public_dir: Path | str,
):
    src = enpath(src)
    assets = src.glob("**/*_files")

    for asset in assets:
        if path_contains_dir(asset, "libs"):
            add_html_dep(asset / "libs", public_dir)


def move_assets(src: Path | str, public_dir: Path | str):
    src = enpath(src)
    public_dir = enpath(public_dir)

    assets = src.glob("**/*_files")
    for asset in assets:
        parts = asset.parts
        if "content" in parts:
            suffix = os.path.join(*parts[parts.index("content") + 1 :])
        else:
            suffix = dir
        dest = Path(public_dir, suffix)
        # hack to fix bug in moving assets for index.qmd
        if "public/public" in str(dest):
            shutil.rmtree(Path("src/content/public"))
            return
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(asset, dest)


def add_html_dep(dir: Path | str, public_dir: Path | str):
    lib_files = dir.glob("*")
    dest_dir = public_dir / "libs"
    # [analysis/<analysis-name>/<anlysis-name>_files/libs/jquery-1.11.1]
    for dependency in lib_files:
        dest = dest_dir / dependency.name  # public/libs/jquery-1.11.1
        if not dest.is_dir():
            shutil.move(dependency, dest)
    shutil.rmtree(dir)


def adjust_resource_links(file: str | Path):
    path = enpath(file)
    # example path.parts
    # ('src', 'content', 'analysis', 'dynamic-rmd-quarto', 'index.md')
    parent_dirs = path.parts[:-1]
    if parent_dirs[-1] == "content":
        # this is the index.md for home page
        prefix = ""
    else:
        dir = parent_dirs[2]  # "data" or "analysis"
        prefix = "/" + os.path.join(
            *parent_dirs[parent_dirs.index(dir) :]
        )  # analysis/dynamic-rmd-quarto
    with path.open(mode="r+") as f:
        lines_replaced = [process_line(line, prefix) for line in f]
        f.seek(0)
        f.writelines(lines_replaced)
        f.truncate()


def process_line(line: str, prefix: str):
    # check for gfm markdown image syntax
    if re.match(r"^!\[.*\]\(.+\)", line):
        line_replaced = re.sub(
            r"^!\[(.*)\]\((.+)\)", r"![\1]({prefix}/\2)".format(prefix=prefix), line
        )
        return line_replaced

    match = re.match(r"^(<script|<link|<img).+?>", line)
    if match is None:
        return line

    type = re.match(r"^<\w+", line).group(0).strip("<").strip(" ")
    if type == "script":
        return prefix_resource_link(line, "src", prefix)

    elif type == "link":
        return prefix_resource_link(line, "href", prefix)

    elif type == "img":
        return prefix_resource_link(line, "src", prefix)


def prefix_resource_link(line, attr, prefix):
    match = re.search(r'{attr}="(.*?)"'.format(attr=attr), line)
    if match:
        attr_val = match.group(1)
        if not attr_val.startswith("http"):
            if "libs" in attr_val:
                libs_idx = attr_val.find("libs")
                libs_idx = libs_idx + len("libs")
                line_replaced = re.sub(
                    r'{attr}="(.*?)"'.format(attr=attr),
                    r'{attr}="/libs{after}"'.format(attr=attr, after=attr_val[libs_idx:]),
                    line,
                )
            else:
                line_replaced = re.sub(
                    r'{attr}="(.*?)"'.format(attr=attr),
                    r'{attr}="{prefix}/\1"'.format(attr=attr, prefix=prefix),
                    line,
                )

            return line_replaced

    return line
