from time import sleep
from screen_frame_grabber import grab_screen_frame
from ball_tracker import get_current_ball_position
from keyboard_adapter import move_left, move_right, jump, kick


SCREEN_FRAME_BBOX = (520, 400, 1950, 1150)
MOVE_TO_KEYBOARD_COMMAND = {
    "LEFT": move_left,
    "RIGHT": move_right,
    "JUMP": jump,
    "KICK": kick
}


def hash_state(state):
    (x, y) = state
    return f"{x},{y}"


def apply_action(action):
    move, interval = action
    command = MOVE_TO_KEYBOARD_COMMAND[move]
    command(interval)


class SoccerHeadsEnvironment:
    def __init__(self):
        self.state = None
        self.refresh_state()
        self.n_actions = 4

    def refresh_state(self):
        screen_frame = grab_screen_frame(SCREEN_FRAME_BBOX)
        ball_position = get_current_ball_position(screen_frame)
        # print("Ball position", ball_position)
        if ball_position is not None:
            self.state = ball_position
        else:
            self.refresh_state()

    def step(self, action):
        old_state = self.state
        apply_action(action)
        sleep(0.5)
        self.refresh_state()
        # print("Old state, action, new state", old_state, action, self.state)
        return self.state, self.reward(old_state, self.state)

    def reward(self, old_state, new_state):
        (x_old, y_old) = old_state
        (x_new, y_new) = new_state
        return -x_new + y_new

    def get_state(self):
        return self.state

    def get_n_actions(self):
        return self.n_actions
