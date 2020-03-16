import pathlib

lib_dir = pathlib.Path(__file__).parent.resolve()
root_dir = lib_dir.parent

data_dir = root_dir / 'data'

geojson_dir = data_dir / 'geojson'
fixes_dir = data_dir / 'fixes'

levels_dir = data_dir / 'levels'
level_3_dir = levels_dir / 'level_3'

export_dir = data_dir / 'export'
export_0_dir = export_dir / 'level_0'
export_1_dir = export_dir / 'level_1'
export_2_dir = export_dir / 'level_2'
export_3_dir = export_dir / 'level_3'
