import random

def player(prev_play, opponent_history=[], my_history=[]):
    # Add to opponent history
    if prev_play:
        opponent_history.append(prev_play)

    # Add to your own move history
    if hasattr(player, "last_move"):
        my_history.append(player.last_move)

    if not hasattr(player, "patterns"):
        player.patterns = {}

    if len(opponent_history) < 3:
        guess = random.choice(["R", "P", "S"])
        player.last_move = guess
        return guess

    patterns = player.patterns
    last_two = "".join(opponent_history[-2:])

    if last_two not in patterns:
        patterns[last_two] = {"R": 0, "P": 0, "S": 0}

    if len(opponent_history) >= 4:
        last_three = "".join(opponent_history[-3:-1])
        next_move = opponent_history[-1]
        if last_three not in patterns:
            patterns[last_three] = {"R": 0, "P": 0, "S": 0}
        patterns[last_three][next_move] += 1

    prediction = max(patterns[last_two], key=patterns[last_two].get)
    counter_moves = {"R": "P", "P": "S", "S": "R"}
    guess = counter_moves[prediction]

    # Try to detect if we are losing to a reactive bot like abbey
    if len(my_history) >= 1:
        # If opponent's last move beats our last move a lot, switch!
        counter = {"R": "S", "P": "R", "S": "P"}
        if opponent_history[-1] == counter[my_history[-1]]:
            # They are countering us! So flip the guess
            guess = counter_moves[guess]

    player.last_move = guess
    return guess