from country_levels_lib.config import root_dir, id_dir, docs_dir, id3_dir
from country_levels_lib.utils import read_json, read_file, write_file


def generate_country_list():
    levels = read_json(id_dir / 'id012.json')
    code_list = '# Country list'

    for id0, id0_data in sorted(levels.items(), key=lambda item: item[1]['name']):
        name = id0_data['name']
        code = id0[4:].lower()

        code_list += (
            f'\n{name}   '
            f'[view](../export/geojson/medium/id0/{code}.geojson)   '
            f'code: **{id0}**   '
        )

        if (id3_dir / f'{code}.json').is_file():
            code_list += f'[states/counties](export/id/id3/{code}.json)'

        code_list += '\n\n'

        if 'sub1' not in id0_data:
            continue

        sub1 = id0_data['sub1']
        for id1, id1_data in sub1.items():
            name = id1_data['name']
            level = id1[:3]
            code = id1[4:].lower()

            code_list += (
                f'  - {name}   '
                f'[view](../export/geojson/medium/{level}/{code}.geojson)   '
                f'code: **{id1}**   '
                f'\n\n'
            )
            if 'sub2' not in id1_data:
                continue

            sub2 = id1_data['sub2']
            for id2, id2_data in sub2.items():
                name = id2_data['name']
                level = id2[:3]
                code = id2[4:].lower()

                code_list += (
                    f'  - {name}   '
                    f'[view](../export/geojson/medium/{level}/{code}.geojson)   '
                    f'code: **{id2}**   '
                    f'\n\n'
                )

    write_file(docs_dir / 'country_list.md', code_list)
    print(f'Readme updated')
