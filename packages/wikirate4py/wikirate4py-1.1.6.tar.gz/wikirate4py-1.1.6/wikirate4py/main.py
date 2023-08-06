from pprint import pprint

import requests

import wikirate4py

api = wikirate4py.API('ThessaloWikiRate',
                      wikirate_api_url="https://staging.wikirate.org",
                      auth=('wikirate', 'wikirat'))

metric = api.update_company(identifier=14540468, os_id='NH452365')

print(metric)

