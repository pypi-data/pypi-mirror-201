import pickle
import json
import pandas as pd


def read_csv(file_path, sep=',', column_names=None, use_cols=None, squeeze=False):
    return pd.read_csv(file_path, sep=sep, header=None, names=column_names, usecols=use_cols, squeeze=squeeze)


def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def read_pickle(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)


def test_read():
    print("je sais lire")



