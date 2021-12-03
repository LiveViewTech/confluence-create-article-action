from typing import Dict
from os import environ

import requests


workspace = environ.get('GITHUB_WORKSPACE')
if not workspace:
    raise Exception('No workspace is set')

envs: Dict[str, str] = {}
for key in ['parent', 'title', 'cloud', 'user', 'token']:
    value = environ.get(f'INPUT_{key.upper()}')
    if not value:
        raise Exception(f'Missing value for {key}')
    envs[key] = value

url = f"https://{envs['cloud']}.atlassian.net/wiki/rest/api/content"
content = {
    'type': 'page',
    'title': envs['title'],
    'body': {
        'editor': {
            'value': '',
            'representation': 'editor'
        }
    }
}

updated = requests.put(url, json=content, auth=(envs['user'], envs['token'])).json()
link = updated['_links']['base'] + updated['_links']['webui']

print(f'::set-output name=url::{link}')

print(f'Uploaded content successfully to page {link}')
