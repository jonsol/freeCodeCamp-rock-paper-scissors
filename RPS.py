import random

def player(prev_play, opponent_history=[], my_history=[]):
    # Store opponent play
    if prev_play:
        opponent_history.append(prev_play)

    # Store own last move
    if hasattr(player, "last_move"):
        my_history.append(player.last_move)

    if not hasattr(player, "patterns"):
        player.patterns = {}

    patterns = player.patterns

    # Random for first few rounds
    if len(opponent_history) < 3:
        guess = random.choice(["R", "P", "S"])
        player.last_move = guess
        return guess

    # Markov chain prediction
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

    # 🔍 Detect reactive bot like Abbey
    if len(my_history) >= 5:
        # Count how many times opponent beats my last move
        counter = {"R": "P", "P": "S", "S": "R"}
        beaten = 0
        for my, opp in zip(my_history[-5:], opponent_history[-5:]):
            if opp == counter[my]:
                beaten += 1

        if beaten >= 4:
            # They are clearly reacting → switch strategy
            counter_to_my_last = {"R": "S", "P": "R", "S": "P"}
            guess = counter_to_my_last[my_history[-1]]

    player.last_move = guess
    return guess
