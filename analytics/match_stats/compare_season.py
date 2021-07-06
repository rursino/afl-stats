import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle, islice

from match_stats import MatchStats


# Load match stats.
matchData = MatchStats()


def compare_season(df, y):

    years = [int(year) for year in df.data.keys()]

    min_value, max_value = 0, 0

    fig = plt.figure(figsize=(20, 7))
    color_set = ['orange', 'g', 'r', 'c', 'm', 'y', 'royalblue']
    colors = list(islice(cycle(color_set), len(years)))

    for i, year in enumerate(years):
        season = df.get_season(year)

        # Normalise scores in 2020.
        if year == 2020:
            season *= 20 / 16
        
        x = season.index
        x = (x / len(x) - 0.5) / 1.5 + year
        # y = (season['GL'] / season['BH'] - 1) * 100

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

    plt.show()

y = (season['GL'] / season['BH'] - 1) * 100
compare_season(matchData, y)