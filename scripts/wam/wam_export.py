#!/usr/bin/env python3
import shutil

from country_levels_lib.wam import wam_export
from country_levels_lib.config import export_dir


def main():
    shutil.rmtree(export_dir / 'geojson', ignore_errors=True)

    for simp in [5, 7, 8]:
        wam_export.split_geojson(1, simp, debug=False)
        wam_export.split_geojson(2, simp, debug=False)


if __name__ == "__main__":
    main()
