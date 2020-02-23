from keras.callbacks import EarlyStopping
from util import *

Y_test = load_data('Datasets/UCI-HAR-Dataset/UCI-HAR-Dataset/test/y_test.txt')
Y_test_OHE = one_hot_encode_labels(Y_test)
print(Y_test_OHE.shape)

X_test = load_data('Datasets/UCI-HAR-Dataset/UCI-HAR-Dataset/test/X_test.txt')
print(X_test.shape)

# X_train = load_data('Datasets/UCI-HAR-Dataset/UCI-HAR-Dataset/train/X_train.txt')
# print(X_train.shape)
# Y_train = load_data('Datasets/UCI-HAR-Dataset/UCI-HAR-Dataset/train/y_train.txt')
# print(Y_train.shape)

model = create_model()
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
model.fit(X_test, Y_test_OHE, epochs=2000, batch_size=8, validation_split=0.3, shuffle=True, callbacks=[es])
save_model(model, "First_attempt")
test_model(model, X_test, Y_test)

# feature_selection_decision_trees(X_test, Y_test)
# feature_selection_f_value(X_test, Y_test)
# feature_selection_feature_correlation(X_test)
