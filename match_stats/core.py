import pandas as pd
import numpy as np
import os
import json


CURRENT_PATH = os.path.dirname(__file__)


class MatchStats:
    """ Retrieve match stats from the matchstats.json file.
    """

    def __init__(self):
        """Retrive match stats and initialise an instance of the MatchStats class.
        """

        fname = os.path.join(CURRENT_PATH, 'data/matchstats.json')
        data = json.load(open(fname, 'r'))

        self.data = data

    def get_season(self, year):
        """Get data for any season and parse it.

        Args:
            year (int or str): Year chosen.

        Returns:
            pd.DataFrame: Dataframe of parsed data.
        """

        data = self.data[str(year)]

        aggdata = {}
        i = 0
        for round_num in data:
            for match in data[round_num]:
                aggdata[i] = pd.DataFrame(match).sum(axis=1)
                i += 1

        return pd.DataFrame(aggdata).T

    def get_seasons(self, start_year, end_year):
        """Get data for a range of seasons, parse each season, and concatenate it all into one dataframe.

        Args:
            start_year (int or str): First year chosen.
            end_year (int or str): Last year chosen.

        Returns:
            pd.DataFrame: Dataframe of parsed data.
        """

        data = self.data

        return pd.concat([self.get_season(str(year)) for year in range(int(start_year), int(end_year)+1)], ignore_index=True)    
