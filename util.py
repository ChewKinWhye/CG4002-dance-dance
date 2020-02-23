import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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


def create_model():
    model = Sequential()
    model.add(Dense(32, input_dim=561, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(6, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


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


def load_data(filename):
    file = open(filename, "r")
    lines_split = []
    for line in file:
        line_split = line.split()
        lines_split.append(line_split)
    df = pd.DataFrame(lines_split)
    df = df.dropna()
    # Makes the df a multiple of the window size
    # df = df.drop(df.index[len(df.index)//window_size*window_size:len(df.index)])
    return df


def one_hot_encode_labels(labels):
    one_hot_encoder = OneHotEncoder(sparse=False)
    one_hot_encoded = one_hot_encoder.fit_transform(labels)
    return one_hot_encoded
