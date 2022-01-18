from itertools import zip_longest

import numpy as np


def get_save_data_from_lineedit(lineedit, value_type=int):
    try:
        value_type = value_type(lineedit.text())
        return value_type
    except ValueError:
        return value_type()


def get_save_data_array_from_lineedit(lineedit, delimiter=' ', value_type=int):
    try:
        values_type = [value_type(item) for item in lineedit.text().split(delimiter)]
        return values_type
    except ValueError:
        return [value_type()]


def equalize_length_of_arrays(fill_value, *args):
    return tuple(zip(*zip_longest(*args, fillvalue=fill_value)))


def generate_polyharmonic_signal(amount_of_points, amplitudes, frequencies):
    time = np.arange(0, amount_of_points, 1)

    harmonics_values = []
    for i in range(len(amplitudes)):
        harmonics_values.append(amplitudes[i] * np.sin(2 * np.pi * frequencies[i] * time / len(time)))

    result_values = []
    for j in time:
        res = 0
        for harmonic_values in harmonics_values:
            res += harmonic_values[j]
        result_values.append(res)

    return time, result_values, harmonics_values
