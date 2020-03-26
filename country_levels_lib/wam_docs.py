import shutil

from country_levels_lib.config import export_dir, docs_dir
from country_levels_lib.utils import read_json, write_file, osm_url, wikidata_url, wikipedia_url


def generate_iso1_list():
    iso1_json = read_json(export_dir / 'iso1.json')

    doc_md = (
        '# ISO 3166-1 list\n'
        'Name | ISO1 | ISO2 | GeoJSON | OSM | Wikidata | Wikipedia | population \n'
        '--- | --- | --- | --- | --- | --- | --- | --- \n'
    )

    for item in sorted(iso1_json.values(), key=lambda k: k['name']):
        data = build_row_data(item)

        iso1 = item['iso1']
        geojson_link = f'[GeoJSON](../export/geojson/q7/iso1/{iso1.upper()}.geojson)'

        iso_2_link = f'[ISO2](iso2_list/{iso1.upper()}.md)'

        doc_md += (
            f'{data["name"]} | {iso1} | {iso_2_link} | {geojson_link} | '
            f'{data["osm_link"]} | {data["wikidata_link"]} | '
            f'{data["wikipedia_link"]} | {data["population"]}'
            f'\n'
        )

    write_file(docs_dir / 'iso1_list.md', doc_md)


def generate_iso2_list():
    iso2_json = read_json(export_dir / 'iso2.json')
    country_codes = {i.split('-')[0] for i in iso2_json}

    subdir = docs_dir / 'iso2_list'
    shutil.rmtree(subdir, ignore_errors=True)
    subdir.mkdir(parents=True)

    for country_code in sorted(country_codes):
        generate_iso2_list_country(country_code)


def generate_iso2_list_country(iso1):
    iso2_json = read_json(export_dir / 'iso2.json')
    iso2_filtered = [i for i in iso2_json.values() if i['iso2'].split('-')[0] == iso1]

    doc_md = f'# ISO 3166-2 list: {iso1.upper()}\n'

    iso2_by_level = {}
    for item in sorted(iso2_filtered, key=lambda k: k['admin_level']):
        level = item['admin_level']
        iso2_by_level.setdefault(level, [])
        iso2_by_level[level].append(item)

    for level, level_items in iso2_by_level.items():
        doc_md += f'\n\n#### Level {level}\n'
        doc_md += (
            'Name | ISO2 | GeoJSON | OSM | Wikidata | Wikipedia | population \n'
            '--- | --- | --- | --- | --- | --- | --- \n'
        )

        for item in sorted(level_items, key=lambda k: k['name']):
            data = build_row_data(item)

            iso2 = item['iso2']
            geojson_link = (
                f'[GeoJSON](../../export/geojson/q7/iso2/{iso1.upper()}/{iso2.upper()}.geojson)'
            )

            doc_md += (
                f'{data["name"]} | {iso2} | {geojson_link} | '
                f'{data["osm_link"]} | {data["wikidata_link"]} | '
                f'{data["wikipedia_link"]} | {data["population"]}'
                f'\n'
            )

    write_file(docs_dir / 'iso2_list' / f'{iso1.upper()}.md', doc_md)


def build_row_data(item):
    name = item['name']
    osm_id = item['osm_id']
    countrylevel_id = item['countrylevel_id']
    population = item.get('population') or ''

    wikidata_id = item.get('wikidata_id')
    wikipedia_id = item.get('wikipedia_id')

    osm_link = f'[OSM]({osm_url(osm_id)})'

    wikidata_link = ''
    if wikidata_id:
        wikidata_link = f'[Wikidata]({wikidata_url(wikidata_id)})'

    wikipedia_link = ''
    if wikipedia_id:
        wikipedia_link = f'[Wikipedia]({wikipedia_url(wikipedia_id)})'

    return {
        'name': name,
        'osm_link': osm_link,
        'countrylevel_id': countrylevel_id,
        'population': population,
        'wikidata_link': wikidata_link,
        'wikipedia_link': wikipedia_link,
    }
