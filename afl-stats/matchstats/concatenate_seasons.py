import json

all_results = json.load(open('data/raw/matchstats_2000_2009.json', 'r'))

for year in range(2010, 2022):
    season_results = json.load(open(f'data/raw/{year}matches.json', 'r'))
    all_results[str(year)] = season_results
    print(f'Done: {year}')

json.dump(all_results, open('data/matchstats.json', 'w'))