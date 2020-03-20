from MachineLearning.main_code.util_main import *
from keras.callbacks import EarlyStopping
from sklearn.utils import shuffle

import numpy as np

data_set_path = "Data-sets/Dance_Data"
sampling_rate = 5
window_length = 2.56  # Seconds

x_data, y_data = load_dance_dance_data_set(data_set_path, sampling_rate=sampling_rate, window_length=window_length)
print("Feature shape:", np.asarray(x_data).shape)
print("Label shape:", np.asarray(y_data).shape)

x_data, y_data = shuffle(x_data, y_data)
x_train_data, x_test_data = x_data[:int(len(x_data)*0.7), :], x_data[int(len(x_data)*0.7):, :]
y_train_data, y_test_data = y_data[:int(len(x_data)*0.7), :], y_data[int(len(x_data)*0.7):, :]

y_train_OHE_data = one_hot_encode_labels(y_train_data)
y_test_OHE_data = one_hot_encode_labels(y_test_data)

model_nn = create_neural_network_model(input_dimension=x_data.shape[1], output_dimension=y_train_OHE_data.shape[1])

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=15)

model_nn.fit(x_train_data, y_train_OHE_data, validation_data=[x_test_data, y_test_OHE_data], epochs=2000,
             batch_size=8, shuffle=True, callbacks=[es])

save_model(model_nn, "neural_network_model")
confusion_matrix, accuracy = test_model_nn(model_nn, x_test_data, y_test_data)
print(confusion_matrix)


# Load model
# Single example
data_point = x_data[0:1]
y = model_nn.predict(data_point)
print(y)
