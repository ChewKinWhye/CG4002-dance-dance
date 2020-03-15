from keras.callbacks import EarlyStopping
from old_code_unused.util import *
import os
import numpy as np
from sklearn.model_selection import KFold # import KFold


def load_data_set_raw():
    x_train = np.zeros((7352, 128, 3))
    data_set_root = "Data-sets/UCI-HAR-Data-set/UCI-HAR-Data-set/train/Inertial Signals"
    for text_file in os.listdir(data_set_root):
        full_path = os.path.join(data_set_root, text_file)
        temp = load_data_uci(full_path).to_numpy().astype(float)
        temp = temp.reshape((len(temp), 128, 1))
        x_train = np.concatenate((x_train, temp), axis=2)
    x_train = extract_features(x_train)
    x_test = np.zeros((2947, 128, 3))
    data_set_root = "Data-sets/UCI-HAR-Data-set/UCI-HAR-Data-set/test/Inertial Signals"
    for text_file in os.listdir(data_set_root):
        full_path = os.path.join(data_set_root, text_file)
        temp = load_data_uci(full_path).to_numpy().astype(float)
        temp = temp.reshape((len(temp), 128, 1))
        x_test = np.concatenate((x_test, temp), axis=2)
    x_test = extract_features(x_test)
    x_data = np.concatenate((x_train, x_test), axis=0)
    y_train = load_data_uci("Data-sets/UCI-HAR-Data-set/UCI-HAR-Data-set/train/y_train.txt")
    y_test = load_data_uci("Data-sets/UCI-HAR-Data-set/UCI-HAR-Data-set/test/y_test.txt")
    y_data = np.concatenate((y_train, y_test), axis=0)
    return x_data, y_data


x_data, y_data = load_data_set_raw()
y_OHE_data = one_hot_encode_labels(y_data)
# Neural network
model_nn = create_neural_network_model(87)
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
# K-fold cross validation
kf = KFold(n_splits=10)
kf.get_n_splits(x_data)
confusion_matrix_total = np.zeros((6, 6))
accuracy_total = 0
for train_index, test_index in kf.split(x_data):
    x_train, x_test = x_data[train_index], x_data[test_index]
    y_train_OHE, y_test_OHE = y_OHE_data[train_index], y_OHE_data[test_index]
    model_nn.fit(x_train, y_train_OHE, validation_data=(x_test, y_test_OHE), epochs=2000,
                 batch_size=8, shuffle=True, callbacks=[es])
    save_model(model_nn, "neural_network_model")
    confusion_matrix, accuracy = test_model_nn(model_nn, x_test, y_data[test_index])
    confusion_matrix_total += confusion_matrix
    accuracy_total += accuracy
print(confusion_matrix_total/10)
print(accuracy_total/10)

# Single example
data_point = x_data[0:1]
y = model_nn.predict(data_point)
print(y)
