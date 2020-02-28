import statistics
import numpy as np
from spectrum import aryule
from scipy.stats import pearsonr
from scipy.stats import entropy
import pandas as pd
from math import sqrt


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


def obtain_sma(data_x, data_y, data_z):
    sma = 0
    for i in range(len(data_x)):
        sma += abs(data_x[i]) + abs(data_y[i]) + abs(data_z[i])
    return sma


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


def extract_features(data):
    # Each two_d_data gives us a 128*12 matrix
    features_total = []
    for two_d_data in data:
        two_d_data_transpose = two_d_data.T
        features = []
        # Each row gives us a 128 matrix
        gyro_jerk_x = np.gradient(two_d_data_transpose[6])
        gyro_jerk_y = np.gradient(two_d_data_transpose[7])
        gyro_jerk_z = np.gradient(two_d_data_transpose[8])
        acc_jerk_x = np.gradient(two_d_data_transpose[9])
        acc_jerk_y = np.gradient(two_d_data_transpose[10])
        acc_jerk_z = np.gradient(two_d_data_transpose[11])

        two_d_data_transpose = np.append(two_d_data_transpose, gyro_jerk_x.reshape(1, len(gyro_jerk_x)), axis=0)
        two_d_data_transpose = np.append(two_d_data_transpose, gyro_jerk_y.reshape(1, len(gyro_jerk_y)), axis=0)
        two_d_data_transpose = np.append(two_d_data_transpose, gyro_jerk_z.reshape(1, len(gyro_jerk_z)), axis=0)
        two_d_data_transpose = np.append(two_d_data_transpose, acc_jerk_x.reshape(1, len(acc_jerk_x)), axis=0)
        two_d_data_transpose = np.append(two_d_data_transpose, acc_jerk_y.reshape(1, len(acc_jerk_y)), axis=0)
        two_d_data_transpose = np.append(two_d_data_transpose, acc_jerk_z.reshape(1, len(acc_jerk_z)), axis=0)
        acc_data_magnitude = obtain_magnitude(two_d_data_transpose[9], two_d_data_transpose[10],
                                              two_d_data_transpose[11])
        two_d_data_transpose = np.append(two_d_data_transpose, acc_data_magnitude.reshape(1, len(acc_data_magnitude)), axis=0)
        acc_data_jerk_magnitude = obtain_magnitude(two_d_data_transpose[15], two_d_data_transpose[16],
                                                   two_d_data_transpose[17])
        two_d_data_transpose = np.append(two_d_data_transpose,
                                         acc_data_jerk_magnitude.reshape(1, len(acc_data_jerk_magnitude)), axis=0)
        gyro_data_magnitude = obtain_magnitude(two_d_data_transpose[6], two_d_data_transpose[7],
                                               two_d_data_transpose[8])
        two_d_data_transpose = np.append(two_d_data_transpose,
                                         gyro_data_magnitude.reshape(1, len(gyro_data_magnitude)), axis=0)
        gyro_data_jerk_magnitude = obtain_magnitude(two_d_data_transpose[12], two_d_data_transpose[13],
                                                    two_d_data_transpose[14])
        two_d_data_transpose = np.append(two_d_data_transpose,
                                         gyro_data_jerk_magnitude.reshape(1, len(gyro_data_jerk_magnitude)), axis=0)

        for row in two_d_data_transpose:
            features.append(obtain_mean(row))
            features.append(obtain_std(row))
            features.extend(obtain_ar_coefficients(row, 1))
            features.extend(obtain_ar_coefficients(row, 2))
            features.extend(obtain_ar_coefficients(row, 3))
            features.extend(obtain_ar_coefficients(row, 4))
            features.append(obtain_entropy(row))
            features.append(obtain_skewness(row))
        features_total.append(features)
    return pd.DataFrame(features_total)


