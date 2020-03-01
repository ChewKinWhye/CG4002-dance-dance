from keras.callbacks import EarlyStopping
from util import *
import os
import numpy as np
from sklearn.svm import SVC


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
    y_train = load_data_uci("Data-sets/UCI-HAR-Data-set/UCI-HAR-Data-set/train/y_train.txt")
    y_test = load_data_uci("Data-sets/UCI-HAR-Data-set/UCI-HAR-Data-set/test/y_test.txt")
    return x_train, y_train, x_test, y_test


x_train, y_train, x_test, y_test = load_data_set_raw()
Y_train_OHE = one_hot_encode_labels(y_train)
Y_test_OHE = one_hot_encode_labels(y_test)

# Neural network
model_nn = create_neural_network_model(172)
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
# Train model
model_nn.fit(x_train, Y_train_OHE, validation_data=(x_test, Y_test_OHE), epochs=2000,
             batch_size=8, shuffle=True, callbacks=[es])
save_model(model_nn, "neural_network_mode")
test_model(model_nn, x_test, y_test)

# Support vector machine
model_svm = create_svm_model()
model_svm.fit(x_train, Y_train_OHE, validation_data=(x_test, Y_test_OHE), epochs=2000,
              batch_size=8, shuffle=True, callbacks=[es])
test_model(model_nn, x_test, y_test)
save_model(model_nn, "neural_network_mode")

