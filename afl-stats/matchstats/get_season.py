import pandas as pd
import numpy as np


def get_season(data, year):
    """Get data for any season and parse it.

    Args:
        data (json): Raw data in JSON object format.
        year (int or str): Year chosen.

    Returns:
        pd.DataFrame: Dataframe of parsed data.
    """

    data = data[str(year)]

    aggdata = {}
    i = 0
    for round_num in data:
        for match in data[round_num]:
            aggdata[i] = pd.DataFrame(match).sum(axis=1)
            i += 1

    return pd.DataFrame(aggdata).T

def get_seasons(data, start_year, end_year):
    """Get data for a range of seasons, parse each season, and concatenate it all into one dataframe.

    Args:
        data (json): Raw data in JSON object format.
        start_year (int or str): First year chosen.
        end_year (int or str): Last year chosen.

    Returns:
        pd.DataFrame: Dataframe of parsed data.
    """

    return pd.concat([get_season(data, str(year)) for year in range(int(start_year), int(end_year)+1)], ignore_index=True)    
