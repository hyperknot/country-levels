#!/usr/bin/env python3
import shutil

from country_level_lib.config import export_geojson_dir
from country_level_lib.geojson import export_id0, export_id1, export_id2, export_id3


def main():
    shutil.rmtree(export_geojson_dir, ignore_errors=True)
    export_geojson_dir.mkdir(parents=True)

    # export to different simplification levels
    for simp in [0, 5, 6, 7, 8]:
        export_id0(simp)
        export_id1(simp)
        export_id2(simp)
        export_id3(simp)


if __name__ == "__main__":
    main()
