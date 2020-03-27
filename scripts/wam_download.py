#!/usr/bin/env python3
from country_levels_lib.wam_download import download_all_regions, write_config


def main():
    write_config()
    download_all_regions()


if __name__ == "__main__":
    main()
