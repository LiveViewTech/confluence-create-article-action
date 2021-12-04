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
        'storage': {
            'value': '',
            'representation': 'storage'
        }
    }
}

search = requests.get('https://liveviewtech.atlassian.net/wiki/rest/api/content',
    params={'title': envs['title'], 'spaceKey': envs['space']},
    auth=(envs['user'], envs['token'])).json()
search_results = search['results']

article = None
if len(search_results) > 0:
    article = search_results[0]
    article['_links']['base'] = search['_links']['base']
else:
    article = requests.post(url, json=content, auth=(envs['user'], envs['token'])).json()

if article == None:
    raise Exception("Something went wrong...")

id = article['id']
link = article['_links']['base'] + article['_links']['webui']

print(f'::set-output name=id::{id}')
print(f'::set-output name=url::{link}')

print(f'Created new page: {link}')
