# -*- coding: utf-8 -*-
from pathlib import Path

import worldcat


def main() -> int:
    assets = Path(__file__).resolve().parent.parent / "assets"
    input_file = assets / "raw" / "DirectExport.txt"
    parser = worldcat.Parser()
    data = worldcat.load(input_file, encoding="cp1251", implementation=parser)
    output_file = assets / "export.json"
    worldcat.save(data, output_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
