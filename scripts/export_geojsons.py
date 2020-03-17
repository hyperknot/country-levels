#!/usr/bin/env python3
import shutil

from country_level_lib.config import export_dir
from country_level_lib.geojson import export_id0, export_id1, export_id2, export_id3


def main():
    shutil.rmtree(export_dir, ignore_errors=True)
    export_dir.mkdir(parents=True)

    # export_id0()
    # export_id1()
    # export_id2()
    export_id3()


if __name__ == "__main__":
    main()
