from pprint import pprint

import requests

import wikirate4py

api = wikirate4py.API('ThessaloWikiRate')

metric = api.get_answer(id=14588427)

print(metric)

