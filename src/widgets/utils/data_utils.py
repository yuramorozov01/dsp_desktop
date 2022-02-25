from itertools import zip_longest

import numpy as np
import scipy.signal
import cv2


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


def normxcorr2(template, image, mode="full"):
    if np.ndim(template) > np.ndim(image) or \
            len([i for i in range(np.ndim(template)) if template.shape[i] > image.shape[i]]) > 0:
        print("normxcorr2: TEMPLATE larger than IMG. Arguments may be swapped.")

    template = template - np.mean(template)
    image = image - np.mean(image)

    a1 = np.ones(template.shape)

    ar = np.flipud(np.fliplr(template))
    out = scipy.signal.fftconvolve(image, ar.conj(), mode=mode)

    image = scipy.signal.fftconvolve(np.square(image), a1, mode=mode) - \
        np.square(scipy.signal.fftconvolve(image, a1, mode=mode)) / (np.prod(template.shape))

    image[np.where(image < 0)] = 0

    template = np.sum(np.square(template))
    out = out / np.sqrt(image * template)

    out[np.where(np.logical_not(np.isfinite(out)))] = 0

    return out


def normalize_image(image):
    normalized = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    normalized = normalized.astype(np.uint8)
    return normalized
