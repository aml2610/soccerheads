import random


class WalkingEnvironment:
    def __init__(self):
        self.state = 0
        self.goal = 10

    def step(self, a):
        old_state = self.state
        if a == 1:
            self.state = self.state + 1
        else:
            self.state = self.state - 1
        return self.state, self.reward(old_state, self.state)

    def distance_to_goal(self, state):
        return abs(self.goal - state)

    def reward(self, old_state, new_state):
        return self.distance_to_goal(old_state) - self.distance_to_goal(new_state)

    def random_action(self):
        return random.randint(0, 1)

    def get_state(self):
        return self.state
