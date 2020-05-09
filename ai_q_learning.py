import numpy as np
import random
import ai_random


ALPHA = 0.1
EPSILON = 0.2
GAMMA = 0.8
ACTION_INDEX_TO_MOVE = {
    0: "LEFT",
    1: "RIGHT",
    2: "JUMP",
    3: "KICK"
}


class QLearningAgent:
    def __init__(self, action_space_size):
        self.action_space_size = action_space_size
        self.q_table = {}
        self.alpha = ALPHA
        self.epsilon = EPSILON
        self.gamma = GAMMA

    def get_next_move(self, current_state):
        if random.uniform(0, 1) < self.epsilon:
            print("Playing random because of epsilon")
            return ai_random.get_next_move()
        else:
            possible_moves = self.q_table.get(current_state, None)
            if possible_moves is None:
                print("Playing random because of no knowledge")
                return ai_random.get_next_move()
            chosen_move = ACTION_INDEX_TO_MOVE[np.argmax(possible_moves)]
            print("Playing according to knowledge")
            # print("Knowledge is", possible_moves)
            return chosen_move, ai_random.get_random_interval(chosen_move)

    def compute_q_value(self, old_state, action, new_state, reward):
        new_state_possible_moves = self.q_table.get(new_state, None)
        new_state_max_reward = 0 if new_state_possible_moves is None else np.max(new_state_possible_moves)
        return self.q_table[old_state][action] + self.alpha * (reward + self.gamma * new_state_max_reward
                                                               - self.q_table[old_state][action])

    def learn(self, old_state, action, new_state, reward):
        if self.q_table.get(old_state, None) is None:
            self.q_table[old_state] = np.zeros(self.action_space_size)
        self.q_table[old_state][action] = self.compute_q_value(old_state, action, new_state, reward)
        # print("Learnt knowledge", self.q_table[old_state])
