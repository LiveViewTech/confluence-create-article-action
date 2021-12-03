from typing import Dict
from os import environ

import requests


workspace = environ.get('GITHUB_WORKSPACE')
if not workspace:
    raise Exception('No workspace is set')

envs: Dict[str, str] = {}
for key in ['parent', 'space', 'title', 'cloud', 'user', 'token']:
    value = environ.get(f'INPUT_{key.upper()}')
    if not value:
        raise Exception(f'Missing value for {key}')
    envs[key] = value

url = f"https://{envs['cloud']}.atlassian.net/wiki/rest/api/content"
content = {
    'type': 'page',
    'title': envs['title'],
    'ancestors': [{
        'id': envs['parent']
    }],
    'space': {
        'key': envs['space']
    },
    'body': {
        'editor': {
            'value': '',
            'representation': 'editor'
        }
    }
}

created = requests.put(url, json=content, auth=(envs['user'], envs['token'])).json()
id = created['id']
link = created['_links']['base'] + created['_links']['webui']

print(f'::set-output name=id::{id}')
print(f'::set-output name=url::{link}')

print(f'Created new page: {link}')
