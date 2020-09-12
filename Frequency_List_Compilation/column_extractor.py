import numpy as np

def min_max_normalize(x, min, max):
    return round((float(x) - min) / (max - min), 4)

def extract_columns(matrix, second_col_idx, scale_min, scale_max):
    return np.column_stack((matrix[:, 0], np.array([value if scale_min is None else min_max_normalize(value, scale_min, scale_max) for value in matrix[:, second_col_idx]]).T))