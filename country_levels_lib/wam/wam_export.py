import shutil

from country_levels_lib.fips import fips_utils
from country_levels_lib.config import geojson_dir, export_dir, fixes_dir
from country_levels_lib.geo import calculate_centroid, find_timezone
from country_levels_lib.utils import read_json, osm_url, write_json, wikidata_url
from country_levels_lib.wam.wam_collect import validate_iso1, validate_iso2
from country_levels_lib.wam.wam_download import wam_data_dir

wam_geojson_simp_dir = geojson_dir / 'wam' / 'simp'

population_map = None
population_fixes = read_json(fixes_dir / 'population.json')
skip_osm_features = {int(i) for i in read_json(fixes_dir / 'skip_osm.json')}
us_states_by_postal = fips_utils.get_state_data()[1]


def split_geojson(iso_level: int, simp_level):
    assert iso_level in [1, 2]

    global population_map
    if not population_map:
        population_map = read_json(wam_data_dir / 'population.json')

    print(f'Splitting iso{iso_level} to level: q{simp_level}')
    file_path = wam_geojson_simp_dir / f'iso{iso_level}-{simp_level}.geojson'

    features = read_json(file_path)['features']
    features_sorted = sorted(features, key=lambda i: i['properties']['admin_level'])

    features_by_iso = dict()

    for feature in features_sorted:
        feature_processed = process_feature_properties(feature, iso_level)
        feature_clean = feature_processed['feature']
        osm_id = feature_clean['properties']['osm_id']
        if osm_id in skip_osm_features:
            print(f'  skipping osm_id: {osm_id}')
            continue

        iso = feature_processed['iso']
        if iso_level == 1:
            if not validate_iso1(iso):
                print(f'invalid iso1: {iso}')
                continue
        else:
            if not validate_iso2(iso):
                print(f'invalid iso2: {iso}')
                continue

        features_by_iso.setdefault(iso, list())
        features_by_iso[iso].append(feature_clean)

    deduplicated_by_iso = deduplicate_features_by_iso(features_by_iso)
    write_json_and_geojsons(deduplicated_by_iso, iso_level, simp_level)


def process_feature_properties(feature: dict, iso_level: int):
    assert iso_level in [1, 2]

    prop = feature['properties']
    alltags = prop['alltags']

    name = prop.pop('name')
    osm_id = int(prop.pop('id'))
    iso = prop.pop(f'iso{iso_level}')

    centroid = calculate_centroid(feature)

    admin_level = int(prop.pop('admin_level'))
    wikidata_id = prop.pop('wikidata_id', None)
    countrylevel_id = f'iso{iso_level}:{iso}'
    population = population_map.get(wikidata_id)
    if countrylevel_id in population_fixes:
        if population:
            print(f'Population not needed anymore in fixes: {countrylevel_id}')
        population = population_fixes[countrylevel_id]

    timezone = alltags.pop('timezone', None)
    if not timezone:
        timezone = find_timezone(centroid['lon'], centroid['lat'])
        if not timezone:
            print(f'missing timezone for ${iso} ${name} ${timezone}')

    # override population for US states from Census data
    if iso.startswith('US-'):
        postal_code = iso[3:]
        state_data = us_states_by_postal.get(postal_code, {})
        population_from_census = state_data.get('population')
        if population_from_census is not None:
            population = population_from_census

    wikipedia_from_prop = prop.pop('wikipedia', None)
    wikipedia_from_alltags = alltags.pop('wikipedia', None)
    if (
        wikipedia_from_prop
        and wikipedia_from_alltags
        and wikipedia_from_prop != wikipedia_from_alltags
    ):
        print(wikipedia_from_prop, wikipedia_from_alltags)
    wikipedia_id = wikipedia_from_alltags
    if wikipedia_from_prop:
        wikipedia_id = wikipedia_from_prop

    feature.pop('bbox', None)

    for key in ['boundary', 'note', 'rpath', 'srid', 'timestamp']:
        prop.pop(key, None)

    for key in [
        'ISO3166-1',
        'ISO3166-1:alpha2',
        'ISO3166-1:numeric',
        'ISO3166-2',
        'ISO3166-2:alpha2',
        'ISO3166-2:numeric',
        'land_area',
        'wikidata',
    ]:
        alltags.pop(key, None)

    new_prop = {
        'name': name,
        f'iso{iso_level}': iso,
        'admin_level': admin_level,
        'osm_id': osm_id,
        'countrylevel_id': countrylevel_id,
        'osm_data': prop,
        'center_lat': round(centroid['lat'], 2),
        'center_lon': round(centroid['lon'], 2),
    }

    if timezone:
        new_prop['timezone'] = timezone

    if population:
        new_prop['population'] = population

    if wikidata_id:
        new_prop['wikidata_id'] = wikidata_id

    if wikipedia_id:
        new_prop['wikipedia_id'] = wikipedia_id

    feature['properties'] = new_prop

    return {
        'feature': feature,
        'iso': iso,
    }


def deduplicate_features_by_iso(features_by_iso: dict):
    deduplicated = {}
    for iso, features in features_by_iso.items():
        if len(features) == 1:
            deduplicated[iso] = features[0]
        else:
            print(f'  duplicate features for: {iso}')
            for feature in features:
                prop = feature['properties']
                name = prop['name']
                admin_level = prop['admin_level']
                osm_id = prop['osm_id']
                population = prop.get('population')
                wikidata_id = prop.get('wikidata_id')

                print(
                    f'    {name} '
                    f'admin_level: {admin_level}  '
                    f'population: {population}  '
                    f'{osm_url(osm_id)} '
                    f'{wikidata_url(wikidata_id)}  '
                )

            # pick the first one by admin_level
            features_sorted = sorted(features, key=lambda k: k['properties']['admin_level'])
            deduplicated[iso] = features_sorted[0]
            print()
    return deduplicated


def write_json_and_geojsons(deduplicated_by_iso: dict, iso_level: int, simp_level: int):
    assert iso_level in [1, 2]

    level_subdir = export_dir / 'geojson' / f'q{simp_level}' / f'iso{iso_level}'
    shutil.rmtree(level_subdir, ignore_errors=True)
    level_subdir.mkdir(parents=True)

    json_data = {}
    for iso, feature in deduplicated_by_iso.items():
        new_prop_without_osm_data = {
            k: v for k, v in feature['properties'].items() if k != 'osm_data'
        }
        json_data[iso] = new_prop_without_osm_data

        if iso_level == 1:
            write_json(level_subdir / f'{iso}.geojson', feature)
            json_data[iso]['geojson_path'] = f'iso1/{iso}.geojson'

        else:
            iso2_start, iso2_end = iso.split('-')

            iso2_subdir = level_subdir / iso2_start
            iso2_subdir.mkdir(exist_ok=True)

            write_json(level_subdir / iso2_start / f'{iso}.geojson', feature)
            json_data[iso]['geojson_path'] = f'iso2/{iso2_start}/{iso}.geojson'

    if simp_level == 5:
        write_json(export_dir / f'iso{iso_level}.json', json_data, indent=2, sort_keys=True)
