#!/usr/bin/env python

import requests
import json
import time

ARCGIS_SERVER_URL = 'https://cartes.ville.sherbrooke.qc.ca/arcgis/rest/services/Utilitaires/Localisateur/MapServer/0/query?{}'
HEADERS = {
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US;en;q=0.8,fr;q=0.6',
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Referer': 'https://carte.ville.sherbrooke.qc.ca/infopropriete/',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}


def export_objects(begin=1, count=1, fields='*'):
    params = {
        'f': 'geojson',
        'objectIds': ','.join([str(i) for i in list(range(begin, begin + count))]),
        'outFields': fields,
        'returnGeometry': 'true',
    }

    url = ARCGIS_SERVER_URL.format('&'.join([k + "=" + params[k] for k in params]))

    result = do_query(url)

    return result


def do_query(endpoint, params={}):
    r = requests.get(endpoint, params=params, headers=HEADERS, timeout=1)

    if r.status_code != 200:
        raise Exception('http error code {} from {}'.format(r.status_code, r.url))

    return r.json()


def convert_values_to_numbers(feature):
    for key in ["VALEUR_TERRAIN", "VALEUR_BATIMENT", "VALEUR_PROPRIETE"]:
        if key in feature["properties"] and feature["properties"][key] not in ['', None]:
            feature["properties"][key] = float(feature["properties"][key])
    return feature



if __name__ == "__main__":
    print("Exporting object ids from Sherbrooke Arcgis server")

    step = 300
    output_file = 'output.geojson'

    with open(output_file, 'w') as f:
        f.write('{"type": "FeatureCollection", "features": [')

    i = 1
    while True:
        print('Fetching {} to {}'.format(i, i + step - 1))
        geojson = export_objects(i, step)

        if not geojson['features']:
            break

        features_converted = [convert_values_to_numbers(feature) for feature in geojson['features']]

        with open(output_file, 'a') as f:
            for feature in features_converted:
                json.dump(feature, f)
                f.write(',')

        i += step

    with open(output_file, 'rb+') as f:
        f.seek(-1, 2)
        f.truncate()

    with open(output_file, 'a') as f:
        f.write(']}')

    print("Done")
