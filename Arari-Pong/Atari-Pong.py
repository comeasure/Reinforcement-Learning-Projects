import gym
import numpy as np
import tensorflow as tf
from tensorflow.keras import models, layers, optimizers
from collections import deque
import random

# Define DQN model
def build_model(state_shape, action_shape):
    model = models.Sequential()
    model.add(layers.Dense(24, input_shape=state_shape, activation='relu'))
    model.add(layers.Dense(24, activation='relu'))
    model.add(layers.Dense(action_shape, activation='linear'))
    return model

# Define DQN agent
class DQNAgent:
    def __init__(self, state_shape, action_shape):
        self.state_shape = state_shape
        self.action_shape = action_shape
        self.model = build_model(state_shape, action_shape)
        self.target_model = build_model(state_shape, action_shape)
        self.target_model.set_weights(self.model.get_weights())
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.model.compile(loss='mse', optimizer=optimizers.Adam(learning_rate=self.learning_rate))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_shape)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.target_model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

# Initialize gym environment and agent
env = gym.make('Pong-v0')
state_shape = env.observation_space.shape
action_shape = env.action_space.n
agent = DQNAgent(state_shape, action_shape)

# Train the agent
episodes = 1000
batch_size = 32

for e in range(episodes):
    state = env.reset()
    state = np.reshape(state, [1, state_shape[0]])
    for time in range(5000):
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        reward = reward if not done else -10
        next_state = np.reshape(next_state, [1, state_shape[0]])
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        if done:
            agent.update_target_model()
            print(f"episode: {e}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
            break
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

