from MachineLearning.main_code.util_main import *

model_nn = create_neural_network_model(172)

data_p_1 = []
data_p_2 = []
data_p_3 = []


p_1_movement = model_nn.predict(data_p_1)
p_2_movement = model_nn.predict(data_p_1)
p_3_movement = model_nn.predict(data_p_1)
output = [1, 2, 3]

if p_1_movement == "RIGHT" and p_2_movement == "NONE" and p_3_movement == "LEFT":
    output = [3, 2, 1]
elif p_1_movement == "RIGHT" and p_2_movement == "LEFT" and p_3_movement == "NONE":
    output = [2, 1, 3]
elif p_1_movement == "RIGHT" and p_2_movement == "LEFT" and p_3_movement == "LEFT":
    output = [2, 3, 1]
elif p_1_movement == "NONE" and p_2_movement == "RIGHT" and p_3_movement == "LEFT":
    output = [1, 3, 2]
elif p_1_movement == "NONE" and p_2_movement == "LEFT" and p_3_movement == "NONE":
    output = [2, 1, 3]
# Output remains the same
else:
    output = [1, 2, 3]


