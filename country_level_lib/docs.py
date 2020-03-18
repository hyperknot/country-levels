from country_level_lib.config import root_dir, id_dir
from country_level_lib.utils import read_json, read_file, write_file


def generate_readme():
    levels = read_json(id_dir / 'id012.json')
    document = ''

    for id0, id0_data in levels.items():
        name = id0_data['name']
        code = id0[4:].lower()

        document += (
            f'- **{id0}** [{name}](export/geojson/id0/{code}.geojson)'
            f'      '
            f'[id3 list](export/id/id3/{code}.json)'
            f'\n'
        )
        # print(id0, id0_data)
        if 'sub1' not in id0_data:
            continue

        sub1 = id0_data['sub1']
        for id1, id1_data in sub1.items():
            print('  ', id1, id1_data)
            if 'sub2' not in id1_data:
                continue

            sub2 = id1_data['sub2']
            for id2, id2_data in sub2.items():
                print('   ', id2, id2_data)

    readme_template = read_file(root_dir / 'README_template.md')
    readme_replaced = readme_template.replace('___REPLACE_TEMPLATE___', document)
    write_file(root_dir / 'README.md', readme_replaced)

    print(f'Readme updated')
