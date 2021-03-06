"""Scrape seasons of match statistics from AFL Tables.
Script expects the following cmd line inputs:
    start_year end_year
    OR
    year
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
import os

CURRENT_PATH = os.path.dirname(__file__)

out_fname = 'matchstats_'
if len(sys.argv) == 2:
    year = int(sys.argv[1])
    years = [year]
    out_fname += str(year)
else:
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2]) + 1
    years = range(start_year, end_year)
    out_fname += f'{start_year}_{(end_year-1)}'


def get_match_stats(stat_url):
    stat_page = requests.get(stat_url)
    stat_soup = BeautifulSoup(stat_page.content, 'html.parser')

    teams = stat_soup.title.text.split(' - ')[1].split(' v ')

    b_tag = stat_soup.find_all('b')
    for i, line in enumerate(b_tag):
        if line.text == 'Totals':
            start_index = i
            break
    stats = stat_soup.find_all('b')[i:i+45]
    stats = [line.text for line in stats]

    stat_headings = ['KI', 'MK', 'HB', 'DI', 'GL', 'BH', 'HO', 'TK', 'RB', 'IF', 'CL', 'CG', 'FF', 'FA']

    totals_index = []
    for i, e in enumerate(stats):
        if e == "Totals":
            totals_index.append(i)
    
    home_stats = stats[totals_index[0]+1:totals_index[1]]
    if len(totals_index) == 3:
        away_stats = stats[totals_index[1]+1:totals_index[2]]
    else:
        away_stats = stats[totals_index[1]+1:]

    home_stats = [int(stat) for stat in home_stats]
    home_stats = dict(zip(stat_headings, home_stats))
    home_stats['PTS'] = home_stats['GL']*6 + home_stats['BH']
    away_stats = [int(stat) for stat in away_stats]
    away_stats = dict(zip(stat_headings, away_stats))
    away_stats['PTS'] = away_stats['GL']*6 + away_stats['BH']

    return {teams[0]: home_stats, teams[1]: away_stats}

def get_round_matches(result_tag):
    round_matches = []
    for match_num, match_result in enumerate(result_tag):
        match_result = match_result.find_all('td')
        if len(match_result) == 8:
            stat_url = afltables_url + match_result[7].find('a')['href'][3:]
            print(match_num+1)
            match_stats = get_match_stats(stat_url)
            round_matches.append(match_stats)

    return round_matches


afltables_url = "https://afltables.com/afl/"
all_results = {}
for year in years:
    print(year)

    season_url = afltables_url + f"seas/{year}.html"
    season_page = requests.get(season_url)
    season_soup = BeautifulSoup(season_page.content, 'html.parser')

    year_results = {}
    round_num = 1
    table_tag = season_soup.find_all('table')
    for i, line in enumerate(table_tag):
        round_str = line.text.split('Rnd')[0]
        if round_str == f'Round {round_num}':
            print(round_str)
            try:
                year_results[round_num] = get_round_matches(table_tag[i+2:i+11])
                round_num += 1
            except TypeError:
                break
    all_results[year] = year_results


fname = os.path.join(CURRENT_PATH, f'raw/{out_fname}.json')
json.dump(all_results, open(fname, 'w'))
