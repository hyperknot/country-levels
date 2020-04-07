#!/usr/bin/env python3

from country_levels_lib.wam.wam_docs import (
    generate_iso1_list,
    generate_iso2_list,
)


def main():
    generate_iso1_list()
    generate_iso2_list()


if __name__ == "__main__":
    main()
