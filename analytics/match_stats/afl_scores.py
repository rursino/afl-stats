import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle, islice
from scipy import stats
from match_stats  import MatchStats


# Load match stats.
matchData = MatchStats()


years = [int(year) for year in matchData.data.keys()]
max_value = 0

fig = plt.figure(figsize=(20, 7))
color_set = ['orange', 'g', 'r', 'c', 'm', 'y', 'royalblue']
colors = list(islice(cycle(color_set), len(years)))

y_stats = []
for i, year in enumerate(years):
    year_data = matchData.get_season(year)
    
    # Normalise scores in 2020.
    if year == 2020:
        year_data['PTS'] *= 20 / 16
    
    x = year_data.index
    x = (x / len(x) - 0.5) / 1.5 + year
    y = year_data.PTS

    y_mean = y.mean()
    y_std = y.std()
    y_stats.append((y_mean, y_std))

    plt.scatter(x, y, color=colors[i])

    plt.scatter(year, y_mean, s=100, color='k')
    plt.errorbar(year, y_mean, yerr=y_std*1.645, color='k')

    # Extract maximum value from all years for plotting purposes.
    if y.max() > max_value:
        max_value = y.max()

plt.xticks(years)
for i, year in enumerate(years):
    plt.bar(year, max_value * 1.2, 1, alpha=0.2, color=colors[i]
    plt.text(year, max_value * 1.1, "{:.1f}".format(y_stats[i][0]), ha='center')

plt.text(years[0] + (years[-1] - years[0]) / 2, max_value * 1.15, "Mean", weight="bold", ha='center')

plt.xlim(years[0] - 0.5, years[-1] + 0.5)
plt.ylim([0, max_value * 1.2])

plt.show()

def determine_trend(x):
    return stats.linregress(years, x)

mean_scores = [mean for mean, _ in y_stats]
trend = determine_trend(mean_scores)
print(trend.pvalue)