import argparse
from argparse import Namespace

from collection_framework.unique_collection import unique_symbol

from .my_exceptions import NoArgumentsError


def get_args() -> Namespace:
    parser = argparse.ArgumentParser(description='Counting unique symbols')
    parser.add_argument("--string", "-s", help='Enter data for processing')
    parser.add_argument("--file",
                        "-f",
                        type=argparse.FileType(),
                        help='Enter file name')
    return parser.parse_args()


def get_result() -> int:
    args = get_args()
    if not args.file and not args.string:
        raise NoArgumentsError('You need to enter arguments')
    if args.file:
        return unique_symbol(args.file.read())
    return unique_symbol(args.string)
