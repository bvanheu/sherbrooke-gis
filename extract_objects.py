#!/usr/bin/env python

import requests
import json
import time

ARCGIS_SERVER_URL = 'https://cartes.ville.sherbrooke.qc.ca/arcgis/rest/services/Utilitaires/Localisateur/MapServer/0/query?{}'
HEADERS = {
    'DNT' : '1',
    'Accept-Encoding' : 'gzip, deflate, sdch',
    'Accept-Language' : 'en-US;en;q=0.8,fr;q=0.6',
    'User-Agent' : 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
    'Content-Type' : 'application/x-www-form-urlencoded',
    'Accept' : '*/*',
    'Referer' : 'https://carte.ville.sherbrooke.qc.ca/infopropriete/',
    'X-Requested-With' : 'XMLHttpRequest',
    'Connection' : 'keep-alive',
}

def export_objects(begin=1, count=1, fields='*'):
    params = {
        'f': 'json',
        'objectIds': ','.join([str(i) for i in list(range(begin,begin+count))]),
        'outFields': fields,
        'returnGeometry': 'false',
    }

    url = ARCGIS_SERVER_URL.format( '&'.join([k+"="+params[k] for k in params]))

    result = do_query(url)

    return result

def do_query(endpoint, params={}):
    r = requests.get(endpoint, params=params, headers=HEADERS, timeout=1)

    if r.status_code != 200:
        raise Exception('http error code {} from {}'.format(r.status_code, r.url))

    return r.json()

if __name__ == "__main__":
    print("Exporting object ids from Sherbrooke Arcgis server")

    step = 300

    for i in range(1, 70000, step):
        print('{} / {}'.format(i, 70000))
        j = export_objects(i, step)

        #p['features'][0]['attributes']['OBJECTID']
        print(j)
        for i in j['features']:
            with open('./output/{}.json'.format(i['attributes']['OBJECTID']), 'w') as f:
                f.write(json.dumps(i['attributes']))
        time.sleep(1)

    print("Done")

