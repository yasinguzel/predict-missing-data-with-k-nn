from src.knn import *
from src.utils import *

k = int(input('Enter value of k = '))

dataset = read_csv_file('./dataset/ENB2012_data.csv')

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

missing_cells = detect_missing_cells(missing_data)

predict_missing_value(missing_cells, missing_data, train_data, k)
