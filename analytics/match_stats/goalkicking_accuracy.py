import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle, islice
from scipy import stats

from match_stats import MatchStats


# Load match stats.
matchData = MatchStats()


years = [int(year) for year in matchData.data.keys()]
min_value, max_value = 0, 0

fig = plt.figure(figsize=(20, 7))
color_set = ['orange', 'g', 'r', 'c', 'm', 'y', 'royalblue']
colors = list(islice(cycle(color_set), len(years)))

for i, year in enumerate(years):
    year_data = matchData.get_season(year)

    # Normalise scores in 2020.
    if year == 2020:
        year_data *= 20 / 16
    
    x = year_data.index
    x = (x / len(x) - 0.5) / 1.5 + year
    y = (year_data['GL'] / year_data['BH'] - 1) * 100

    plt.scatter(x, y, color=colors[i])

    # Extract minimum and maximum value from all years for plotting purposes.
    if y.min() < min_value:
        min_value = y.min()
    if y.max() > max_value:
        max_value = y.max()

plt.xticks(years)

window_min = min_value * (1.2 ** -np.sign(min_value))
window_max = max_value * (1.3 ** np.sign(max_value))
plt.xlim(years[0] - 0.5, years[-1] + 0.5)
plt.ylim([window_min, window_max])

for i, year in enumerate(years):
    plt.bar(year, (window_min, window_max), 1, alpha=0.2, color=colors[i])


# Extra bits

y_stats = []
for i, year in enumerate(years):
    y_mean = y.mean()
    y_std = y.std()
    y_stats.append((y_mean, y_std))

    plt.scatter(year, y_mean, s=100, color='k')
    plt.errorbar(year, y_mean, yerr=y_std*1.645, color='k')


for i, year in enumerate(years):
    plt.text(year, max_value * 1.15, "{:.1f}".format(y_stats[i][0]), ha='center')

plt.text(years[0] + (years[-1] - years[0]) / 2, max_value * 1.22, "Mean", weight="bold", ha='center')

plt.axhline(0, color='k')



plt.show()
