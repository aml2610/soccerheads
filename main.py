from time import sleep
from keyboard_adapter import wait_for_space_press, start_listening_for_s_press, stop_listening_for_s_press
from ai_q_learning import QLearningAgent
from soccerheads_environment import SoccerHeadsEnvironment, hash_state


MOVE_TO_ACTION_INDEX = {
    "LEFT": 0,
    "RIGHT": 1,
    "JUMP": 2,
    "KICK": 3
}
SLEEP_TIME_BEFORE_START = 1


stopped = False


def stop():
    global stopped
    stopped = True
    stop_listening_for_s_press()


def play():
    global stopped
    sleep(SLEEP_TIME_BEFORE_START)
    env = SoccerHeadsEnvironment()
    agent = QLearningAgent(env.get_n_actions())
    while not stopped:
        current_state = env.get_state()
        if current_state == (706, 299):
            sleep(0.5)
            env.refresh_state()
        else:
            hashed_current_state = hash_state(current_state)
            action = agent.get_next_move(hashed_current_state)
            observation, reward = env.step(action)
            move, _ = action
            agent.learn(
                hashed_current_state,
                MOVE_TO_ACTION_INDEX[move],
                hash_state(observation),
                reward
            )


if __name__ == "__main__":
    wait_for_space_press()
    start_listening_for_s_press(stop)
    play()
