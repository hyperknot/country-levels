import shutil

from country_levels_lib.config import root_dir, id_dir, docs_dir, id3_dir
from country_levels_lib.utils import read_json, read_file, write_file


def generate_country_list():
    levels = read_json(id_dir / 'id012.json')
    doc_md = '# Country list'

    for id0, id0_data in sorted(levels.items(), key=lambda item: item[1]['name']):
        name = id0_data['name']
        code = id0[4:].lower()

        doc_md += (
            f'\n{name}     '
            f'code: **{id0}**     '
            f'[view](../export/geojson/medium/id0/{code}.geojson)     '
        )

        if (id3_dir / f'{code}.json').is_file():
            doc_md += f'[states/provinces](country_list_id3/{code}.md)'

        doc_md += '\n\n'

        if 'sub1' not in id0_data:
            continue

        sub1 = id0_data['sub1']
        for id1, id1_data in sorted(sub1.items(), key=lambda item: item[1]['name']):
            name = id1_data['name']
            level = id1[:3]
            code = id1[4:].lower()

            doc_md += (
                f'  - {name}     '
                f'code: **{id1}**     '
                f'[view](../export/geojson/medium/{level}/{code}.geojson)     '
                f'\n\n'
            )
            if 'sub2' not in id1_data:
                continue

            sub2 = id1_data['sub2']
            for id2, id2_data in sorted(sub2.items(), key=lambda item: item[1]['name']):
                name = id2_data['name']
                level = id2[:3]
                code = id2[4:].lower()

                doc_md += (
                    f'    - {name}     '
                    f'code: **{id2}**     '
                    f'[view](../export/geojson/medium/{level}/{code}.geojson)     '
                    f'\n\n'
                )

    write_file(docs_dir / 'country_list.md', doc_md)
    print(f'country_list.md updated')


def generate_id3_lists():
    docs_id3 = docs_dir / 'country_list_id3'
    shutil.rmtree(docs_id3, ignore_errors=True)
    docs_id3.mkdir(parents=True)

    country_jsons = id3_dir.glob('*.json')
    count = 0
    for country_json in country_jsons:
        country_code = country_json.stem
        generate_id3_md(country_code)
        count += 1
    print(f'{count} country_list id3.mds written')


def generate_id3_md(country_iso):
    filename = f'{country_iso.lower()}.json'
    level3 = read_json(id3_dir / filename)
    level012 = read_json(id_dir / 'id012.json')

    country_name = level012[f'id0:{country_iso.upper()}']['name']

    doc_md = f'# {country_name} states/provinces/counties'

    for id3, id3_data in sorted(level3.items(), key=lambda item: item[1]['name']):
        name = id3_data['name']
        id3_country, id3_state = id3.split(':')[1].split('-')
        assert country_iso.lower() == id3_country.lower()

        doc_md += (
            f'\n{name}     '
            f'code: **{id3}**     '
            f'[view](../export/geojson/medium/id3/{country_iso.lower()}/{id3_state.lower()}.geojson)     '
            f'\n\n'
        )

    write_file(docs_dir / 'country_list_id3' / f'{country_iso}.md', doc_md)
