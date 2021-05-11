import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from load_data import raw_data
from get_season import get_season, get_seasons

plt_indices = 0

for year in range(2000, 2021):
    year_data = get_season(raw_data, year)

    # Normalise scores in 2020.
    if year == 2020:
        year_data['PTS'] *= 1.25
    
    plt.scatter(year_data.index + plt_indices, year_data.PTS)

    plt_indices += 400

plt.show()