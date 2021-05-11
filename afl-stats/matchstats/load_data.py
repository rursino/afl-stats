import os
import json

CURRENT_PATH = os.path.dirname(__file__)
fname = os.path.join(CURRENT_PATH, 'data/matchstats.json')

raw_data = json.load(open(fname, 'r'))
