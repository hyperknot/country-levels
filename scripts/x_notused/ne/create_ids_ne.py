#!/usr/bin/env python3
import shutil

from country_levels_lib.config import id_dir
from country_levels_lib.ne012 import process_ne012
from country_levels_lib.ne3 import process_ne3


def main():
    shutil.rmtree(id_dir, ignore_errors=True)
    id_dir.mkdir(parents=True)

    process_ne012()
    process_ne3()


if __name__ == "__main__":
    main()
