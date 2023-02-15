# Deep Learning models for custom environment
# from custom_environment import CustomEnv
# env = CustomEnv()

# # implemnet keras model ,simple DQN model
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Flatten
# from tensorflow.keras.optimizers import Adam

# class DQN(Sequential):
#     def __init__(self, action_space, observation_space):
#         super().__init__()
#         self.add(Flatten(input_shape=(1,) + observation_space))
#         self.add(Dense(24, activation="relu"))
#         self.add(Dense(24, activation="relu"))
#         self.add(Dense(action_space, activation="linear"))
#         self.compile(loss="mse", optimizer=Adam(lr=0.001))