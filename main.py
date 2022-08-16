import worldcat
from pathlib import Path


if __name__ == "__main__":
    data = Path(__file__).resolve().parent / "assets" / "raw" / "DirectExport.txt"
    parser = worldcat.Parser()

    data = worldcat.load(data, encoding="cp1251", implementation=parser)
    breakpoint()