from src.utils import *

k = input('Enter value of k = ')

dataset = read_csv_file()

RATIO = 4
TRAIN_DATA_RATIO = 3
DATASET_LENGTH = len(dataset.index)

train_data_length = calculate_data_length(TRAIN_DATA_RATIO, DATASET_LENGTH, RATIO)

train_data = dataset[:train_data_length]

query_data = dataset[train_data_length:]