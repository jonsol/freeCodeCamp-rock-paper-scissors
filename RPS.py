import random

def player(prev_play, opponent_history=[]):
    if prev_play:
        opponent_history.append(prev_play)

    if len(opponent_history) < 3:
        # For first few moves, pick random
        return random.choice(['R', 'P', 'S'])

    if not hasattr(player, "patterns"):
        player.patterns = {}

    patterns = player.patterns

    last_two = "".join(opponent_history[-2:])

    if last_two not in patterns:
        patterns[last_two] = {"R": 0, "P": 0, "S": 0}

    #  Only update pattern if enough history!
    if len(opponent_history) >= 4:
        last_three = "".join(opponent_history[-3:-1])
        next_move = opponent_history[-1]

        if last_three not in patterns:
            patterns[last_three] = {"R": 0, "P": 0, "S": 0}

        patterns[last_three][next_move] += 1

    prediction = max(patterns[last_two], key=patterns[last_two].get)

    counter_moves = {"R": "P", "P": "S", "S": "R"}
    guess = counter_moves[prediction]

    return guess

