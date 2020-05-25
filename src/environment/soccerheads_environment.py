from time import sleep
from src.screen.screen_frame_grabber import grab_screen_frame
from src.ai.soccerheads_object_tracker import get_current_ball_position, get_current_my_player_position
from src.keyboard.keyboard_adapter import move_left, move_right, jump, kick


SCREEN_FRAME_BBOX = (520, 400, 1950, 1150)
MOVE_TO_KEYBOARD_COMMAND = {
    "LEFT": move_left,
    "RIGHT": move_right,
    "JUMP": jump,
    "KICK": kick
}
GOAL_SCORED_BUMP = 500
GOAL_CONCEDED_BUMP = -500
CORRECT_POSITION_BUMP = 50
INCORRECT_POSITION_BUMP = -100


def hash_state(state):
    ((x_ball, y_ball), (x_me, y_me)) = state
    return f"{x_ball},{y_ball};{x_me},{y_me}"


def apply_action(action):
    move, interval = action
    command = MOVE_TO_KEYBOARD_COMMAND[move]
    command(interval)


def floor_coords_to_tens(coords):
    (x, y) = coords
    return x / 10 * 10, y / 10 * 10


class SoccerHeadsEnvironment:
    def __init__(self):
        self.state = None
        self.refresh_state()
        self.n_actions = 4

    def refresh_state(self):
        screen_frame = grab_screen_frame(SCREEN_FRAME_BBOX)
        ball_position = get_current_ball_position(screen_frame)
        my_player_position = get_current_my_player_position(screen_frame)
        # print("Ball position", ball_position)
        # print("My player position", my_player_position)
        if ball_position is not None and my_player_position is not None:
            self.state = (floor_coords_to_tens(ball_position), floor_coords_to_tens(my_player_position))
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
        ((x_ball_old, y_ball_old), _) = old_state
        ((x_ball_new, y_ball_new), (x_me_new, y_me_new)) = new_state
        how_close_ball_has_moved_to_opponent_post = (-x_ball_new + y_ball_new) - (-x_ball_old + y_ball_old)
        i_am_positioned_correctly = x_me_new - x_ball_new > 0
        correct_position_bump = CORRECT_POSITION_BUMP if i_am_positioned_correctly else INCORRECT_POSITION_BUMP
        return how_close_ball_has_moved_to_opponent_post + correct_position_bump

    def get_state(self):
        return self.state

    def get_n_actions(self):
        return self.n_actions
