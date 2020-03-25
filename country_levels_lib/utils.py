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


def read_file(file_path: pathlib.Path):
    with file_path.open() as infile:
        return infile.read()


def write_file(file_path: pathlib.Path, text):
    with file_path.open('w') as outfile:
        outfile.write(text)


def split_to_chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def osm_url(id_):
    return f'https://www.openstreetmap.org/relation/{id_}'


def wd_url(id_):
    return f'https://www.wikidata.org/wiki/{id_}'
