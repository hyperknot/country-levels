#!/usr/bin/env python3
import shutil

from country_levels_lib.config import ne_id_dir
from country_levels_lib.ne012 import process_ne012
from country_levels_lib.ne3 import process_ne3


def main():
    shutil.rmtree(ne_id_dir, ignore_errors=True)
    ne_id_dir.mkdir(parents=True)

    process_ne012()
    process_ne3()


if __name__ == "__main__":
    main()
