#!/usr/bin/env python3
import shutil

from country_level_lib.config import id_dir
from country_level_lib.id012 import process_id012
from country_level_lib.id3 import process_id3


def main():
    shutil.rmtree(id_dir, ignore_errors=True)
    id_dir.mkdir(parents=True)

    # process_id012()
    process_id3()


if __name__ == "__main__":
    main()
