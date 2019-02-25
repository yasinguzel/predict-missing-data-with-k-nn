import math

from src.utils import *

# k = input('Enter value of k = ')

dataset = read_csv_file('./dataset/test.csv')

dataset = normalize_dataset(dataset)
save_data_frame_as_a_csv(dataset, 'normalized_data')

RATIO = 4
TRAIN_DATA_RATIO = 3
DATASET_LENGTH = len(dataset.index)

train_data_length = calculate_data_length(TRAIN_DATA_RATIO, DATASET_LENGTH, RATIO)
train_data = dataset[:train_data_length]

query_data = dataset[train_data_length:]
save_data_frame_as_a_csv(query_data, 'query_data')

missing_data = delete_cell_from_row_random(query_data)
save_data_frame_as_a_csv(missing_data, 'missing_data')

distances_list = [[]]
distance_df = pd.DataFrame()

for missing_data_row, missing_data_column in zip(*numpy.where(pd.isnull(missing_data))):

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
        distances_list.append([train_data_index, distance])

    distance_df = pd.DataFrame(distances_list, columns=['row', 'distance'])
    sorted_distance_df = distance_df.sort_values('distance')
    print(sorted_distance_df, '\n')
    distance_df.drop(distance_df.columns, axis=1)
    distances_list = [[]]
