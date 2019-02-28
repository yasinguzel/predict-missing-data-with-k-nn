import math
import numpy
import pandas as pd
from itertools import islice


def detect_missing_cells(data):
    missing_data_list = []
    for missing_data_row, missing_data_column in zip(*numpy.where(pd.isnull(data))):
        missing_data_list.append([missing_data_row, missing_data_column])

    return missing_data_list


def predict_missing_value(missing_cells, missing_data, train_data, k):
    for missing_data_row, missing_data_column in missing_cells:

        copy_missing_data = missing_data.copy()
        copy_missing_data.drop(missing_data.columns[missing_data_column], axis=1, inplace=True)

        copy_train_data = train_data.copy()
        copy_train_data.drop(missing_data.columns[missing_data_column], axis=1, inplace=True)

        distances_list = []

        for train_data_index, train_data_row in copy_train_data.iterrows():
            sum_one_point_distance = 0

            for train_data_cell, missing_data_cell in zip(train_data_row, copy_missing_data.iloc[missing_data_row]):
                one_point_distance = pow((train_data_cell - missing_data_cell), 2)
                sum_one_point_distance += one_point_distance

            distance = math.sqrt(sum_one_point_distance)
            distances_list.append(
                [train_data_index, distance, train_data.iloc[train_data_index, missing_data_column],
                 calculate_weight(distance)])

        find_missing_value_with_weight_voting(distances_list, k)
        distances_list.clear()


def find_missing_value_with_weight_voting(distances_list, k):
    distance_df = pd.DataFrame(distances_list, columns=['row', 'distance', 'value', 'weight'])
    sorted_distance_df = distance_df.sort_values('distance')

    for distance_index, distance_row in islice(sorted_distance_df.iterrows(), k):
        for inner_distance_index, inner_distance_row in islice(sorted_distance_df.iterrows(), k):
            if distance_row['value'] == inner_distance_row['value']:
                sorted_distance_df.at[distance_index, 'weight'] = sorted_distance_df.at[distance_index, 'weight'] + \
                                                                  inner_distance_row[
                                                                      'weight']

    sorted_by_weight_df = sorted_distance_df.sort_values('weight')
    prediction = sorted_by_weight_df.tail(1)['value']
    print(prediction)


def calculate_weight(distance):
    weight = 1 / pow(distance, 2)
    return weight
