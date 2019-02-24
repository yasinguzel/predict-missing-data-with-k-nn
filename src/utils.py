import pandas as pd
import random
from sklearn import preprocessing
import numpy


def read_csv_file():
    data = pd.read_csv('./dataset/ENB2012_data.csv', delimiter=';')
    return data


def normalize_dataset(dataset):
    array = dataset.values
    min_max_scalar = preprocessing.MinMaxScaler()
    scaled_array = min_max_scalar.fit_transform(array)
    dataset = pd.DataFrame(scaled_array)
    return dataset


def calculate_data_length(data_ratio, dataset_length, ratio):
    return int(data_ratio * dataset_length / ratio)


def save_data_frame_as_a_csv(data_frame, name):
    data_frame.to_csv('./results/{name}.csv'.format(name=name), sep=';')


def delete_cell_from_row_random(query_data):
    for index, row in query_data.iterrows():
        random_column = random.choice(list(query_data.columns.values))

        query_data.at[index, random_column] = numpy.nan
    print(query_data)
    return query_data
