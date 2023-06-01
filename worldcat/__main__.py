# -*- coding: utf-8 -*-
"""This module contains CLI entrypoint."""
import argparse
import typing
from pathlib import Path

from .worldcat import load, save


def read_folder(path: typing.Union[Path, str]) -> typing.Iterator[Path]:
    """Reads folder yielding each file separately."""
    if isinstance(path, str):
        path = Path(path).resolve()
    for file in path.rglob("*.txt"):
        yield file


def main() -> int:
    """Worldcat's parser CLI."""
    parser = argparse.ArgumentParser(description="Parse database.")
    parser.add_argument("--path", help="path to directory with .txt files.")
    parser.add_argument("--output-file", help="path to output file.")
    parser.add_argument("--encoding", default="utf-8", help="files encoding.")
    args = parser.parse_args()

    data = []
    for export in read_folder(args.path):
        parsed = load(export, encoding=args.encoding)
        data.extend(parsed)

    save(data, Path(args.output_file).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
