#!/usr/bin/env python3
import shutil

from country_level_lib.config import export_dir
from country_level_lib.export import export_0, export_1


def main():
    shutil.rmtree(export_dir, ignore_errors=True)
    export_dir.mkdir()

    export_0()
    export_1()


if __name__ == "__main__":
    main()
