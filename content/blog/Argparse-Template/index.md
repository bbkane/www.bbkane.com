+++
title = "Argparse Template"
date = 2023-08-29
+++

Python's [`argparse`](https://docs.python.org/3/library/argparse.html) library is super flexible. I want to use it to design CLIs like the [`azure-cli`](https://learn.microsoft.com/en-us/cli/azure/), with the following structure (imagine a `conversation-generator` CLI):

```
conversation-generator
        --log-level <value>
    greet
        --name <value>
    conversation
        --mood <value>
        ask
        declare
            --add-random-fact <true|false>
```

This is a pretty rigid structure that I find easy to read and expand. It has the following designed limitations

- No top-level commands - `program-name` doesn't do anything besides print subcommands. All "action" happens via subcommands
- Subcommands can be grouped by subsections, almost like you can group files by directory
- No positional arguments - commands receive all parameters via `--flag`s

I wrote [a Go library](https://github.com/bbkane/warg) to give me this easily, but argparse is flexible enough to do it in Python without too much work. I'm also adding a few convenience flags I find useful, like `--log-level`.

I try to stick to stdlib Python, but if I'm regularly passing files as flag values, I also use [shtab](https://github.com/iterative/shtab) to add zsh completion for files/directories.

So, here's the skeleton:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys

import shtab

__author__ = "Benjamin Kane"
__version__ = "0.1.0"
__doc__ = f"""
<description>
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

    subcommands = parser.add_subparsers(dest="subcommand_name", required=True)

    # greet
    greet_cmd = subcommands.add_parser("greet", help="Say a greeting")
    greet_cmd.add_argument("--name", required=True, help="Person to greet")

    # conversation
    conversation_cmd = subcommands.add_parser("conversation", help="conversation subcommands")
    conversation_cmd.add_argument("--mood", required=True, help="mood for the conversation")

    conversation_subcommands = conversation_cmd.add_subparsers(
        dest="conversation_subcommand_name",
        required=True,
        help="subcommand name",
    )

    # ask
    _ = conversation_subcommands.add_parser("ask", help="ask a question")

    # declare
    declare_cmd = conversation_subcommands.add_parser("declare", help="declare something")

    # Use boolean with a default (--include-random-fact/--no-include-random-fact)
    # alternative to action='store_true'/'store_false'
    declare_cmd.add_argument(
        "--include-random-fact",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="stream change output to stdout in addition to a file",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        format="# %(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)s\n%(message)s\n",
        level=logging.getLevelName(args.log_level),
    )

    match args.subcommand_name:
        case "greet":
            print(f"Hello {args.name}")
        case "conversation":
            match args.conversation_subcommand_name:
                case "ask":
                    print("Huh?")
                case "declare":
                    random_fact = "The sky is blue" if args.include_random_fact else "boring..."
                    print(f"Mood: {args.mood}. I declare: {random_fact}")
                case _:
                    raise SystemExit(f"Unknown subcommand: {args.conversation_subcommand_name!r}")
        case _:
            raise SystemExit(f"Unknown command: {args.subcommand_name!r}")

if __name__ == "__main__":
    main()
```
