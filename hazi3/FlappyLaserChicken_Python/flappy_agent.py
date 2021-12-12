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
        # print(state)
        action = self.max_q_idx(state)

        if not self.test:  # and ...:
            # action =
            pass
        else:
            # action =
            pass

        return action

    def epoch_end(self, epoch_reward_sum):
        pass

    def action_from_q_table(self, old_state, action):
        return self.q_table[old_state[0]][old_state[1]][old_state[2]][old_state[3]][old_state[4]][action]

    def calc_new_q(self, a, new_state, reward, Q):
        return a*Q + a*(reward + 0.2*self.max_q_val(new_state))

    def learn(self, old_state, action, new_state, reward):
        a = 0.5
        Q = self.action_from_q_table(old_state, action)
        self.q_table[old_state[0]][old_state[1]][old_state[2]][old_state[3]
                                                               ][old_state[4]][action] = self.calc_new_q(a, new_state, reward, Q)

    def max_q_val(self, old_state):
        return max(self.q_table[old_state[0]][old_state[1]][old_state[2]][old_state[3]][old_state[4]])

    def max_q_idx(self, old_state):
        return list(self.q_table[old_state[0]][old_state[1]][old_state[2]][old_state[3]][old_state[4]]).index(max(self.q_table[old_state[0]][old_state[1]][old_state[2]][old_state[3]][old_state[4]]))

    def train_end(self):
        # ...
        self.test = True
