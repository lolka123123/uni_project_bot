import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LANG_PATH = os.path.join(BASE_DIR, 'languages', 'english.json')

with open(LANG_PATH, encoding='UTF8') as file:
    json_file = json.load(file)


def get_translate(key):
    try:
        return json_file[key]
    except KeyError:
        return '□'

