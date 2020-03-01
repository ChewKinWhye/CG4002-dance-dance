import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.svm import SVC

from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import pandas as pd
import os
from feature_extraction import extract_features


def feature_selection_remove_correlated(x_train, x_test):
    correlated_features = set()
    correlation_matrix = x_train.corr()
    for i in range(len(correlation_matrix.columns)):
        for j in range(i):
            if abs(correlation_matrix.iloc[i, j]) > 0.8:
                colname = correlation_matrix.columns[i]
                correlated_features.add(colname)
    print(str(len(correlated_features)) + " correlated features removed")
    x_train = x_train.drop(correlated_features, axis=1)
    x_test = x_test.drop(correlated_features, axis=1)
    return x_train, x_test


def feature_selection_rfe(x_train, y_train):
    y_train = y_train.to_numpy()
    y_train = y_train.reshape(len(y_train))
    print("Starting training")
    rfc = RandomForestClassifier(random_state=101)
    rfecv = RFECV(estimator=rfc, step=1, cv=StratifiedKFold(10), scoring='accuracy')
    selector = rfecv.fit(x_train, y_train)
    print('Optimal number of features: {}'.format(rfecv.n_features_))
    plt.figure(figsize=(16, 9))
    plt.title('Recursive Feature Elimination with Cross-Validation', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Number of features selected', fontsize=14, labelpad=20)
    plt.ylabel('% Correct Classification', fontsize=14, labelpad=20)
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_, color='#303F9F', linewidth=3)
    plt.show()
    print(selector.support_)
    print(selector.ranking_)


# This function ranks the features based on the Gini importance
def feature_selection_decision_trees(x_test, y_test):
    model = ExtraTreesClassifier()
    model.fit(x_test, y_test)
    print(model.feature_importances_)
    feat_importances = pd.Series(model.feature_importances_, index=x_test.columns)
    feat_importances.nlargest(10).plot(kind='barh')
    plt.show()


def feature_selection_f_value(x_test, y_test):
    bestfeatures = SelectKBest(score_func=f_classif, k=10)
    fit = bestfeatures.fit(x_test, y_test)
    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(x_test.columns)
    # concat two dataframes for better visualization
    featureScores = pd.concat([dfcolumns, dfscores], axis=1)
    featureScores.columns = ['Feature-Index', 'Score']  # naming the dataframe
    print(featureScores.nlargest(len(featureScores), 'Score'))


# def feature_selection_feature_correlation(x_test):
#     corrmat = x_test.corr()
#     print(x_test)
#     print(corrmat)
#     top_corr_features = corrmat.index
#     plt.figure(figsize=(20, 20))
#     # plot heat map
#     g = sns.heatmap(x_test[top_corr_features].corr(), annot=True, cmap="RdYlGn")


def create_neural_network_model(input_dimension):
    model = Sequential()
    model.add(Dense(32, input_dim=input_dimension, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(6, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def create_svm_model():
    clf = SVC(gamma='auto')
    return clf


def test_model(model_to_test, x_test, y_test):
    predictions = model_to_test.predict(x_test, batch_size=64, verbose=1)
    predictions_boolean = np.argmax(predictions, axis=1)
    print(predictions_boolean)
    # Count start from 1
    predictions_boolean += 1
    y_test = y_test.astype(int)
    print(y_test)
    print(classification_report(y_test, predictions_boolean))


def save_model(model_to_save, name):
    model_json = model_to_save.to_json()
    with open(name + ".json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model_to_save.save_weights(name + ".h5")
    print("Saved model to disk")


def load_model(model_name):
    json_file = open(model_name + '.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_name + ".h5")
    print("Loaded model from disk")
    return loaded_model


def load_data_uci(filename):
    file = open(filename, "r")
    lines_split = []
    for line in file:
        line_split = line.split()
        lines_split.append(line_split)
    df = pd.DataFrame(lines_split)
    df = df.dropna()
    return df


def load_data_sets_uci(data_set_root):
    y_test = load_data_uci(os.path.join(data_set_root, "test", "y_test.txt"))
    x_test = load_data_uci(os.path.join(data_set_root, "test", "X_test.txt"))
    x_train = load_data_uci(os.path.join(data_set_root, "train", "X_train.txt"))
    y_train = load_data_uci(os.path.join(data_set_root, "train", "y_train.txt"))
    return x_train.astype(float), y_train.astype(int), x_test.astype(float), y_test.astype(int)


def one_hot_encode_labels(labels):
    one_hot_encoder = OneHotEncoder(sparse=False)
    one_hot_encoded = one_hot_encoder.fit_transform(labels)
    return one_hot_encoded


def load_data_from_csv(csv_file_name):
    data = pd.read_csv(csv_file_name)
    return data


def load_data_motion_sense(filename, root_dir, lookup, time_step):
    first = True
    for csv_files in os.listdir(os.path.join(root_dir, filename)):
        if csv_files.find('.csv'):
            if first:
                data_set_x = load_data_from_csv(os.path.join(root_dir, filename, csv_files))
                first = False
            else:
                data = load_data_from_csv(os.path.join(root_dir, filename, csv_files))
                data_set_x = data_set_x.append(data)

    data_set_x = continuous_to_time_step(data_set_x, time_step, 12)
    data_set_x = extract_features(data_set_x)
    label = np.full(len(data_set_x), lookup[filename[0:3]])
    data_set_y = pd.DataFrame(label, columns=['Labels'])
    return data_set_x, data_set_y


def load_data_sets_motion_sense(root_dir, lookup, time_step):
    first = True
    for folders in os.listdir(root_dir):
        print(folders)
        if first:
            data_set_x, data_set_y = load_data_motion_sense(folders, root_dir, lookup, time_step)
            first = False
        else:
            temp_x, temp_y = load_data_motion_sense(folders, root_dir, lookup, time_step)
            data_set_x = data_set_x.append(temp_x)
            data_set_y = data_set_y.append(temp_y)
        print(np.asarray(data_set_x).shape)
        print(np.asarray(data_set_y).shape)
    data_set_y = data_set_y.dropna()
    return data_set_x, data_set_y


# Returns a rows * window_size * num_features array
def continuous_to_time_step(x, window_size, num_features):
    x.drop(x.iloc[:, 0:1], inplace=True, axis=1)
    first = True
    for i in range(0, num_features):
        column = x.iloc[:, i:i+1]
        column = column.head(len(column) - len(column)%window_size)
        column = column.to_numpy()
        column = column.reshape((int(column.shape[0] / window_size), window_size))
        if first:
            data_reshaped = column
            first = False
        else:
            data_reshaped = np.dstack((data_reshaped, column))
    return data_reshaped
