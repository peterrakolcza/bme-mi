from time import time

import numpy as np
np.random.seed(0)

class FlappyAgent:

    def __init__(self, observation_space_size, action_space, n_iterations):
        self.q_table = np.zeros([*observation_space_size, len(action_space)])
        self.env_action_space = action_space
        self.n_iterations = n_iterations

        self.test = False

    def step(self, state):
        temp = self.q_table[state]

        max = -1
        maxIndex = -1
        for i in range(len(temp)):
            if max < temp[i]:
                max = temp[i]
                maxIndex = i

        action = maxIndex

        if not self.test:  # and ...:
            # action =
            pass
        else:
            # action =
            pass

        return action

    def epoch_end(self, epoch_reward_sum):
        pass

    def learn(self, old_state, action, new_state, reward):
        delta = 0.5
        temp = self.q_table[new_state]

        result = max(temp)

        self.q_table[old_state][action] = delta * self.q_table[old_state][action] + delta * (reward + 0.8 * result)

    def train_end(self):
        # ...
        self.test = True
