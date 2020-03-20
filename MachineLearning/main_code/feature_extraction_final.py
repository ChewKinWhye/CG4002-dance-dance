from spectrum import aryule
from scipy.stats import pearsonr
from scipy.stats import entropy
from math import sqrt
from numpy.fft import fft, fftfreq

import pandas as pd
import statistics
import numpy as np


def obtain_min(data):
    return np.min(data)


def obtain_max(data):
    return np.max(data)


def obtain_mean(data):
    return statistics.mean(data)


def obtain_std(data):
    return statistics.stdev(data)


def obtain_ar_coefficients(data, burg_order):
    ar, _, _ = aryule(data, order=burg_order)
    return ar


def obtain_correlation_coefficient(data1, data2):
    corr, _ = pearsonr(data1, data2)
    return corr


def fourier_transform(data):
    return np.fft.fft(data)


# Signal magnitude area
def obtain_sma(data_x, data_y, data_z):
    sma = 0
    for i in range(len(data_x)):
        sma += abs(data_x[i]) + abs(data_y[i]) + abs(data_z[i])
    return sma


def obtain_band_energy(data, start, end):
    energy = 0
    for i in range(start-1, end):
        energy += pow(data[i], 2)
    return energy


def obtain_entropy(data):
    data = pd.Series(data)
    p_data = data.value_counts()           # counts occurrence of each value
    entropy_value = entropy(p_data)  # get entropy from counts
    return entropy_value


def obtain_max_index(data):
    return np.argmax(data)


def obtain_skewness(data):
    data = pd.DataFrame(data)
    return float(data.skew())


def obtain_magnitude(data_x, data_y, data_z):
    data_magnitude = []
    for i in range(0, len(data_x)):
        magnitude = sqrt(pow(data_x[i], 2) + pow(data_y[i], 2) + pow(data_z[i], 2))
        data_magnitude.append(magnitude)
    return np.asarray(data_magnitude)


def extract_features_t_body_acc(acc_x, acc_y, acc_z):
    features = []
    features.append(obtain_min(acc_x))
    features.append(obtain_min(acc_y))
    features.append(obtain_min(acc_z))

    features.append(obtain_max(acc_x))
    features.append(obtain_max(acc_y))
    features.append(obtain_max(acc_z))

    features.append(obtain_mean(acc_x))
    features.append(obtain_mean(acc_y))
    features.append(obtain_mean(acc_z))

    features.append(obtain_std(acc_x))
    features.append(obtain_std(acc_y))
    features.append(obtain_std(acc_z))

    features.extend(obtain_ar_coefficients(acc_x, 4))
    features.extend(obtain_ar_coefficients(acc_y, 4))
    features.extend(obtain_ar_coefficients(acc_z, 4))

    features.append(obtain_correlation_coefficient(acc_x, acc_y))
    features.append(obtain_correlation_coefficient(acc_z, acc_y))
    features.append(obtain_correlation_coefficient(acc_x, acc_z))
    return features


def extract_features_t_body_acc_mag(acc_mag):
    features = []
    features.append(obtain_min(acc_mag))
    features.append(obtain_max(acc_mag))
    features.append(obtain_mean(acc_mag))
    features.append(obtain_std(acc_mag))
    features.extend(obtain_ar_coefficients(acc_mag, 4))
    return features


def extract_features_f_body_acc(f_body_acc_x, f_body_acc_y, f_body_acc_z):
    freqs = fftfreq(len(f_body_acc_x))
    mask = freqs >= 0
    f_body_acc_x = 2 * f_body_acc_x[mask]
    f_body_acc_y = 2 * f_body_acc_y[mask]
    f_body_acc_z = 2 * f_body_acc_z[mask]
    features = []
    features.append(obtain_min(f_body_acc_x))
    features.append(obtain_min(f_body_acc_y))
    features.append(obtain_min(f_body_acc_z))

    features.append(obtain_max(f_body_acc_x))
    features.append(obtain_max(f_body_acc_y))
    features.append(obtain_max(f_body_acc_z))

    features.append(obtain_mean(f_body_acc_x))
    features.append(obtain_mean(f_body_acc_y))
    features.append(obtain_mean(f_body_acc_z))

    features.append(obtain_std(f_body_acc_x))
    features.append(obtain_std(f_body_acc_y))
    features.append(obtain_std(f_body_acc_z))

    features.extend(obtain_ar_coefficients(f_body_acc_x, 4))
    features.extend(obtain_ar_coefficients(f_body_acc_y, 4))
    features.extend(obtain_ar_coefficients(f_body_acc_z, 4))

    features.append(obtain_max_index(f_body_acc_x))
    features.append(obtain_max_index(f_body_acc_y))
    features.append(obtain_max_index(f_body_acc_z))

    features.append(obtain_skewness(f_body_acc_x))
    features.append(obtain_skewness(f_body_acc_y))
    features.append(obtain_skewness(f_body_acc_z))
    return features


def extract_features_f_body_acc_mag(f_body_acc_mag):
    freqs = fftfreq(len(f_body_acc_mag))
    mask = freqs >= 0
    f_body_acc_mag = 2 * f_body_acc_mag[mask]
    features = []
    features.append(obtain_min(f_body_acc_mag))
    features.append(obtain_max(f_body_acc_mag))
    features.append(obtain_mean(f_body_acc_mag))
    features.append(obtain_std(f_body_acc_mag))
    features.extend(obtain_ar_coefficients(f_body_acc_mag, 4))
    features.append(obtain_max_index(f_body_acc_mag))
    features.append(obtain_skewness(f_body_acc_mag))
    return features


# This function takes in a 2D list of data points from one window slice
# and returns a list of the features extracted from the data points
def extract_features(two_d_data):
    # Each two_d_data gives us a ?*3 matrix
    num_points = len(two_d_data)
    two_d_data = np.asarray(two_d_data)
    two_d_data_transpose = two_d_data.T
    features = []
    # Add Acc magnitude
    acc_data_magnitude = obtain_magnitude(two_d_data_transpose[0], two_d_data_transpose[1],
                                          two_d_data_transpose[2])
    two_d_data_transpose = np.append(two_d_data_transpose, acc_data_magnitude.reshape(1, len(acc_data_magnitude)),
                                     axis=0)
    # Add Frequency body Acceleration
    f_body_acc_x = np.abs(fft(np.asanyarray(two_d_data_transpose[0])) / num_points)
    f_body_acc_y = np.abs(fft(np.asanyarray(two_d_data_transpose[1])) / num_points)
    f_body_acc_z = np.abs(fft(np.asanyarray(two_d_data_transpose[2])) / num_points)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_acc_x.reshape(1, len(f_body_acc_x)), axis=0)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_acc_y.reshape(1, len(f_body_acc_y)), axis=0)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_acc_z.reshape(1, len(f_body_acc_z)), axis=0)
    # Add Frequency body acceleration magnitude
    f_body_acc_magnitude = np.abs(fft(np.asanyarray(two_d_data_transpose[3])) / num_points)
    two_d_data_transpose = np.append(two_d_data_transpose,
                                     f_body_acc_magnitude.reshape(1, len(f_body_acc_magnitude)), axis=0)

    # Start extracting time features
    features.extend(extract_features_t_body_acc(two_d_data_transpose[0], two_d_data_transpose[1],
                                                two_d_data_transpose[2]))
    features.extend(extract_features_t_body_acc_mag(two_d_data_transpose[3]))

    # Start extracting frequency features
    features.extend(extract_features_f_body_acc(two_d_data_transpose[4], two_d_data_transpose[5],
                                                two_d_data_transpose[6]))
    features.extend(extract_features_f_body_acc_mag(two_d_data_transpose[7]))

    return features
