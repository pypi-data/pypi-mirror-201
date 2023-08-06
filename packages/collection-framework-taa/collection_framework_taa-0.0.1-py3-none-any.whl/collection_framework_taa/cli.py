from argparse import ArgumentParser, FileType, Namespace

from .collect_framework import unique_symbol
from .exceptions import UniqueArgsError


def get_args() -> Namespace:
    parser = ArgumentParser(
        description="counting unique characters in a string or file"
    )
    parser.add_argument("--file", type=FileType(), help="file to count")
    parser.add_argument("--string", help="string to count")
    return parser.parse_args()


def get_result(args: Namespace | None = None) -> int:
    args = args or get_args()
    if args.file:
        return unique_symbol(args.file.read())
    if args.string:
        return unique_symbol(args.string)
    raise UniqueArgsError("No arguments")
