import pathlib

lib_dir = pathlib.Path(__file__).parent.resolve()
root_dir = lib_dir.parent

data_dir = root_dir / 'data'
geojson_dir = data_dir / 'geojson'
levels_dir = data_dir / 'levels'
tmp_dir = data_dir / 'tmp'
fixes_dir = data_dir / 'fixes'

level3_dir = levels_dir / 'level3'
