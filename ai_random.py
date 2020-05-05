from random import randint, uniform


POSSIBLE_MOVES = ["LEFT", "RIGHT", "JUMP", "KICK"]

MOVE_INTERVAL_MIN_MAX = [0.1, 0.5]
JUMP_INTERVAL_MIN_MAX = [0.0, 0.3]
KICK_INTERVAL_MIN_MAX = [0.8, 1.0]


MOVE_TO_INTERVAL_MIN_MAX = {
    "LEFT": MOVE_INTERVAL_MIN_MAX,
    "RIGHT": MOVE_INTERVAL_MIN_MAX,
    "JUMP": JUMP_INTERVAL_MIN_MAX,
    "KICK": KICK_INTERVAL_MIN_MAX
}


def get_random_interval(move):
    [interval_min, interval_max] = MOVE_TO_INTERVAL_MIN_MAX[move]
    return uniform(interval_min, interval_max)


def get_next_move():
    move = POSSIBLE_MOVES[randint(0, len(POSSIBLE_MOVES) - 1)]
    interval = get_random_interval(move)
    return move, interval
