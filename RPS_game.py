# DO NOT MODIFY THIS FILE

import random

def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)

    # Frequency-based strategy (for Mrugesh and Kris)
    if len(opponent_history) >= 5:
        guess = predict_move(opponent_history)
        return counter_move(guess)

    # Random fallback (for first few rounds or unpredictable bots)
    return random.choice(["R", "P", "S"])

def predict_move(history):
    # Use a sliding window of size 3 to predict opponent's next move
    if len(history) < 3:
        return random.choice(["R", "P", "S"])

    last_3 = "".join(history[-3:])
    pattern_counts = {}

    # Build pattern frequency dictionary
    for i in range(len(history) - 3):
        pattern = "".join(history[i:i+3])
        next_move = history[i+3]
        if pattern == last_3:
            if next_move not in pattern_counts:
                pattern_counts[next_move] = 0
            pattern_counts[next_move] += 1

    if not pattern_counts:
        return random.choice(["R", "P", "S"])

    # Return the most likely next move
    return max(pattern_counts, key=pattern_counts.get)

def counter_move(move):
    # Return the move that beats the predicted move
    if move == "R":
        return "P"
    elif move == "P":
        return "S"
    elif move == "S":
        return "R"
    else:
        return random.choice(["R", "P", "S"])  # In case of empty or unknown
