import shutil

from country_levels_lib.config import geojson_dir, export_dir
from country_levels_lib.geo import calculate_centroid, find_timezone
from country_levels_lib.utils import read_json, write_json


def export_br_muni():
    for quality in [5, 7, 8]:
        process_br_muni_quality(quality)


def process_br_muni_quality(quality):
    assert quality in [5, 7, 8]

    print(f'Processing BR_Muni county GeoJSON {quality}')

    features = read_json(geojson_dir / 'br_muni' / 'simp' / f'simp-{quality}.geojson')['features']

    geojson_export_dir = export_dir / 'geojson' / f'q{quality}' / 'br_muni'
    shutil.rmtree(geojson_export_dir, ignore_errors=True)

    json_data = dict()

    for feature in features:
        prop = feature['properties']

        name = prop.pop('name')
        name_long = prop.pop('name_long')
        population = int(prop.pop('population'))
        state_code = prop.pop('state')
        ibge_code = prop.pop('ibge_code')

        assert not prop  # make sure we removed everything from the original properties

        countrylevel_id = f'br_muni:{ibge_code}'

        centroid = calculate_centroid(feature)
        timezone = find_timezone(centroid['lon'], centroid['lat'])

        new_prop = {
            'name': name,
            'name_long': name_long,
            'state_code': state_code,
            'state_code_iso': f'iso2:BR-{state_code}',
            'ibge_code': ibge_code,
            'population': population,
            'countrylevel_id': countrylevel_id,
            'center_lat': round(centroid['lat'], 2),
            'center_lon': round(centroid['lon'], 2),
            'timezone': timezone,
        }
        feature['properties'] = new_prop

        state_subdir = geojson_export_dir / state_code
        state_subdir.mkdir(parents=True, exist_ok=True)
        write_json(state_subdir / f'{ibge_code}.geojson', feature)

        json_data[ibge_code] = dict(new_prop)
        json_data[ibge_code]['geojson_path'] = f'br_muni/{state_code}/{ibge_code}.geojson'

    write_json(
        export_dir / 'geojson' / f'q{quality}' / 'br_muni_all.geojson',
        {"type": "FeatureCollection", "features": features},
    )

    if quality == 7:  # only write the file once
        write_json(export_dir / f'br_muni.json', json_data, indent=2, sort_keys=True)

    print(f'  {len(features)} GeoJSON processed')
