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
        'f': 'json',
        'objectIds': ','.join(map(str, range(begin, begin + count))),
        'outFields': fields,
        'returnGeometry': 'false',
    }

    url = ARCGIS_SERVER_URL.format('&'.join([f"{k}={params[k]}" for k in params]))

    return do_query(url)


def do_query(endpoint, params={}):
    r = requests.get(endpoint, params=params, headers=HEADERS, timeout=1)

    if r.status_code != 200:
        raise Exception(f'http error code {r.status_code} from {r.url}')

    return r.json()


def save_data_to_json_file(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def data_generator(start=1, step=300):
    counter = start

    while True:
        print(f'Processing IDs from {counter}')
        j = export_objects(counter, step)

        if not j['features']:
            break

        for item in j['features']:
            yield item['attributes']

        counter += step


if __name__ == "__main__":
    print("Exporting object ids from Sherbrooke Arcgis server")

    output_file = 'output.json'
    gen = data_generator()

    data = list(gen)
    save_data_to_json_file(data, output_file)

    print("Done")
