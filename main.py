import worldcat
from pathlib import Path


def main() -> int:
    data = Path(__file__).resolve().parent / "assets" / "raw" / "DirectExport.txt"
    parser = worldcat.Parser()

    data = worldcat.load(data, encoding="cp1251", implementation=parser)
    breakpoint()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
