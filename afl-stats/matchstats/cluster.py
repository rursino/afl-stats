import json
import sklearn
import pandas as pd
import numpy as np

data = json.load(open('data/2020matches.json', 'r'))

aggdata = {}

i = 0
for round_num in data:
    for match in data[round_num]:
        aggdata[i] = pd.DataFrame(match).sum(axis=1)
        i += 1

all_stats = pd.DataFrame(aggdata).T
print(all_stats)