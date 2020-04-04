#!/usr/bin/env python3
import shutil

from country_levels_lib.config import export_geojson_dir
from country_levels_lib.ne.ne_geojson import export_ne0, export_ne1, export_ne2, export_ne3


def main():
    shutil.rmtree(export_geojson_dir, ignore_errors=True)
    export_geojson_dir.mkdir(parents=True)

    # export to different simplification levels
    for simp in [0, 5, 7, 8]:
        export_ne0(simp)
        export_ne1(simp)
        export_ne2(simp)
        export_ne3(simp)


if __name__ == "__main__":
    main()
