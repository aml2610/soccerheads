from time import sleep
from keyboard_adapter import move_left, move_right, jump, kick, wait_for_space_press, start_listening_for_s_press, \
    stop_listening_for_s_press
from ai_q_learning import QLearningAgent
from screen_frame_grabber import grab_screen_frame
from ball_tracker import get_current_ball_position


MOVE_TO_KEYBOARD_COMMAND = {
    "LEFT": move_left,
    "RIGHT": move_right,
    "JUMP": jump,
    "KICK": kick
}
MOVE_TO_ACTION_INDEX = {
    "LEFT": 0,
    "RIGHT": 1,
    "JUMP": 2,
    "KICK": 3
}
N_POSSIBLE_MOVES = 4
SCREEN_FRAME_BBOX = (520, 400, 1950, 1150)
SLEEP_TIME_BEFORE_START = 1
SLEEP_TIME_BETWEEN_MOVES = 0.1


stopped = False


def stop():
    global stopped
    stopped = True
    stop_listening_for_s_press()


def apply_move(move, interval):
    command = MOVE_TO_KEYBOARD_COMMAND[move]
    command(interval)


def build_state(ball_position):
    (x, y) = ball_position
    return f"{x},{y}"


def compute_reward(ball_position):
    (x, y) = ball_position
    return -x + y


def play():
    global stopped
    global old_state
    global new_state
    old_state = None
    new_state = None
    agent = QLearningAgent(N_POSSIBLE_MOVES)
    sleep(SLEEP_TIME_BEFORE_START)
    while not stopped:
        sleep(SLEEP_TIME_BETWEEN_MOVES)
        current_frame = grab_screen_frame(SCREEN_FRAME_BBOX)
        current_ball_position = get_current_ball_position(current_frame)
        if current_ball_position is not None:
            current_state = build_state(current_ball_position)
            next_move, interval = agent.get_next_move(current_state)
            apply_move(next_move, interval)
            old_state = new_state
            new_state = current_state
            agent.learn(
                old_state,
                MOVE_TO_ACTION_INDEX[next_move],
                new_state,
                compute_reward(current_ball_position)
            )


if __name__ == "__main__":
    wait_for_space_press()
    start_listening_for_s_press(stop)
    play()
