import pandas as pd
import numpy as np
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression

from load_data import raw_data
from get_season import get_season, get_seasons

import json
import os


# Read in raw data.
CURRENT_PATH = os.path.dirname(__file__)
fname = os.path.join(CURRENT_PATH, 'data/matchstats.json')
raw_data = json.load(open(fname, 'r'))


# Linear regression model
def linreg_model(df_train, df_forecast, forecast_col='PTS', test_size=0.2):

    # Drop collinear/repeated variables
    columns_to_drop = ['DI', 'GL', 'BH', 'FA']
    df_train = df_train.drop(columns_to_drop, 1)
    df_forecast = df_forecast.drop(columns_to_drop, 1)

    # Generate features and label.
    X = np.array(df_train.drop([forecast_col], 1))
    y = np.array(df_train[forecast_col])

    # Split data into train and test components.
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=test_size)

    # Linear regression model.
    clf = LinearRegression()
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)

    X_lately = np.array(df_forecast.drop([forecast_col], 1))
    forecast_set = clf.predict(X_lately)
    
    return clf, accuracy, forecast_set, df_train.columns


df_train = get_seasons(raw_data, 2000, 2020)
df_forecast = get_season(raw_data, 2021)

clf, accuracy, forecast_set, columns_used = linreg_model(df_train, df_forecast)

print('Accuracy: ', np.round(accuracy, 3), '\n')

error = df_forecast['PTS'].values - forecast_set
print('Error array: ', np.round(error))
print('Mean: ', error.mean())
print('STD: ', error.std())
print('Min: ', np.round(error.min()))
print('Max: ', np.round(error.max()))

mse = np.sum(error**2) / len(error)
print('MSE: ', np.round(mse, 2))
