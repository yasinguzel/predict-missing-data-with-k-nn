import math
import numpy
import pandas as pd
from itertools import islice


def detect_missing_cells(data):
    missing_data_list = []
    for missing_data_row, missing_data_column in zip(*numpy.where(pd.isnull(data))):
        missing_data_list.append([missing_data_row, missing_data_column])

    return missing_data_list


def predict_missing_value(missing_cells, missing_data, train_data, dataset, k):
    distances_list = []
    for missing_data_row, missing_data_column in missing_cells:

        copy_missing_data = missing_data.copy()
        copy_missing_data.drop(missing_data.columns[missing_data_column], axis=1, inplace=True)

        copy_train_data = train_data.copy()
        copy_train_data.drop(missing_data.columns[missing_data_column], axis=1, inplace=True)

        for train_data_index, train_data_row in copy_train_data.iterrows():
            sum_one_point_distance = 0

            for train_data_cell, missing_data_cell in zip(train_data_row, copy_missing_data.iloc[missing_data_row]):
                one_point_distance = pow((train_data_cell - missing_data_cell), 2)
                sum_one_point_distance += one_point_distance

            distance = math.sqrt(sum_one_point_distance)
            distances_list.append([train_data_index, distance, train_data.iloc[train_data_index, missing_data_column]])

        find_missing_value_with_weight_voting(distances_list, k)
        distances_list.clear()


def find_missing_value_with_weight_voting(distances_list, k):
    distance_df = pd.DataFrame(distances_list, columns=['row', 'distance', 'value'])
    sorted_distance_df = distance_df.sort_values('distance')

    sum_distance = 0
    for distance_index, distance_row in islice(sorted_distance_df.iterrows(), int(k)):
        sum_distance += distance_row['value']

    print(sorted_distance_df)
