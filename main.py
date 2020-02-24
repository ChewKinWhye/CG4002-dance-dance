from keras.callbacks import EarlyStopping
from util import *
data_set_root = "Data-sets/UCI-HAR-Data-set/UCI-HAR-Data-set"

# Load data sets
X_train, Y_train, X_test, Y_test = load_data_sets(data_set_root)
Y_test_OHE = one_hot_encode_labels(Y_test)
Y_train_OHE = one_hot_encode_labels(Y_train)
print("Data sets loaded")

X_train, X_test = feature_selection_remove_correlated(X_train, X_test)
feature_selection_rfe(X_train, Y_train)

# feature_selection_rfe(X_train, Y_train)

# feature_selection_lasso(X_train, Y_train)
# feature_selection_decision_trees(X_test, Y_test)
# feature_selection_f_value(X_test, Y_test)
# feature_selection_feature_correlation(X_test)

# Create model
# model = create_model()
# es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
# # Train model
# model.fit(X_train, Y_train_OHE, validation_data=(X_test, Y_test_OHE), epochs=2000,
#           batch_size=8, shuffle=True, callbacks=[es])
#
# save_model(model, "First_attempt")
# test_model(model, X_test, Y_test)


