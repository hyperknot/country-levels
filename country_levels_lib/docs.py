from country_levels_lib.config import root_dir, id_dir, docs_dir, id3_dir
from country_levels_lib.utils import read_json, read_file, write_file


def generate_readme():
    levels = read_json(id_dir / 'id012.json')
    tree_md = ''

    for id0, id0_data in levels.items():
        name = id0_data['name']
        code = id0[4:].lower()

        tree_md += f'\n**{id0}** [{name}](export/geojson/id0/{code}.geojson)'

        if (id3_dir / f'{code}.json').is_file():
            tree_md += f' *([id3](export/id/id3/{code}.json))*'

        tree_md += '\n\n'

        if 'sub1' not in id0_data:
            continue

        sub1 = id0_data['sub1']
        for id1, id1_data in sub1.items():
            name = id1_data['name']
            level = id1[:3]
            code = id1[4:].lower()

            tree_md += f'  - **{id1}** [{name}](export/geojson/{level}/{code}.geojson)\n\n'
            if 'sub2' not in id1_data:
                continue

            sub2 = id1_data['sub2']
            for id2, id2_data in sub2.items():
                name = id2_data['name']
                level = id2[:3]
                code = id2[4:].lower()

                tree_md += f'    - **{id2}** [{name}](export/geojson/{level}/{code}.geojson)\n\n'

    readme_template = read_file(docs_dir / 'README_template.md')
    readme_replaced = readme_template.replace('___REPLACE_TEMPLATE___', tree_md)
    write_file(root_dir / 'README.md', readme_replaced)

    print(f'Readme updated')
