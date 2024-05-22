import numpy as np
from collections import deque

SEED = 42

class ReplayBuffer:
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.buffer = deque(maxlen=buffer_size)

    def add(self, state, action, reward, next_state, done):
        experience = (state, action, reward, next_state, done)
        self.buffer.append(experience)

    def sample(self, batch_size):
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        states, actions, rewards, next_states, dones = zip(*[self.buffer[idx] for idx in 
indices])
        return np.array(states), np.array(actions), np.array(rewards), np.array(next_states), np.array(dones)

def __len__(self):
	return len(self.buffer)

