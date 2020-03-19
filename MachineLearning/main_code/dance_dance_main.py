from util_main import *
from keras.callbacks import EarlyStopping
from sklearn.model_selection import KFold
import tensorflow as tf
import numpy as np

data_set_path = "Data-sets/Dance_Data"
sampling_rate = 20
window_length = 2.56  # Seconds

x_data, y_data = load_dance_dance_data_set(data_set_path, sampling_rate=sampling_rate, window_length=window_length)
print("Feature shape:", np.asarray(x_data).shape)
print("Label shape:", np.asarray(y_data).shape)

y_OHE_data = one_hot_encode_labels(y_data)

model_nn = create_neural_network_model(input_dimension=x_data.shape[1], output_dimension=y_OHE_data.shape[1])
print(x_data.shape[1])
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
# K-fold cross validation, only used for model evaluation
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
    # confusion_matrix_total += confusion_matrix
    accuracy_total += accuracy
    # break
# print(confusion_matrix_total/10)
print("Accuracy: " + str(accuracy_total*10) + "%")


# Load model
# Single example
data_point = x_data[0:1]
y = model_nn.predict(data_point)
print(y)
