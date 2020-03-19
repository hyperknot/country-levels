import pathlib

lib_dir = pathlib.Path(__file__).parent.resolve()
root_dir = lib_dir.parent

data_dir = root_dir / 'data'
geojson_dir = data_dir / 'geojson'
fixes_dir = data_dir / 'fixes'
wikidata_dir = data_dir / 'wikidata'

export_dir = root_dir / 'export'

id_dir = export_dir / 'id'
id3_dir = id_dir / 'id3'

export_dir = export_dir / 'geojson'
export_id0_dir = export_dir / 'id0'
export_id1_dir = export_dir / 'id1'
export_id2_dir = export_dir / 'id2'
export_id3_dir = export_dir / 'id3'

docs_dir = root_dir / 'docs'
