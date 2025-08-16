# RPS.py
# MODIFICATION OF player.py
import random
import numpy as np
import time

moves = ["R", "P", "S"]

def counter(move):
    return {'R': 'P', 'P': 'S', 'S': 'R', '':'null'}[move] 

def encode_state(opp_hist, my_hist, N=2):
    mapping = {"": 3, "R": 0, "P": 1, "S": 2}  # "" → 3 as "empty"
    return tuple([mapping[m] for m in opp_hist[-N:] + my_hist[-N:]])

#my_last_move = "R"  # Default move before the first round
def player(prev_play, opponent_history=[], my_history=[], q_data={"Q": {}, "last_state": None, "last_action": None}):
    global my_last_move
    # Append histories
    if prev_play != "":
        opponent_history.append(prev_play)
    if len(my_history) < len(opponent_history):
        my_history.append(my_last_move)
    
    N = 2
    state = encode_state(opponent_history, my_history, N)

    # Initialize Q-values for unseen state
    if state not in q_data["Q"]:
        q_data["Q"][state] = [0, 0, 0]  # Q-values for R, P, S

    # Epsilon-greedy policy
    epsilon = 0.1
    if random.random() < epsilon:
        action_idx = random.randint(0, 2)
    else:
        action_idx = int(np.argmax(q_data["Q"][state]))

    # Update Q-table based on last step
    if q_data["last_state"] is not None:
        reward = 0
        if my_history[-1] == counter(prev_play):
            reward = 1
        elif prev_play == counter(my_history[-1]):
            reward = -1

        last_q = q_data["Q"][q_data["last_state"]][q_data["last_action"]]
        max_future_q = max(q_data["Q"][state])
        q_data["Q"][q_data["last_state"]][q_data["last_action"]] = \
            last_q + 0.1 * (reward + 0.9 * max_future_q - last_q)

    # Choose move and save
    guess = moves[action_idx]
    q_data["last_state"] = state
    q_data["last_action"] = action_idx

    #global my_last_move
    my_last_move = guess
    return guess
