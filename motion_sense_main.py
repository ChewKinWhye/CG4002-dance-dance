from keras.callbacks import EarlyStopping
from util import *
root_dir = "Data-sets/motionsense-dataset/A_DeviceMotion_data/A_DeviceMotion_data"
lookup = {"dws": 1, "jog": 2, "sit": 3, "std": 4, "ups": 5, "wlk": 6}
time_step = 128

data_set_x, data_set_y = load_data_sets_motion_sense(root_dir, lookup, time_step)
data_set_y_OHE = one_hot_encode_labels(data_set_y)
model = create_model(172)
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)
# Train model
model.fit(data_set_x, data_set_y_OHE, validation_split=0.3, epochs=2000,
          batch_size=8, shuffle=True, callbacks=[es])
