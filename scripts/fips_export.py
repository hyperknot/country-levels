#!/usr/bin/env python3
from pprint import pprint

from country_levels_lib.fips_utils import get_county_data


def main():
    data = get_county_data()
    pprint(data)
    # export_fips()


if __name__ == "__main__":
    main()
