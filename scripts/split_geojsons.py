#!/usr/bin/env python3
import shutil

from country_levels_lib.config import export_dir


def main():
    shutil.rmtree(export_dir, ignore_errors=True)
    export_dir.mkdir()

    geojson_level_012()
    # process_level_3()


if __name__ == "__main__":
    main()
