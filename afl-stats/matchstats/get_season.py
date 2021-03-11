import requests
from bs4 import BeautifulSoup
import json

afltables_url = "https://afltables.com/afl/"
season_url = afltables_url + "seas/2020.html"

season_page = requests.get(season_url)
season_soup = BeautifulSoup(season_page.content, 'html.parser')

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
    home_stats = [int(stat) for stat in stats[1:23]]
    home_stats = dict(zip(stat_headings, home_stats))
    home_stats['PTS'] = home_stats['GL']*6 + home_stats['BH']
    away_stats = [int(stat) for stat in stats[24:]]
    away_stats = dict(zip(stat_headings, away_stats))
    away_stats['PTS'] = away_stats['GL']*6 + away_stats['BH']

    return {teams[0]: home_stats, teams[1]: away_stats}
    print(team_stats)

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

all_results = {}
round_num = 1
table_tag = season_soup.find_all('table')
for i, line in enumerate(table_tag):
    round_str = line.text.split('Rnd')[0]
    if round_str == f'Round {round_num}':
        print(round_str)
        all_results[round_num] = get_round_matches(table_tag[i+2:i+11])
        round_num += 1

json.dump(all_results, open('data/2020matches.json', 'w'))