import pandas as pd


def read_csv_file():
    data = pd.read_csv('./dataset/ENB2012_data.csv', delimiter=';')
    return data


def calculate_data_length(data_ratio, dataset_length, ratio):
    return int(data_ratio * dataset_length / ratio)
