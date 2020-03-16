import pathlib

lib_dir = pathlib.Path(__file__).parent.resolve()
root_dir = lib_dir.parent

data_dir = root_dir / 'data'

geojson_dir = data_dir / 'geojson'
fixes_dir = data_dir / 'fixes'
export_dir = data_dir / 'export'

levels_dir = data_dir / 'levels'
level_3_dir = levels_dir / 'level_3'
