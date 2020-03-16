import json
import pathlib


def read_json(file_path: pathlib.Path):
    with file_path.open() as infile:
        return json.load(infile)


def write_json(file_path: pathlib.Path, data, indent: int = None, sort_keys: bool = False):
    with file_path.open('w') as outfile:
        json.dump(
            data, outfile, ensure_ascii=False, indent=indent, allow_nan=False, sort_keys=sort_keys
        )
