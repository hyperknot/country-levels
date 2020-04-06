import shutil

from country_levels_lib.config import docs_dir
from country_levels_lib.ne.ne_012 import ne_id_dir, ne3_dir
from country_levels_lib.utils import read_json, write_file

md_space = '&nbsp;' * 5


def generate_country_list():
    levels = read_json(ne_id_dir / 'ne012.json')
    doc_md = '# Country list'

    for ne0, ne0_data in sorted(levels.items(), key=lambda item: item[1]['name']):
        name = ne0_data['name']
        code = ne0[4:].lower()

        doc_md += (
            f'\n{name}{md_space}'
            f'code: **{ne0}**{md_space}'
            f'[view](../export/geojson/medium/ne0/{code}.geojson){md_space}'
        )

        if (ne3_dir / f'{code}.json').is_file():
            doc_md += f'[states/provinces](country_list_ne3/{code}.md)'

        doc_md += '\n\n'

        if 'sub1' not in ne0_data:
            continue

        sub1 = ne0_data['sub1']
        for ne1, ne1_data in sorted(sub1.items(), key=lambda item: item[1]['name']):
            name = ne1_data['name']
            level = ne1[:3]
            code = ne1[4:].lower()

            doc_md += (
                f'  - {name}{md_space}'
                f'code: **{ne1}**{md_space}'
                f'[view](../export/geojson/medium/{level}/{code}.geojson){md_space} '
                f'\n\n'
            )
            if 'sub2' not in ne1_data:
                continue

            sub2 = ne1_data['sub2']
            for ne2, ne2_data in sorted(sub2.items(), key=lambda item: item[1]['name']):
                name = ne2_data['name']
                level = ne2[:3]
                code = ne2[4:].lower()

                doc_md += (
                    f'    - {name}{md_space}'
                    f'code: **{ne2}**{md_space}'
                    f'[view](../export/geojson/medium/{level}/{code}.geojson){md_space}'
                    f'\n\n'
                )

    write_file(docs_dir / 'country_list.md', doc_md)
    print(f'country_list.md updated')


def generate_ne3_lists():
    docs_ne3 = docs_dir / 'country_list_ne3'
    shutil.rmtree(docs_ne3, ignore_errors=True)
    docs_ne3.mkdir(parents=True)

    country_jsons = ne3_dir.glob('*.json')
    count = 0
    for country_json in country_jsons:
        country_code = country_json.stem
        generate_ne3_md(country_code)
        count += 1
    print(f'{count} country_list ne3.mds written')


def generate_ne3_md(country_iso):
    filename = f'{country_iso.lower()}.json'
    level3 = read_json(ne3_dir / filename)
    level012 = read_json(ne_id_dir / 'ne012.json')

    country_name = level012[f'ne0:{country_iso.upper()}']['name']

    doc_md = f'# {country_name} states/provinces/counties'

    for ne3, ne3_data in sorted(level3.items(), key=lambda item: item[1]['name']):
        name = ne3_data['name']
        ne3_country, ne3_state = ne3.split(':')[1].split('-')
        assert country_iso.lower() == ne3_country.lower()

        doc_md += (
            f'\n{name}{md_space}'
            f'code: **{ne3}**{md_space}'
            f'[view](../../export/geojson/medium/ne3/{country_iso.lower()}/{ne3_state.lower()}.geojson){md_space}'
            f'\n\n'
        )

    write_file(docs_dir / 'country_list_ne3' / f'{country_iso}.md', doc_md)
