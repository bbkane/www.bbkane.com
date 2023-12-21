#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
from pathlib import Path

__author__ = "Benjamin Kane"
__version__ = "0.1.0"
__doc__ = f"""
Convert blog from mixed <name.md> and <name/index.md> to all <name/index.md>
Examples:
    {sys.argv[0]}
Help:
Please see Benjamin Kane for help.
Code at <repo>
"""

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--log-level",
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="log level",
    )

    parser.add_argument(
        "--content-dir",
        default="~/Git-GH/www.bbkane.com/content/blog",
        help="dir containing mixed folders and index files",
        type=Path,
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        format="# %(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)s\n%(message)s\n",
        level=logging.getLevelName(args.log_level),
    )

    file: Path
    for file in args.content_dir.expanduser().glob("*.md"):
        if file.name == "_index.md":
            continue
        dirpath = Path(file.parent / file.stem)
        print(dirpath)
        dirpath.mkdir()
        file.rename(dirpath / "index.md")


if __name__ == "__main__":
    main()
