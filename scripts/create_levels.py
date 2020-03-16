#!/usr/bin/env python3
import shutil

from country_levels_lib.config import levels_dir
from country_levels_lib.level_012 import process_level_012
from country_levels_lib.level_3 import process_level_3


def main():
    # shutil.rmtree(levels_dir, ignore_errors=True)
    # process_level_012()
    process_level_3()


if __name__ == "__main__":
    main()
