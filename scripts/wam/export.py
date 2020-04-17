#!/usr/bin/env python3

from country_levels_lib.wam import wam_export
from country_levels_lib.wam.wam_collect import save_wam_population


def main():
    save_wam_population()

    for simp in ['high', 'medium', 'low']:
        wam_export.split_geojson(1, simp)
        wam_export.split_geojson(2, simp)


if __name__ == "__main__":
    main()
